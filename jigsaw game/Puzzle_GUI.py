import pygame
import pygame_gui
import math

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (120, 120, 120)

FONT = pygame.font.Font(None, 20)
FONT_LABELS = pygame.font.Font(None, 20)
FONT_WIN = pygame.font.Font(None, 48)

BORDER = 30
BORDER_STORE = 10


def calc_puzzle_size(image_size, available_size):
    scale = max(image_size[0] / available_size[0],
                image_size[1] / available_size[1])
    return (int(image_size[0]/scale), int(image_size[1]/scale))


# get tile index, either in store or puzzle
def get_tile_at_location(location, gui):
    # right hand side: store
    if location[0] > gui.window_size[0]/2:
        if (
            location[1] > gui.store_loc[1]
            and location[1] <= (
                gui.store_loc[1]
                + (math.ceil(len(
                    gui._puzzle.get_a_store('box').get_contents())
                    / gui.store_pieces_per_row))
                * (gui.piece_size[1] + BORDER_STORE))
            and location[0] > gui.store_loc[0]
            and location[0] <= (
                gui.store_loc[0]
                + (gui.store_pieces_per_row *
                    (gui.piece_size[0] + BORDER_STORE)))
        ):
            x = int((location[0] - gui.store_loc[0])
                    / (gui.piece_size[0] + BORDER_STORE))
            y = int((location[1] - gui.store_loc[1])
                    / (gui.piece_size[1] + BORDER_STORE))
            tile_index = x + y * gui.store_pieces_per_row
            upper_left = location_of_tile(tile_index, gui)
            if (
                (upper_left[0] + gui.piece_size[0]) >= location[0]
                and (upper_left[1] + gui.piece_size[1]) >= location[1]
            ):
                if is_there_piece_here(tile_index, gui):
                    return tile_index
        return None
    # left hand side: puzzle
    else:
        if (
            location[1] > gui.grid_nodes[0][0][1]
            and location[1] <= gui.grid_nodes[-1][-1][1]
            and location[0] > gui.grid_nodes[0][0][0]
            and location[0] <= gui.grid_nodes[-1][-1][0]
        ):
            col = int((location[0] - gui.puzzle_loc[0]) / gui.piece_size[0])
            row = int((location[1] - gui.puzzle_loc[1]) / gui.piece_size[1])
            return (col, row)
        return None


