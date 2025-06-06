from colors import COLORS

# Define the shapes of the tetrominos
TETROMINO_SHAPES = {
    "I": [
        [".....",
         ".....",
         "IIII.",
         ".....",
         "....."],
        [".....",
         "..I..",
         "..I..",
         "..I..",
         "..I.."]
    ],
    "J": [
        [".....",
         ".J...",
         ".JJJ.",
         ".....",
         "....."],
        [".....",
         "..JJ.",
         "..J..",
         "..J..",
         "....."],
        [".....",
         ".....",
         ".JJJ.",
         "...J.",
         "....."],
        [".....",
         "..J..",
         "..J..",
         ".JJ..",
         "....."]
    ],
    "L": [
        [".....",
         "...L.",
         ".LLL.",
         ".....",
         "....."],
        [".....",
         "..L..",
         "..L..",
         "..LL.",
         "....."],
        [".....",
         ".....",
         ".LLL.",
         ".L...",
         "....."],
        [".....",
         ".LL..",
         "..L..",
         "..L..",
         "....."]
    ],
    "O": [
        [".....",
         ".....",
         ".OO..",
         ".OO..",
         "....."]
    ],
    "S": [
        [".....",
         ".....",
         "..SS.",
         ".SS..",
         "....."],
        [".....",
         "..S..",
         "..SS.",
         "...S.",
         "....."]
    ],
    "T": [
        [".....",
         "..T..",
         ".TTT.",
         ".....",
         "....."],
        [".....",
         "..T..",
         "..TT.",
         "..T..",
         "....."],
        [".....",
         ".....",
         ".TTT.",
         "..T..",
         "....."],
        [".....",
         "..T..",
         ".TT..",
         "..T..",
         "....."]
    ],
    "Z": [
        [".....",
         ".....",
         ".ZZ..",
         "..ZZ.",
         "....."],
        [".....",
         "...Z.",
         "..ZZ.",
         "..Z..",
         "....."]
    ]
}


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[shape]
        self.rotation = 0
        self.pattern = TETROMINO_SHAPES[shape]

    def rotate(self, clockwise=True):
        """Rotate the tetromino clockwise or counterclockwise."""
        dir = 1 if clockwise else -1
        self.rotation = (self.rotation + dir) % len(self.pattern)

    def get_shape(self):
        """Return the current rotation of the tetromino."""
        return self.pattern[self.rotation]

    def get_blocks(self):
        """Get the positions of blocks in the tetromino relative to its position."""
        blocks = []
        shape = self.get_shape()
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell != '.':
                    blocks.append((self.x + j, self.y + i))
        
        return blocks
