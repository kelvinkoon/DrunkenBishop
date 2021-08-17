import argparse
import os
import binascii
from typing import List


class Constants:
    START_COL = 8
    START_ROW = 4
    NUM_HEX_BYTES = 16


class DrunkenBishopGenerator:
    def __init__(self):
        # "S" and "E" reserved for start and end points
        self.freq_to_val = {
            0: " ",
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
        self.curr_col = Constants.START_COL
        self.curr_row = Constants.START_ROW
        self.board = [[0] * self.num_col for _ in range(self.num_row)]

    def moveUpLeft(self):
        """
        Move current position up and left
        """
        if self.curr_col > 0:
            self.curr_col -= 1
        if self.curr_row > 0:
            self.curr_row -= 1

    def moveUpRight(self):
        """
        Move current position up and right
        """
        if self.curr_col < self.num_col - 1:
            self.curr_col += 1
        if self.curr_row > 0:
            self.curr_row -= 1

    def moveDownLeft(self):
        """
        Move current position down and left
        """
        if self.curr_col > 0:
            self.curr_col -= 1
        if self.curr_row < self.num_row - 1:
            self.curr_row += 1

    def moveDownRight(self):
        """
        Move current position down and right
        """
        if self.curr_col < self.num_col - 1:
            self.curr_col += 1
        if self.curr_row < self.num_row - 1:
            self.curr_row += 1

    def generateAscii(self, fingerprint: str, random: bool = False):
        """
        Generate ASCII representation
        If random is True, generate a random key
        """
        if random:
            fingerprint = self.generateRandomKey()

        # Validate byte string format
        if len(fingerprint.split(":")) != Constants.NUM_HEX_BYTES:
            raise ValueError("Hexidecimal byte string should have 16 octets.")

        # Parse fingerprint to bytes
        fp_bytes = fingerprint.split(":")
        for fp_byte in fp_bytes:
            # Convert from hex to binary
            bits = bin(int(fp_byte, 16))[2:].zfill(8)
            # Convert pair bits to steps from LSB
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
            Constants.START_COL,
            Constants.START_ROW,
            self.curr_col,
            self.curr_row,
        )
        self.prettyPrint(fingerprint, ascii_board)
        self.resetBoard()

    def readBoard(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """
        Convert board to characters based on frequency of visits
        Start and end points reserved for "S" and "E"
        """
        ascii_board = [[""] * self.num_col for _ in range(self.num_row)]
        for i in range(0, self.num_row):
            for j in range(0, self.num_col):
                ascii_board[i][j] = self.freq_to_val[self.board[i][j]]

        # Mark beginning and end points
        ascii_board[start_y][start_x] = "S"
        ascii_board[end_y][end_x] = "E"

        return self.formatBoard(ascii_board)

    def formatBoard(self, ascii_board: List[str]):
        """
        Add bordering for ASCII board
        """
        formatted_board = "+" + "-" * (self.num_col) + "+\n"
        for ascii_row in ascii_board:
            formatted_board += "|" + "".join(ascii_row) + "|\n"
        formatted_board += "+" + "-" * (self.num_col) + "+\n"
        return formatted_board

    def resetBoard(self):
        """
        Reset frequency and position of board 
        """
        self.board = [[0] * self.num_col for _ in range(self.num_row)]
        self.curr_col = Constants.START_COL
        self.curr_row = Constants.START_ROW

    def prettyPrint(self, fingerprint, ascii_board):
        """
        Format print statement for user 
        """
        res = "Fingerprint:\n{fingerprint}\n{ascii}".format(
            fingerprint=fingerprint, ascii=ascii_board
        )
        print(res)

    def generateRandomKey(self):
        """
        Generate a random 16 octet key 
        """
        random_bytes = []
        for _ in range(0, Constants.NUM_HEX_BYTES):
            random_bytes.append(binascii.b2a_hex(os.urandom(1)).decode("utf-8"))
        return ":".join(random_bytes)

def initializeParser():
    """
    Initialize parser arguments 
    """
    parser = argparse.ArgumentParser(description="Convert a key to ASCII representation via Drunken Bishop algorithm.")
    parser.add_argument(
        "-k",
        "--key",
        metavar="key",
        nargs="?",
        const="",
        type=str,
        help="16 octet byte string",
    )
    parser.add_argument(
        "-r",
        "--random",
        help="generate random key for ASCII representation",
        action="store_true",
    )
    return parser

def main():
    parser = initializeParser()
    args = parser.parse_args()

    generator = DrunkenBishopGenerator()
    generator.generateAscii(args.key, args.random)


if __name__ == "__main__":
    main()