# returns upper left corner of piece
def location_of_tile(tile_index, gui):
    # tile in store
    if type(tile_index) == int:
        x = (int(gui.window_size[0]/2 + BORDER)
             + (gui.piece_size[0] + BORDER_STORE)
             * (tile_index % gui.store_pieces_per_row))
        y = (BORDER +
             (gui.piece_size[1] + BORDER_STORE)
             * (tile_index//gui.store_pieces_per_row))
    # tile in puzzle
    else:
        x = gui.puzzle_loc[0] + gui.piece_size[0] * tile_index[0]
        y = gui.puzzle_loc[1] + gui.piece_size[1] * tile_index[1]
    return (x, y)


def is_there_piece_here(tile_index, gui):
    # tile in store
    if type(tile_index) == int:
        if tile_index < len(gui._puzzle.get_a_store('box').get_contents()):
            return True
        return False
    # tile in puzzle
    else:
        if gui._puzzle.grid[tile_index[0]][tile_index[1]]:
            return True
        return False


class GUI:
    def __init__(self, window_size, puzzle):
        self.window_size = window_size
        self.window_surface = pygame.display.set_mode((window_size))
        self.background = pygame.Surface((window_size))
        self.background.fill(white)

        self.start(window_size, puzzle)

        self.manager = pygame_gui.UIManager((window_size))
        # start and quit buttons
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (BORDER, window_size[1] - 50 - BORDER),
                (100, 32)),
            text='Start game', manager=self.manager)
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (BORDER + 120, window_size[1] - 50 - BORDER),
                (100, 32)),
            text='Quit game', manager=self.manager)
        # rotate image
        self.rotate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (BORDER + 400, 101 - BORDER),
                (120, 32)),
            text='Rotate image', manager=self.manager)
        # image file dropdown menu
        self.imageDropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self._puzzle.availableImageList,
            starting_option=self._puzzle.availableImageList[0],
            # self.image_name
            relative_rect=pygame.Rect(
                (BORDER + 110, 101 - BORDER),
                (270, 32)),
            manager=self.manager)

        text_puzzle_size_x = FONT_LABELS.render(
            'Enter number of pieces across (2-12):', True, black)
        text_puzzle_size_y = FONT_LABELS.render(
            'Enter number of pieces down (2-12):', True, black)
        text_puzzle_pieces = FONT_LABELS.render(
            'Number of pieces in puzzle: ' + str(self._rows*self._cols),
            True, black)
        text_current_image = FONT_LABELS.render(
            'Available images at script folder location:', True, black)
        text_image_loc = FONT_LABELS.render(
            str(self._puzzle.image_folder), True, black)
        # text_update_image_loc = FONT_LABELS.render(
        #     'Enter new image file location:', True, black)
        # text_current_image_name = FONT_LABELS.render(
        #     'Current image file name: ' + str(self._puzzle.image_name),
        #     True, black)
        text_choose_image = FONT_LABELS.render(
            'Select an image:', True, black)
        text_win_message = FONT_WIN.render(
            'You solved it, nice work!', True, black)
        text_invalid_input = FONT_LABELS.render(
            'Invalid file name/location, please try again', True, black)

        self.text_surfaces = [
            text_puzzle_size_x,
            text_puzzle_size_y,
            text_puzzle_pieces,
            text_current_image,
            text_image_loc,
            # text_update_image_loc,
            # text_current_image_name,
            text_choose_image,
            text_win_message,
            text_invalid_input
        ]

        self.start_game_button()

    def start(self, window_size, puzzle):
        self._puzzle = puzzle
        self._rows = puzzle.get_height()
        self._cols = puzzle.get_width()
        self.game_started = False
        self.win = False
        self.image_original = puzzle.image
        self.image_size = self.image_original.get_size()

        self.window_puzzle_size = (int(self.window_size[0]/2 - 2 * BORDER),
                                   int(self.window_size[1] - 8 * BORDER))
        self.puzzle_size = calc_puzzle_size(self._puzzle.get_image_size(),
                                            self.window_puzzle_size)
        self.puzzle_loc = (int(self.window_size[0]/4 - self.puzzle_size[0]/2),
                           int(self.window_size[1]/2 - self.puzzle_size[1]/2))
        self.store_loc = (int(self.window_size[0]/2 + BORDER), BORDER)
        self.image_scaled = pygame.transform.scale(self.image_original,
                                                   self.puzzle_size)
        self.piece_size = (int(self.puzzle_size[0]/self._cols),
                           int(self.puzzle_size[1]/self._rows))
        self.grid_nodes = [[(self.puzzle_loc[0] + self.piece_size[0]*col,
                             self.puzzle_loc[1] + self.piece_size[1]*row) for
                            row in range(self._rows + 1)] for
                           col in range(self._cols + 1)]

        self.store_pieces_per_row = int((self.window_size[0]/2 - 2*BORDER) /
                                        (self.piece_size[0] + BORDER_STORE))

        self.tile_selected = False
        self.tile_index = None
        self.tile_loc = None
        self.destination = None
        self.invalid_input = False

        puzzle_size_input_x = InputBox(
            self._puzzle.update_width,
            window_size[0]//2 - BORDER - 30,
            window_size[1] - BORDER - 70, 30, 20)
        puzzle_size_input_y = InputBox(
            self._puzzle.update_height,
            window_size[0]//2 - BORDER - 30,
            window_size[1] - BORDER - 40, 30, 20)
        # puzzle_image_name_input = InputBox(self._puzzle.update_image_name,
        #                                    BORDER + 185, BORDER + 70, 60, 20)
        # puzzle_image_loc_input = InputBox(self._puzzle.update_image_loc,
        #                                   BORDER + 190, BORDER + 20, 60, 20)

        self.update_buttons = [puzzle_size_input_x,
                               puzzle_size_input_y,
                               # puzzle_image_name_input,
                               # puzzle_image_loc_input,
                               ]

    def draw(self):
        self.window_surface.blit(self.background, (0, 0))
        # vertical line dividing store and puzzle
        pygame.draw.lines(self.window_surface, black, False,
                          ((self.window_surface.get_size()[0]//2, BORDER),
                           (self.window_surface.get_size()[0]//2,
                            self.window_surface.get_size()[1] - BORDER)),
                          5)
        # text labels
        # no. cols
        self.window_surface.blit(self.text_surfaces[0],
                                 (self.window_size[0]//2 - BORDER - 270,
                                  self.window_size[1] - BORDER - 65))
        # no. rows
        self.window_surface.blit(self.text_surfaces[1],
                                 (self.window_size[0]//2 - BORDER - 265,
                                  self.window_size[1] - BORDER - 35))
        # total pieces
        self.window_surface.blit(self.text_surfaces[2],
                                 (self.window_size[0]//2 - BORDER - 190,
                                  self.window_size[1] - BORDER - 10))
        # current image file text
        self.window_surface.blit(self.text_surfaces[3], (BORDER, BORDER))
        # image file path
        self.window_surface.blit(self.text_surfaces[4], (BORDER, BORDER + 25))
        # select an image instruction
        self.window_surface.blit(self.text_surfaces[5], (BORDER, BORDER + 50))
        # win message
        if self.win:
            self.window_surface.blit(self.text_surfaces[6],
                                     (self.window_size[0]//2 + BORDER + 50,
                                      self.window_size[1]//2))
        # invalid input
        if self.invalid_input:
            self.window_surface.blit(self.text_surfaces[7],
                                     (BORDER + 150, BORDER + 120))
        # update fields
        for button in self.update_buttons:
            button.draw(self.window_surface)
        # puzzle grid lines
        # rows
        for row in range(self._rows + 1):
            pygame.draw.lines(self.window_surface, black, False,
                              (self.grid_nodes[0][row],
                               self.grid_nodes[-1][row]), 1)
        # cols
        for col in range(self._cols + 1):
            pygame.draw.lines(self.window_surface, black, False,
                              (self.grid_nodes[col][0],
                               self.grid_nodes[col][-1]), 1)
        # pieces in puzzle
        if self.game_started:
            for row in range(self._rows):
                for col in range(self._cols):
                    if self._puzzle.grid[col][row] is not None:
                        self.window_surface.blit(
                            self._puzzle.grid[col][row].get_image(),
                            self.grid_nodes[col][row])
        # pieces in store
        if self.game_started:
            for idx, piece in enumerate(
                self._puzzle.get_a_store('box').get_contents()
            ):
                self.window_surface.blit(piece.get_image(),
                                         (int(self.window_size[0]/2 + BORDER)
                                         + (self.piece_size[0] + BORDER_STORE)
                                         * (idx % self.store_pieces_per_row),
                                          BORDER + (self.piece_size[1]
                                          + BORDER_STORE)
                                          * (idx
                                          // self.store_pieces_per_row)))
        # draw blue rectangle to highlight selected piece
        if self.tile_selected:
            pygame.draw.rect(self.window_surface, blue,
                             (
                                 self.tile_loc[0],
                                 self.tile_loc[1],
                                 self.piece_size[0],
                                 self.piece_size[1]),
                             3)
        # start and quit ui buttons
        self.manager.draw_ui(self.window_surface)
        pygame.display.update()

    def start_game_button(self):
        self.restart()
        self.game_started = True
        for row in range(self._rows):
            for col in range(self._cols):
                image = pygame.transform.chop(
                    pygame.transform.chop(
                        self.image_scaled,
                        (0, 0, self.piece_size[0] * col,
                            self.piece_size[1] * row)),
                        (self.piece_size[0],
                            self.piece_size[1], 1000, 2000))
                self._puzzle.create_piece((col, row), image)
        self._puzzle.get_a_store('box').shuffle_store()
        # used for returning pieces to the store
        blank_piece = pygame.Surface(self.piece_size)
        blank_piece.fill(grey)
        self._puzzle.create_piece(0, blank_piece)

    def button_handler(self, event):
        # create all pieces, put them in box store, randomise order
        if event.ui_element == self.start_button:
            self.start_game_button()
        if event.ui_element == self.quit_button:
            pygame.quit()
            exit()
        if event.ui_element == self.rotate_button:
            self._puzzle.rotate_image_90CW()
            self.start_game_button()

    def mouse_handler(self, event):
        click_pos = pygame.mouse.get_pos()
        for button in self.update_buttons:
            button.clicked_input(click_pos)
        if self.game_started:
            if self.tile_selected is False:
                self.tile_index = get_tile_at_location(click_pos, self)
                if self.tile_index == len(
                    self._puzzle.get_a_store('box').get_contents()
                ) - 1:
                    self.tile_index = None
                elif (type(self.tile_index) == int or
                        type(self.tile_index) == tuple):
                    if (type(self.tile_index) == int
                        or (type(self.tile_index) == tuple
                            and is_there_piece_here(self.tile_index, self))):
                        self.tile_loc = location_of_tile(self.tile_index, self)
                        self.tile_selected = True
            # tile currently selected
            else:
                # click in store
                if click_pos[0] > self.window_size[0]/2:
                    # check if in bounds
                    if type(get_tile_at_location(click_pos, self)) == int:
                        # check for the blank piece
                        if get_tile_at_location(click_pos, self) ==\
                            len(self._puzzle.get_a_store('box')
                                .get_contents()) - 1:
                            # current selection is in puzzle, return to store
                            if type(self.tile_index) == tuple:
                                self._puzzle.move_piece(self.tile_index, None)
                                self.tile_selected = False
                                self.tile_index = None
                            else:
                                self.tile_selected = False
                                self.tile_index = None
                        # change to new selection
                        else:
                            self.tile_index = get_tile_at_location(click_pos,
                                                                   self)
                            self.tile_loc = location_of_tile(self.tile_index,
                                                             self)
                # sending a tile to clicked location in puzzle
                else:
                    # check if in bounds
                    if type(get_tile_at_location(click_pos, self)) == tuple:
                        self.destination = get_tile_at_location(click_pos,
                                                                self)
                        # no piece at destination so make move
                        if not is_there_piece_here(self.destination, self):
                            self._puzzle.move_piece(self.tile_index,
                                                    self.destination)
                            self.tile_selected = False
                            self.tile_index = None
                            self.destination = None
                        # piece at destination
                        else:
                            # selected and destination both in puzzle
                            # update current selection
                            self.tile_index = self.destination
                            self.tile_loc = location_of_tile(self.tile_index,
                                                             self)
                # if only 'return piece' left in store check if win
                if len(self._puzzle.get_a_store('box').get_contents()) == 1:
                    if self._puzzle.check_game_state():
                        self.win = True

    def key_handler(self, event):
        for button in self.update_buttons:
            if button.get_active_bool():
                output = button.input_box_keyhandler(self, event)
                if output:
                    if output == 'n_exists':
                        self.invalid_input = True
                    else:
                        self.restart()

    def dropdown_handler(self):
        self._puzzle.update_image_name(self.imageDropdown.selected_option)
        self.start_game_button()

    def restart(self):
        self._puzzle.restart()
        self.start(self.window_size, self._puzzle)


class InputBox:
    def __init__(self, function, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = grey
        self.text = text
        self.text_surface = FONT.render(text, True, self.colour)
        self.active = False
        self.update_function = function

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 1)

    def clicked_input(self, click_loc):
        if self.rect.collidepoint(click_loc):
            self.active = True
        else:
            self.active = False
        self.colour = blue if self.active else grey

    def get_active_bool(self):
        return self.active

    def input_box_keyhandler(self, gui, event):
        if event.key == pygame.K_RETURN:
            if (self.update_function == gui._puzzle.update_image_name):
                # or self.update_function == gui._puzzle.update_image_loc):
                output = self.update_function(self.text)
                self.text = ''
                return output
            else:
                if self.text.isnumeric() and (2 <= int(self.text) <= 12):
                    self.update_function(self.text)
                    self.text = ''
                    return True
            self.text = ''
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
        # re-render the text
        self.text_surface = FONT.render(self.text, True, self.colour)
        self.update_size()

    def update_size(self):
        # resize box if text is too long
        width = max(30, self.text_surface.get_width() + 10)
        self.rect.w = width


def start_game(window_size, puzzle):
    clock = pygame.time.Clock()
    pygame.display.set_caption('Picture Puzzle')
    gui = GUI(window_size, puzzle)
    gui.draw()
    is_running = True
    while is_running:
        timeDelta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                exit()
            else:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        gui.button_handler(event)
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        gui.dropdown_handler()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    gui.mouse_handler(event)
                if event.type == pygame.KEYDOWN:
                    gui.key_handler(event)
            gui.manager.process_events(event)
        gui.manager.update(timeDelta)
        gui.draw()
