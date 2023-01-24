import pygame
from pygame import locals

pygame.init()
pygame.joystick.init()

try: #init joystick
    j = pygame.joystick.Joystick(0)
    j.init()
    print('Enabled joystick: ' + j.get_name())
except pygame.error:
    print('no joystick found.')

while True:
    for e in pygame.event.get():
        if e.type == pygame.locals.JOYAXISMOTION: #Axes
            #0+1:nunckuck(DPAD when disconnected), 4+5:rot
            print('Nunckuck x:{},  y:{}'.format(round(j.get_axis(0), 5), round(j.get_axis(1), 5)))
            print('Rotation x:{},  y:{}'.format(round(j.get_axis(4), 5), round(j.get_axis(5), 5)))
        elif e.type == pygame.locals.JOYHATMOTION: #D-pad
            print('D-pad', e.value)
        elif e.type == pygame.locals.JOYBUTTONDOWN: #Button press
            print('button down: ', wii[e.button])
        elif e.type == pygame.locals.JOYBUTTONUP: #Button release
            print('button up: ', wii[e.button])
