import os
from glob import glob
import pygame
import random
import Puzzle_GUI


class Puzzle:
    def __init__(self, pieces):
        self.width = pieces[0]
        self.height = pieces[1]
        self.grid = [[None for row in range(self.height)]
                     for _ in range(self.width)]
        self.stores = {'box': Store('Box')}
        self.image_folder = os.path.dirname(os.path.abspath(__file__))
        self.availableImageList = glob('*.jpg') + glob('*.png')
        self.image_name = self.availableImageList[0]
        self.image = pygame.image.load(open(
            f'{self.image_folder}/{self.image_name}'))

    def __str__(self):
        ans = ''
        for row in range(self.height):
            ans += str(self.grid[row])
            ans += '\n'
        return ans

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def update_width(self, new_width):
        self.width = int(new_width)

    def update_height(self, new_height):
        self.height = int(new_height)

    def rotate_image_90CW(self):
        self.image = pygame.transform.rotate(self.image, 90)

    # def update_image_loc(self, new_image_loc):
    #     self.image_folder = Path(new_image_loc)

    def update_image_name(self, new_image_name):
        self.image_name = new_image_name
        file = f'{self.image_folder}/{self.image_name}'
        if os.path.exists(file):
            self.image = pygame.image.load(open(file))
            return 'exists'
        else:
            return 'n_exists'

    # returns tuple image (width, height)
    def get_image_size(self):
        return self.image.get_size()

    def get_a_store(self, store_key):
        return self.stores[store_key]

    def create_piece(self, solved_location, image):
        piece = Piece(solved_location, image)
        self.stores['box'].add_piece(piece)

    def move_piece(self, tile_index, destination):
        # tile in store
        if type(tile_index) == int:
            piece = self.get_a_store('box').get_contents().pop(tile_index)
            piece.update_location(destination)
            self.grid[destination[0]][destination[1]] = piece
        # tile in puzzle
        else:
            if type(destination) == tuple:
                piece = self.grid[tile_index[0]][tile_index[1]]
                piece.update_location(destination)
                self.grid[destination[0]][destination[1]] = piece
            # sending piece back to store
            else:
                piece = self.grid[tile_index[0]][tile_index[1]]
                piece.update_location(None)
                self.get_a_store('box').add_piece(
                    self.grid[tile_index[0]][tile_index[1]], -1)
            self.grid[tile_index[0]][tile_index[1]] = None

    # empties grid and store
    def restart(self):
        self.grid = [
            [None for row in range(self.height)]
            for col in range(self.width)]
        self.get_a_store('box').empty_store()

    def check_game_state(self):
        for col in range(self.width):
            for row in range(self.height):
                piece = self.grid[col][row]
                if piece.get_current_location() != piece.get_solved_location():
                    return False
        return True


class Store:
    def __init__(self, name):
        self.name = str(name)
        self.contents = []

    def __str__(self):
        ans = ''
        for pieces in self.contents:
            ans += str(pieces.get_value()) + ' '
        return str(self.name) + (' contains pieces: ') + ans

    def get_contents(self):
        return self.contents

    def shuffle_store(self):
        random.shuffle(self.contents)

    def add_piece(self, piece, insert_location=-1):
        if piece.solved_location != 0:
            self.contents.insert(insert_location, piece)
        else:
            self.contents.append(piece)

    def remove_piece(self, piece):
        self.contents.pop(piece)

    def empty_store(self):
        self.contents = []


class Piece:
    def __init__(self, solved_location, image, current_location=None):
        self.solved_location = solved_location
        self.image = image
        self.current_location = current_location

    def __str__(self):
        return ('piece: ') + str(self.value)

    def get_solved_location(self):
        return self.solved_location

    def get_current_location(self):
        return self.current_location

    def get_image(self):
        return self.image

    def update_location(self, new_location):
        self.current_location = new_location


def run_game(window_dimensions, number_pieces):
    puzzle = Puzzle(number_pieces)
    Puzzle_GUI.start_game(window_dimensions, puzzle)


if __name__ == '__main__':
    # X x Y
    default_window = width, height = 1200, 800
    default_pieces = (4, 4)
    run_game(default_window, default_pieces)
