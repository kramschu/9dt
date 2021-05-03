from components.validation import Validators
from components.error_handling import ErrorHandlers
from models import Games, Players, Moves, db
from flask import jsonify, Response
from sqlalchemy import desc
import json


class GameFunctions:

    def _get_in_progress_games(self):
        game_data = Games.query.get(game_id)
        if game_data is None:
            return ErrorHandlers._404_error('Game not Found')

        in_progress_ids = []
        all_games = Games.query.all()
        for row in all_games:
            if row.game_state == "IN_PROGRESS":
                in_progress_ids.append(str(row.game_id))

        return jsonify({
                    'games': in_progress_ids
                    })

    def _create_game(self, players, columns, rows):
        error = Validators()._validate_board(players, columns, rows)
        if error:
            return error

        # This step is currently not needed. The players table is not used.
        # TODO: replace all player_name references with foreign_key on
        # primary_key
        player_ids = []
        for player in players:
            player_row = Players.query.filter_by(player_name=player).first()
            if player_row is None:
                new_player = Players(player_name=player)
                db.session.add(new_player)
                db.session.commit()
                player_row = Players.query.filter_by(player_name=player).first()
            player_ids.append(player_row.player_name)
        player_ids = ','.join(map(str, player_ids))

        new_game = Games(players=str(player_ids),
                         game_columns=columns, game_rows=rows,
                         game_state="IN_PROGRESS")
        db.session.add(new_game)
        db.session.commit()
        game_id = new_game.game_id
        return jsonify({"gameId": str(game_id)})

    def _get_game_state(self, game_id):
        game_data = Games.query.get(game_id)
        if game_data is None:
            return ErrorHandlers._404_error('Game not Found')

        if game_data.game_state == 'DONE':
            game_object = {
                "players": game_data.players,
                "state": game_data.game_state,
                'winner': game_data.winner
            }
        else:
            game_object = {
                "players": game_data.players,
                "state": game_data.game_state,
            }
        return jsonify(game_object)

    def _get_moves_list(self, game_id):
        moves_list = []

        game_data = Games.query.get(game_id)
        if game_data is None:
            return ErrorHandlers._404_error('Game not Found')

        moves = Moves.query.filter_by(game_id=game_id).all()
        if moves is []:
            moves_list = []
        else:
            for move in moves:
                if move.move_column == 0:
                    move_object = {
                        "type": "QUIT",
                        "player": move.player_id,
                    }
                else:
                    move_object = {
                        "type": "MOVE",
                        "player": move.player_id,
                        "column": move.move_column
                    }
                moves_list.append(move_object)

        return jsonify({
                "moves": moves_list
            })

    def _move_player(self, game_id, player_id, column):
        row = Validators()._validate_move(game_id, player_id, column)

        # TODO: I need to update this part of the function.
        # There is a better way of checking response besides a bare try/except.
        try:
            isinstance(row, int)
            last_move = Moves.query.filter_by(
                game_id=game_id).order_by(desc(Moves.move_number)).first()
            move_number = 1 if last_move is None else last_move.move_number + 1

            new_move = Moves(move_column=column, move_row=row,
                             move_number=move_number, game_id=game_id,
                             player_id=player_id)
            db.session.add(new_move)
            db.session.commit()
            Validators()._validate_game_state(game_id, player_id)
            return jsonify({
                    "move": f"{game_id}/moves/{move_number}"
                })

        except:
            return row

    def _get_move(self, game_id, move_number):
        move = Moves.query.filter_by(game_id=game_id).filter_by(
                                     move_number=move_number).first()
        error = Validators()._validate_get_move(move, game_id, move_number)
        if error:
            return error

        if move.move_column == 0:
            move_object = {
                "type": "QUIT",
                "player": move.player_id,
            }
        else:
            move_object = {
                "type": "MOVE",
                "player": move.player_id,
                "column": move.move_column
            }
        return jsonify(move_object)

    def _quit_game(self, game_id, player_id):
        error = Validators()._validate_quit(game_id, player_id)
        if error:
            return error
        last_move = Moves.query.filter_by(game_id=game_id).order_by(
            desc(Moves.move_number)).first()
        move_number = 1 if last_move is None else last_move.move_number + 1
        new_move = Moves(move_column=0, move_row=0, move_number=move_number,
                         game_id=game_id, player_id=player_id)
        db.session.add(new_move)
        db.session.commit()

        current_game = Games.query.get(game_id)
        quiters = Moves.query.filter_by(game_id=game_id).filter_by(move_column=0).all()
        players = (current_game.players).split(",")
        if len(quiters) >= len(players) - 1:
            for quiter in quiters:
                if quiter.player_id in players:
                    players.remove(quiter.player_id)
            current_game.winner = players[0]
            current_game.game_state = 'DONE'
        db.session.commit()

        return Response(
                'OK',
                status=202,
            )
