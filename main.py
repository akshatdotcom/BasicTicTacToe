from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS  # what is this?
from flask_socketio import SocketIO, emit, send 


app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = '4504617834314490345'
socketio = SocketIO(app)

serverBoard= [
  ['', '', ''],
  ['', '', ''],
  ['', '', '']
]

players = dict() 
temp = map(str, list("XOXOXOXOXOXOXOXOXOXOXO"))
isX=True 


@app.route('/', methods=['GET', 'POST'])
def index():
  print('oof')
  return render_template('index.html')


@socketio.on('connect')
def handle_client_connected_event():
  print(request.sid, 'oof')
  players[request.sid] = next(temp) 
  #send('you\'re {0}'.format(next(temp)), broadcast=True)
  # emit('debug', {'data': 'Connected'})


# remember to de the player checking
# this does not need the socketio decorator
def is_move_valid(move, player):
  if serverBoard[move[0]][move[1]] != '':
    return False
  else:
    if isX:
      xOrCircle = "X"
    else:
      xOrCircle = "O"
    serverBoard[move[0]][move[1]] = xOrCircle
    return True

# the to() I saw on something in JS but I think it should work in python as well
def error_signal(player):
  socketio.emit('invalid move')

# should be a boolean in front end, should be boolean = not boolean to toggle: why does it need to be in the front end? 
def lock_unlock(player):
  socketio.emit('toggle')

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
    win_condition()
    # lock_unlock(player)
  else:
    # should prompt for another move
    print('rejected', move)
    # error_signal(player)
  print(serverBoard)
  

def win_condition():
  win = False

  # check for win
  if win:
    print('end')
    socketio.send('end')

if __name__ == '__main__': 
  socketio.run(app, debug=True, host='127.0.0.1', port=5000)


# def game_has_ended():
#     board = serverBoard
#     for i in range(3):
#         if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != " ":
#             print(board[0][i], "wins vertically")
#             return True
#     for i in range(3):
#         if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != " ":
#             print(board[i][0], "wins horizontally!")
#             return True

#     diag1 = False
#     diag2 = False

#     if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
#         diag1 = True

#     if board[2][0] == board[1][1] and board[1][1] == board[0][2]:
#         diag2 = True

#     if board[1][1] == " ":
#         diag1 = False
#         diag2 = False

#     if diag1 or diag2:
#         print(board[1][1], "wins diagonally!")
#         return True

#     tie = True
#     for i in board:
#         for b in i:
#             if b == " ":
#                 tie = False
#                 break
#     if tie:
#         print("It is a tie!")
#         return True

#     return False
