class CoordinateConstants:
    START_COL = 8
    START_ROW = 4


class DrunkenBishopGenerator:
    def __init__(self):
        # "S" and "E" reserved for start and end points
        self.freq_to_val = {
            0: "",
            1: ".",
            2: "o",
            3: "+",
            4: "=",
            5: "*",
            6: "B",
            7: "O",
            8: "X",
            9: "@",
            10: "%",
            11: "&",
            12: "#",
            13: "/",
            14: "^",
            15: "S",
            16: "E",
        }
        self.num_col = 17
        self.num_row = 9
        self.curr_col = CoordinateConstants.START_COL
        self.curr_row = CoordinateConstants.START_ROW
        self.board = [[0] * self.num_col for _ in range(self.num_row)]

    def moveUpLeft(self):
        if self.curr_col > 0:
            self.curr_col -= 1
        if self.curr_row > 0:
            self.curr_row -= 1

    def moveUpRight(self):
        if self.curr_col < self.num_col - 1:
            self.curr_col += 1
        if self.curr_row > 0:
            self.curr_row -= 1

    def moveDownLeft(self):
        if self.curr_col > 0:
            self.curr_col -= 1
        if self.curr_row < self.num_row - 1:
            self.curr_row += 1

    def moveDownRight(self):
        if self.curr_col < self.num_col - 1:
            self.curr_col += 1
        if self.curr_row < self.num_row - 1:
            self.curr_row += 1

    def generateAscii(self, fingerprint):
        # TODO: Ensure fingerprint is valid hexidecimal format

        # Parse fingerprint to bytes
        fp_bytes = fingerprint.split(":")
        for fp_byte in fp_bytes:
            # Convert from hex to binary
            bits = bin(int(fp_byte, 16))[2:].zfill(8)
            # Convert pair bits to steps
            for i in range(len(bits), 1, -2):
                step = bits[i - 2 : i]
                if step == "00":
                    self.moveUpLeft()
                elif step == "01":
                    self.moveUpRight()
                elif step == "10":
                    self.moveDownLeft()
                elif step == "11":
                    self.moveDownRight()
                else:
                    raise ValueError(
                        "Value of {fp_byte} is invalid".format(fp_byte=fp_byte)
                    )

                # Increment visited new position
                self.board[self.curr_row][self.curr_col] += 1

        ascii_board = self.readBoard(
            CoordinateConstants.START_COL,
            CoordinateConstants.START_ROW,
            self.curr_col,
            self.curr_row,
        )
        self.prettyPrint(fingerprint, ascii_board)
        self.resetBoard()

    def readBoard(self, start_x, start_y, end_x, end_y):
        ascii_board = [[""] * self.num_col for _ in range(self.num_row)]
        for i in range(0, self.num_row):
            for j in range(0, self.num_col):
                ascii_board[i][j] = self.freq_to_val[self.board[i][j]]

        # Mark beginning and end points
        ascii_board[start_y][start_x] = "S"
        ascii_board[end_y][end_x] = "E"
        return "\n".join(
            ["".join(["{:4}".format(item) for item in row]) for row in ascii_board]
        )

    def resetBoard(self):
        self.board = [[0] * self.num_col for _ in range(self.num_row)]
        self.curr_col = CoordinateConstants.START_COL
        self.curr_row = CoordinateConstants.START_ROW

    def prettyPrint(self, fingerprint, ascii_board):
        res = "Fingerprint:\n{fingerprint}\n{ascii}".format(
            fingerprint=fingerprint, ascii=ascii_board
        )
        print(res)


"""
TODOs:
- Validate fingerprint input
- Parse CLI args
- Write 'random' function
- Add function signatures
"""


def main():
    test_fp = "37:e4:6a:2d:48:38:1a:0a:f3:72:6d:d9:17:6b:bd:5e"
    generator = DrunkenBishopGenerator()
    generator.generateAscii(test_fp)


if __name__ == "__main__":
    main()
