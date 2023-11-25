import os
import numpy as np
import math
import time

rect_points_screen = []
rect_points = []
angle = math.radians(8) # minimum: 8

rectangle_width = 5 #minimum: 4

R = np.array([[np.cos(angle), -np.sin(angle)],
              [np.sin(angle), np.cos(angle)]]) #2D rotation matrix

size = os.get_terminal_size()
w = size.columns
h = size.lines

def makeScreen(w, h, c):
  return [[c] * w for _ in range(h)]

def makeRotation(points: list, matrix: np.ndarray[any]):
  center_x = w//2
  center_y = h//2
  rotated_square = np.dot(points, matrix)
  rotated_square = rotated_square.round().astype(int)
  rotated_square = rotated_square.tolist()

  rect_points_screen.clear()  # Clear the previous screen coordinates

  for rotated_point in rotated_square:
      screen_x = center_x + rotated_point[0]
      screen_y = center_y + rotated_point[1]
      rect_points_screen.append([screen_x, screen_y])

  return rotated_square


def renderScreen(screen):
  os.system('cls')
  print('\n'.join([''.join(r) for r in screen]))

def drawLine(screen, p1: list, p2: list, color: int):
  dx = p2[0] - p1[0]
  dy = p2[1] - p1[1]

  step = max(abs(dx), abs(dy))

  if step > 0: dx /= step
  if step > 0: dy /= step

  x = p1[0]
  y = p1[1]

  for _ in range(0, int(step) + 1):
    colorStart = '\033[0;' + str(color + 30) + ';40m'
    colorEnd = '\033[0;0m'

    screen[int(y)][int(x)] = colorStart + "█" + colorEnd
    x += dx
    y += dy
  return screen

def initRect(screen, w, h, width):
  center_x = w//2
  center_y = h//2
  rect_points.append([+width, +width]) #botton right corner
  rect_points_screen.append([center_x+width, center_y+width])
  rect_points.append([+width, -width]) #botton left corner
  rect_points_screen.append([center_x+width, center_y-width])
  rect_points.append([-width, -width]) #top left corner
  rect_points_screen.append([center_x-width, center_y-width])
  rect_points.append([-width, +width]) #top right corner
  rect_points_screen.append([center_x-width, center_y+width])

  return screen


colorVar = 1
grid = makeScreen(w,h,' ')
grid = initRect(grid, w, h, rectangle_width)
grid = drawLine(grid, rect_points_screen[3], rect_points_screen[2], colorVar)
grid = drawLine(grid, rect_points_screen[0], rect_points_screen[1], colorVar)
grid = drawLine(grid, rect_points_screen[1], rect_points_screen[2], colorVar)
grid = drawLine(grid, rect_points_screen[0], rect_points_screen[3], colorVar)
originalTopLeftCornerPos = rect_points_screen[3]
renderScreen(grid)
time.sleep(0.5)

iter = 0
while True:
  grid = []
  rect_points = makeRotation(rect_points, R)
  grid = makeScreen(w,h,' ')
  grid = drawLine(grid, rect_points_screen[3], rect_points_screen[2], colorVar)
  grid = drawLine(grid, rect_points_screen[0], rect_points_screen[1], colorVar)
  grid = drawLine(grid, rect_points_screen[1], rect_points_screen[2], colorVar)
  grid = drawLine(grid, rect_points_screen[0], rect_points_screen[3], colorVar)
  renderScreen(grid)
  if iter % 20 == 0:
    if colorVar != 4:
      colorVar += 1
    else:
      colorVar = 1
  iter += 1
  time.sleep(0.05)
