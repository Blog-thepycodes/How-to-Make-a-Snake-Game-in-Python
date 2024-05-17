import PySimpleGUI as sg
from time import time
from random import randint, choice
 
 
def grid_to_pixel(cell):
   top_left = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE
   bottom_right = top_left[0] + CELL_SIZE, top_left[1] + CELL_SIZE
   return top_left, bottom_right
 
 
def generate_apple_position(exclude, grid_size):
   grid_points = [(x, y) for x in range(grid_size) for y in range(grid_size) if (x, y) not in exclude]
   return choice(grid_points) if grid_points else None
 
 
def refresh_game_window(field, snake_body, apple_position):
   field.DrawRectangle((0, 0), (FIELD_SIZE, FIELD_SIZE), 'black')
 
 
   top_left, bottom_right = grid_to_pixel(apple_position)
   field.DrawRectangle(top_left, bottom_right, 'red')
 
 
   for index, part in enumerate(snake_body):
       top_left, bottom_right = grid_to_pixel(part)
       color = 'yellow' if index == 0 else 'green'
       field.DrawRectangle(top_left, bottom_right, color)
 
 
# Constants and variables
FIELD_SIZE = 500 # The bigger this number is the bigger the screen is
CELL_NUM = 15 # The bigger this number is the smaller the snake and the apple is
CELL_SIZE = FIELD_SIZE / CELL_NUM
 
 
snake_body = [(4, 4), (3, 4), (2, 4)]
directions = {'left': (-1, 0), 'right': (1, 0), 'up': (0, 1), 'down': (0, -1)}
direction = directions['up']
 
 
apple_position = generate_apple_position(snake_body, CELL_NUM)
apple_eaten = False
 
 
# Setup GUI
sg.theme('Green')
field = sg.Graph(
   canvas_size=(FIELD_SIZE, FIELD_SIZE),
   graph_bottom_left=(0, 0),
   graph_top_right=(FIELD_SIZE, FIELD_SIZE),
   background_color='black')
game_over_text = sg.Text('', font=('Helvetica', 20), text_color='red')
restart_button = sg.Button('Restart', key='-RESTART-', visible=False)
layout = [
   [field],
   [game_over_text],
   [restart_button]
]
window = sg.Window('Simple Snake Game - The Pycodes', layout, return_keyboard_events=True)
 
 
# Main loop
start_time = time()
score = 0
is_game_over = False
 
 
while True:
   event, values = window.read(timeout=10)
   if event == sg.WIN_CLOSED:
       break
 
 
   # Event handling
   if not is_game_over:
       if event.startswith('Left'):
           direction = directions['left']
       elif event.startswith('Up'):
           direction = directions['up']
       elif event.startswith('Right'):
           direction = directions['right']
       elif event.startswith('Down'):
           direction = directions['down']
   if event == '-RESTART-':
       snake_body = [(4, 4), (3, 4), (2, 4)]
       direction = directions['up']
       apple_position = generate_apple_position(snake_body, CELL_NUM)
       apple_eaten = False
       game_over_text.update('')
       restart_button.update(visible=False)
       score = 0
       is_game_over = False
 
 
   # Game logic
   if not is_game_over:
       time_since_start = time() - start_time
       if time_since_start >= 0.3: # This controls the speed of the snake the smaller the value the faster it gets
           start_time = time()
 
 
           if snake_body[0] == apple_position:
               apple_position = generate_apple_position(snake_body, CELL_NUM)
               apple_eaten = True
               score += 1
 
 
           new_head = (snake_body[0][0] + direction[0], snake_body[0][1] + direction[1])
           snake_body.insert(0, new_head)
           if not apple_eaten:
               snake_body.pop()
           apple_eaten = False
 
 
           if not 0 <= snake_body[0][0] <= CELL_NUM - 1 or \
               not 0 <= snake_body[0][1] <= CELL_NUM - 1 or \
               snake_body[0] in snake_body[1:]:
               game_over_text.update('Game Over! Score: {}'.format(score))
               restart_button.update(visible=True)
               is_game_over = True
 
   # Game graphics
   refresh_game_window(field, snake_body, apple_position)
 
window.close()
