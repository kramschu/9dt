from components.error_handling import ErrorHandlers
from models import Games, Players, Moves, db
from sqlalchemy import asc


class IncorrectValue(ValueError):
    status_code = 400


class Validators():

    def _validate_board(self, players, columns, rows):
        if columns < 4 or rows < 4:
            return ErrorHandlers._400_error(f'Unable to create board with \
                columns: {columns} and rows: {rows}. Board must have at least \
                    4 rows and 4 columns')

        if len(players) < 2:
            return ErrorHandlers._400_error(f'Unable to create board with \
                current players. Game must have at least two players')

    def _validate_get_move(self, move, game_id, move_number):
        game_data = Games.query.get(game_id)
        if game_data is None:
            return ErrorHandlers._404_error('Game not Found')

        if move is None:
            return ErrorHandlers._404_error('Move not Found')

    def _validate_move(self, game_id, player_id, column):
        game_data = Games.query.get(game_id)
        if game_data is None:
            return ErrorHandlers._404_error('Game not Found')
        if player_id not in (game_data.players).split(","):
            return ErrorHandlers._404_error(
                f'{player_id} is not in this game.')

        # TODO: Rework/simplify function logic
        player_moves = Moves.query.filter_by(game_id=game_id).filter_by(
            player_id=player_id).all()
        for player in (game_data.players).split(","):
            opponent_moves = Moves.query.filter_by(game_id=game_id).filter_by(
                player_id=player).all()
            if (len(player_moves) > len(opponent_moves)):
                return ErrorHandlers._409_error(f'It is not players turn, \
                    please wait for other players to move')
            if ((len(player_moves) == len(opponent_moves)) and
               (player_id != (game_data.players).split(",")[0]) and
               (player != player_id)):
                return ErrorHandlers._409_error(f'It is not players turn, \
                    please wait for other players to move')

        if column > game_data.game_columns:
            return ErrorHandlers._400_error(f'Column: {column} is out of \
                range, board dimensions: columns: {game_data.game_columns} by \
                    rows: {game_data.game_rows}')

        column_data = Moves.query.filter_by(game_id=game_id).filter_by(
            move_column=column).order_by(asc(Moves.move_row)).first()
        if column_data is None:
            row = game_data.game_rows
        elif column_data.move_row == 1:
            return ErrorHandlers._400_error(f'Column: {column} is out of \
                range. This column has been filled')
        else:
            row = column_data.move_row - 1
        return row

    def _validate_game_state(self, game_id, player_id):

        # Generate board and move all of player's pieces to board
        # TODO: Write a more efficient function, only have to check
        # lastest move
        game_info = Games.query.get(game_id)
        board = [[0 for c in range(game_info.game_columns)]
                 for r in range(game_info.game_rows)]
        game_moves = Moves.query.filter_by(
                        game_id=game_id).filter_by(player_id=player_id).all()
        for move in game_moves:
            board[move.move_row - 1][move.move_column - 1] = 1

        piece_count = 0
        # Check horizontals
        for i in range(game_info.game_rows):
            piece_count = 0
            for j in range(game_info.game_columns):
                if board[i][j] == 1:
                    piece_count += 1
                if piece_count == 4:
                    game_info.winner = player_id
                    game_info.game_state = 'DONE'
                    db.session.commit()

        piece_count = 0
        # Check verticals
        for i in range(game_info.game_columns):
            piece_count = 0
            for j in range(game_info.game_rows):
                if board[j][i] == 1:
                    piece_count += 1
                if piece_count == 4:
                    game_info.winner = player_id
                    game_info.game_state = 'DONE'
                    db.session.commit()

        # Check both sets of diagnols
        for j in range(game_info.game_columns):
            for i in range(game_info.game_rows):
                try:
                    if board[i][j] == 1 and board[i-1][j-1] == 1 and board[i-2][j-2] == 1 and board[i-3][j-3] == 1:
                        game_info.winner = player_id
                        game_info.game_state = 'DONE'
                        db.session.commit()
                except IndexError:
                    pass

        for j in range(game_info.game_columns):
            for i in range(game_info.game_rows):
                try:
                    if board[i][j] == 1 and board[i+1][j+1] == 1 and board[i+2][j+2] == 1 and board[i+3][j+3] == 1:
                        game_info.winner = player_id
                        game_info.game_state = 'DONE'
                        db.session.commit()
                except IndexError:
                    pass

    def _validate_quit(self, game_id, player_id):
        game_data = Games.query.get(game_id)
        if game_data is None:
            return ErrorHandlers._404_error('Game not Found')

        if game_data.game_state == 'DONE':
            return ErrorHandlers._410_error(f'Game: {game_id} is already in \
                DONE state.')

        if not (player_id == player for
                player in (game_data.players).split(",")):
            return ErrorHandlers._404_error(f'Player: {player_id} \
                is not in this game.')

        if len(Moves.query.filter_by(game_id=game_id).filter_by(
                        player_id=player_id).filter_by(move_column=0).all()) > 0:
            return ErrorHandlers._404_error(f'Player: {player_id}, has already \
                ended this game')
