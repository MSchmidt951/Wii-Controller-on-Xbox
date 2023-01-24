import pygame
from pygame import locals

pygame.init()
pygame.joystick.init()

try:
    j = pygame.joystick.Joystick(0)
    j.init()
    print('Enabled joystick: ' + j.get_name())
except pygame.error:
    print('no joystick found.')

def printAxis(a):
    global j
    try:
        while True:
            for e in pygame.event.get():
                if e.type == pygame.locals.JOYAXISMOTION:
                    print(j.get_axis(a))
    except KeyboardInterrupt:
        print('\n')

def CalibratePos(pos):
    print('Calibrating {}:'.format(pos))
    avg = 0.0
    for i in range(3):
        avg += float(input('   Enter {}'.format(pos)))
    return avg/3

def CalibrateAxes():
    rest = CalibratePos('rest')
    Min = CalibratePos('minimum')
    Max = CalibratePos('maximum')
    tmpMin = Min
    Min = round(1/(abs(min(Min, Max))+rest), 5) #Get true min and max values
    Max = round(1/(max(tmpMin, Max)-rest), 5)
    return [Min, round(rest, 5), Max]

try:
    while True:
        axis = int(input('Either press control+c to exit\nOr enter an axis to monitor: '))
        printAxis(axis)
except KeyboardInterrupt:
    print("\n\nNow enter the positions")

results = []
print('\n\nPress control+C when done to get the results\n')
try:
    while True:
        results.append(CalibrateAxes())
        print('=====Axis Done=====\n')
except KeyboardInterrupt:
    print("\n\nPrinting results")

for i, res in enumerate(results):
    print('{} - {}'.format(i+1, res))
