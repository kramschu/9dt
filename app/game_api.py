from flask import Blueprint, jsonify, request
from components.services import GameFunctions
from models import Games, Moves, Players, db

game_api = Blueprint("game_api", __name__)


@game_api.route('/view_data/<table_name>', methods=['GET'])
def view_table_data(table_name):
    """
    Displays desired table information

    :param table_name: table name
    :type table_name: string

    :return: Returns a dictionary with data object represented as
    a list of table row objects.
    """
    view_list = []
    if table_name == 'Games':
        games = Games.query.all()
        for row in games:
            view_object = {
             'game_id': row.game_id,
             'players': row.players,
             'columns': row.game_columns,
             'rows': row.game_rows,
             'game_state': row.game_state,
             'winner': row.winner
            }
            view_list.append(view_object)

    if table_name == 'Players':
        players = Players.query.all()
        for row in players:
            view_object = {
                'player_id': row.player_id,
                'player_name': row.player_name,
            }
            view_list.append(view_object)

    if table_name == 'Moves':
        moves = Moves.query.all()
        for row in moves:
            view_object = {
                'move_id': row.move_id,
                'move_column': row.move_column,
                'move_row': row.move_row,
                'game_id': row.game_id,
                'player_id': row.player_id
            }
            view_list.append(view_object)
    return jsonify({
                    'data': view_list
                    })


@game_api.route('/', methods=['GET'])
def in_progress_games():
    """
    Returns all in-progress games

    :return: Returns a dictionary with games object represented as
    a list of game ids.
    Example:
        { "games" : ["1", "2"] }
    """

    in_progress_games = GameFunctions()._get_in_progress_games()
    return in_progress_games


@game_api.route('/', methods=['POST'])
def create_game():
    """
    Creates a new game with designated players, columns, and rows.

    :param players: list of game players
    :type players: list of strings
    :param columns: number of columns in the game
    :type columns: integer
    :param rows: number of rows in the game
    :type rows: integer

    :return: Returns a dictionary with gameId represented by a string
    Example:
        { "gameId" : "1" }
    """

    data = request.get_json()
    players, columns, rows = data['players'],  data['columns'], data['rows']
    new_game = GameFunctions()._create_game(players, columns, rows)
    return new_game


@game_api.route('/<game_id>', methods=['GET'])
def get_game_state(game_id):
    """
    Displays Current state of game.

    :param game_id: game id for which game state will be displayed
    :type game_id: integer

    :return: Returns a dictionary containing players, state, and winner of
        game.
    Example:
        {
          "players" : ["player1", "player2"],
          "state": "DONE",
          "winner": "player1"
        }
    """
    game_state = GameFunctions()._get_game_state(game_id)
    return game_state


@game_api.route('/<game_id>/moves', methods=['GET'])
def get_moves(game_id):
    """
    Displays list of moves in a game.

    :param game_id: game id for which moves will be displayed
    :type game_id: integer

    :return: Returns a dictionary containing players, state, and winner of
        game.
    Example:
        {
        "moves": [{"type": "MOVE", "player": "player1",
        "column":1}, {"type": "QUIT", "player": "player2"}]
        }
    """
    game_moves = GameFunctions()._get_moves_list(game_id)
    return game_moves


@game_api.route('/<game_id>/<player_id>', methods=['POST'])
def move_player(game_id, player_id):
    """
    Posts a move to the given column.

    :param game_id: game id for which move will be posted
    :type game_id: integer
    :param player_id: player id for which move will be posted
    :type player_id: string
    :param column: column for which move will be posted
    :type column: integer

    :return: Returns a dictionary containing the game id and move number.
    Example:
        {
        "move": "{gameId}/moves/{move_number}"
        }
    """
    data = request.get_json()
    move_number = GameFunctions()._move_player(
        game_id, player_id, data['column'])
    return move_number


@game_api.route('/<game_id>/moves/<move_number>', methods=['GET'])
def get_move(game_id, move_number):
    """
    Displays move information from designated game and move number

    :param game_id: game id for which move will be displayed
    :type game_id: integer
    :param move_number: move_number for which move will be displayed
    :type move_number: integer

    :return: Returns a dictionary containing the type, player, and column of
        designated move.
    Example:
        {
        "type" : "MOVE",
        "player": "player1",
        "column": 2
        }
    """
    move = GameFunctions()._get_move(game_id, move_number)
    return move


@game_api.route('/<game_id>/<player_id>', methods=['DELETE'])
def quit_game(game_id, player_id):
    """
    Return all in-progress games or create a new game.
    """
    quit_status = GameFunctions()._quit_game(game_id, player_id)
    return quit_status
