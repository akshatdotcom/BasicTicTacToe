from flask import Flask, render_template, request, url_for
from flask_cors import CORS 
from flask_socketio import SocketIO, emit, send


app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = '4504617834314490345'
socketio = SocketIO(app)

serverBoard = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]

players = dict()
temp = map(str, list("XOXOXOXOXOXOXOXOXOXOXO"))
isX = True
unlocked = False


@app.route('/', methods=['GET', 'POST'])
def index():
    print('oof')
    return render_template('index.html')


@socketio.on('connect')
def handle_client_connected_event():
    global unlocked
    print(request.sid, 'oof')
    unlocked = not unlocked
    players[request.sid] = unlocked


# remember to de the player checking
# this does not need the socketio decorator
def is_move_valid(move, player):
    if players[player]:
        if serverBoard[move[0]][move[1]] != '':
            return False
        else:
            if isX:
                xOrCircle = "X"
            else:
                xOrCircle = "O"
            serverBoard[move[0]][move[1]] = xOrCircle
            return True
    else:
        print('you\'re locked')
        return False



# def error_signal(player):
#     socketio.emit('invalid move')


def lock_unlock():
    print(players)
    for i in players.keys():
      players[i] = not players[i]

# the move signal happens when a client clicks on a square
# needs to be rendered into a gui, move should be an array size 2

@socketio.on('move')
def move_judge(move):
    global isX
    # replace none with the player
    player = request.sid
    print('move request received from', players[player])
    move = list(move)
    print(move)
    isX = not isX

    if is_move_valid(move, player):
        # this should broadcast to all automatically
        print('approved', move)
        socketio.emit('board', serverBoard)
        lock_unlock()
    else:
        # should prompt for another move
        print('rejected', move)
        # error_signal(player)
    print(serverBoard)


if __name__ == '__main__':
    serverBoard = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ]
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
