var socket = io.connect();

const X_CLASS = "x";
const CIRCLE_CLASS = "circle";

const WINNING_COMBINATIONS = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

const cellElements = document.querySelectorAll("[data-cell]");
const board = document.getElementById("board");
const winningMessageElement = document.getElementById("winningMessage");
const restartButton = document.getElementById("restartButton");
const winningMessageTextElement = document.querySelector(
  "[data-winning-message-text]"
);
let circleTurn;

startGame();

restartButton.addEventListener("click", startGame);

console.log("script.js is running");
//document.domain+':'+ Location.port);
socket.emit("connect");
//socket.on('connect', function() {
//socket.emit('client_connected',{data:'user has connected'});
// console.log('CONNECTED');
// });

socket.on("debug", (d) => {
  console.log(d);
});

// update the board
socket.on("board", function (receivedBoard) {
    if(receivedBoard == null) {
        console.log("received board is null");
    }
  console.log("received board");
  console.log(receivedBoard);
  render(receivedBoard);
});

function render(boardToRender) {
  for(let row = 0; row < 3; row++) {
    for(let col = 0; col < 3; col++) {
      cell = $(`.cell:nth-child(${row * 3 + col + 1})`)
      // console.log(`R ${row} C ${col}`)
    if (boardToRender[row][col] != null) {
      if (boardToRender[row][col] === "X") {
        cell.addClass(X_CLASS);
      } else if (boardToRender[row][col] === "O") {
        cell.addClass(CIRCLE_CLASS);
      }
      
    }
  }
  }
  // [...cellElements].forEach(function (cell) {
  //   console.log(`R ${rowValue} C ${columnValue}`)
  //   if (boardToRender[rowValue][columnValue] != null) {
  //     if (boardToRender[rowValue][columnValue] === "X") {
  //       cell.classList.add(X_CLASS);
  //     } else if (boardToRender[rowValue][columnValue] === "O") {
  //       cell.classList.add(CIRCLE_CLASS);
  //     }
  //   }
  //   rowValue++;
  //   columnValue++;
  //   if (columnValue == 3) {
  //     columnValue = 0;
  //   }
  // });
}

function startGame() {
  circleTurn = false;
  cellElements.forEach((cell) => {
    cell.classList.remove(X_CLASS);
    cell.classList.remove(CIRCLE_CLASS);
    cell.removeEventListener("click", handleClick);
    cell.addEventListener("click", handleClick, { once: true });
  });
  setBoardHoverClass();
  winningMessageElement.classList.remove("show");
}

function handleClick(e) {
  const cell = e.target;
  const currentClass = circleTurn ? CIRCLE_CLASS : X_CLASS;
  placeMark(cell, currentClass);
  if (checkWin(currentClass)) {
    endGame(false);
  } else if (isDraw()) {
    endGame(true);
  } else {
    swapTurns();
    setBoardHoverClass();
  }
  // placeMark
  // Check for Win
  // Check for Draw
  // Switch Turns
}

function isDraw() {
  return [...cellElements].every((cell) => {
    return (
      cell.classList.contains(X_CLASS) || cell.classList.contains(CIRCLE_CLASS)
    );
  });
}

function endGame(draw) {
  if (draw) {
    winningMessageTextElement.innerText = "Draw!";
  } else {
    winningMessageTextElement.innerText = `${circleTurn ? "O's" : "X's"} Wins!`;
  }
  winningMessageElement.classList.add("show");
}

function placeMark(cell, currentClass) {
  let cellXValue = parseInt(cell.getAttribute("data-cell-x"));
  let cellYValue = parseInt(cell.getAttribute("data-cell-y"));
  console.log(cellYValue, cellXValue);
  socket.emit("move", [cellYValue, cellXValue]);
  // cell.classList.add(currentClass);
}

function swapTurns() {
  circleTurn = !circleTurn;
}

function setBoardHoverClass() {
  board.classList.remove(X_CLASS);
  board.classList.remove(CIRCLE_CLASS);
  board.classList.add(circleTurn ? CIRCLE_CLASS : X_CLASS);
}

// function checkWin(currentClass) {
//   return WINNING_COMBINATIONS.some((combination) => {
//     return combination.every((index) => {
//       return cellElements[index].classList.contains(currentClass);
//     });
//   });
// }
