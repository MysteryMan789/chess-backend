from flask import Flask, jsonify, request
import chess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
board = chess.Board()

@app.route('/validate_move', methods=['POST'])
def validate_move():
    data = request.get_json()
    move_str = data.get('move')
    if not move_str:
        return jsonify({'error': 'No move provided'}), 400
    try:
        move = chess.Move.from_uci(move_str)
    except ValueError:
        return jsonify({'error': 'Invalid move format'}), 400
    if move in list(board.legal_moves) and move in board.legal_moves:
        board.push(move) 
        san = board.san(move)
        return jsonify({
            'new_board': board.fen(),
            'san':san
        })
    else:
        return jsonify({'error': 'Illegal move'}), 400
@app.route('/reset', methods=['POST'])
def reset_board():
    board.reset()
    return jsonify({'new_board': board.fen()})
@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({'board': board.fen()})
@app.route('/legal_moves', methods=['POST'])
def legal_moves():
    data = request.get_json()
    square = data.get('square')
    if not square:
        return jsonify({'error': 'No square provided'}), 400

    moves = [
        move.uci()[2:4]
        for move in board.legal_moves
        if move.uci().startswith(square)
    ]
    return jsonify({'moves': moves})
if __name__ == '__main__':
    app.run(debug=True)
