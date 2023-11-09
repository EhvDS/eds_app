let cols= 3;          // Number of columns in the Canvas
let rows= 3;          // Number of rows in the Canvas
let pieces= [];         // Array of pieces
let img;                       // Google Maps image of Eindhoven
let pieceWidth, pieceHeight;   // Width and height of each piece
let selectedPiece= null; // The piece that is currently selected
let offsetX= 0;       // Offset between the mouse and the piece
let offsetY= 0;       // Offset between the mouse and the piece

// Loading in the Google Maps image of Eindhoven
// Images is saved online to a URL at https://imgbb.com/
function preload() {
  img = loadImage('https://i.ibb.co/dKKvqCy/Schermafbeelding-2023-11-07-163853.png');
}

// Setup for the puzzle in P5.js
function setup() {
  createCanvas(1500, 1300);     // Canvas with the size of 1500 x 1300 pixels
  img.resize(width, height);    // Resize the image to fit the canvas
  pieceWidth = width / cols;    // Width of each piece
  pieceHeight = height / rows;  // Height of each piece

  // The image of Eindhoven is cut into pieces
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      let piece = img.get(x * pieceWidth, y * pieceHeight, pieceWidth, pieceHeight);

      // Each piece of the original image is added to the array with the information of the position
      pieces.push({
        image: piece,
        x: x * pieceWidth,
        y: y * pieceHeight,
        originalX: x * pieceWidth,
        originalY: y * pieceHeight,
        index: y * cols + x
      });
    }
  }

  // We need to shuffle the pieces before drawing them to the canvas
  shufflePieces();
}

// Function to draw the puzzle pieces to the canvas
function draw() {
  background(220); // Add a light-gray background to the canvas

  // Display the puzzle pieces on the canvas
  for (let i = 0; i < pieces.length; i++) {
    image(pieces[i].image, pieces[i].x, pieces[i].y, pieceWidth, pieceHeight);

    // To every piece I want to add a border
    stroke(200); // This is the light-gray color
    noFill();
    rect(pieces[i].x, pieces[i].y, pieceWidth, pieceHeight);
  }
}

// Function to select the puzzle pieces
function mousePressed() {
  // Check if the mouse is over any piece
  for (let i = 0; i < pieces.length; i++) {
    if (mouseX > pieces[i].x && mouseX < pieces[i].x + pieceWidth &&
        mouseY > pieces[i].y && mouseY < pieces[i].y + pieceHeight) {
      selectedPiece = pieces[i];
      offsetX = mouseX - selectedPiece.x;
      offsetY = mouseY - selectedPiece.y;
    }
  }
}

// Dragging the puzzle pieces
function mouseDragged() {
  // If a piece is selected, move it around using the mouse
  if (selectedPiece) {
    selectedPiece.x = mouseX - offsetX;
    selectedPiece.y = mouseY - offsetY;
  }
}

// Function to release the puzzle pieces
function mouseReleased() {
  // If a piece is selected, check if it is in the correct position
  if (selectedPiece) {
    let inPlace = false;

    // Check if the piece is in the correct position
    if (selectedPiece.x >= selectedPiece.originalX - pieceWidth / 2 &&
        selectedPiece.x <= selectedPiece.originalX + pieceWidth / 2 &&
        selectedPiece.y >= selectedPiece.originalY - pieceHeight / 2 &&
        selectedPiece.y <= selectedPiece.originalY + pieceHeight / 2) {
      selectedPiece.x = selectedPiece.originalX;
      selectedPiece.y = selectedPiece.originalY;
      inPlace = true;
    }

    // If the piece is in the correct position, the piece is set to null
    if (inPlace) {
      selectedPiece = null;
      // Check if the puzzle is solved with this new correct piece
      checkPuzzleSolved();
    } else {
      selectedPiece = null;
    }
  }
}

// Function to shuffle the puzzle pieces
function shufflePieces() {
  // Shuffle the puzzle pieces array
  for (let i = pieces.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pieces[i], pieces[j]] = [pieces[j], pieces[i]];
  }

  // Rearrange positions after shuffling
  let index = 0;
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      pieces[index].x = x * pieceWidth;
      pieces[index].y = y * pieceHeight;
      pieces[index].index = y * cols + x;
      index++;
    }
  }
}

// Function to check if the puzzle is solved
function checkPuzzleSolved() {
  let solved = true; // Assume the puzzle is solved at the beginning of the function
  for (let i = 0; i < pieces.length; i++) {
    // Check if the piece is not in the correct position, the puzzle is not solved
    if (pieces[i].x !== pieces[i].originalX || pieces[i].y !== pieces[i].originalY) {
      solved = false; // The puzzle solved is set back to false
      break;
    }
  }

  // If the puzzle is solved is true, the user gets a message
  if (solved) {
    alert("WOW!!!! YOU ARE REALLY GOOD!!!! YOU SOLVED THE EINDHOVEN NEIGHBORHOODS PUZZLE!");
  }
}