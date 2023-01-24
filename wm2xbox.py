import pygame, pyxinput
from pygame import locals
from time import sleep

##Settings
controlsFile = 'CoD.txt'

#Init virtual xbox conntroller and pygame
controller = pyxinput.vController()
pygame.init()
pygame.joystick.init()

#Load the controls and settings
controls = [{}, {}]
settings = {}
controlPreset = -1
f = open('controls/'+controlsFile, 'r')
for line in f:
    line = line.replace('\n', '')
    if line == 'NEXT':
        controlPreset += 1
    elif controlPreset == -1: #Settings
        line = line.split('|')
        invert = line[1] != 'F'
        settings[line[0]] = [invert, float(line[2])]
    else: #Controls
        line = line.split(':')
        controls[controlPreset][line[0]] = line[1]
print(controls)

#Initialise variables
axisRate = 3 #The axes of the wii controller is recorded every axisRate+1 loops
xboxButtons = controls[0]
wii = {
    0:'a',
    1:'b',
    2:'c',
    3:'z',
    4:'1',
    5:'2',
    6:'plus',
    7:'minus',
    8:'home'
}
Dpad = 0
DpadVals = {
    'D-left':4,
    'D-right':8,
    'D-up':1,
    'D-down':2
}
padPressed = False
wmPad = [[], []]
nkX  = ['stick_x', 1.305, 0.0714, 1.247, settings['nkX'][0], settings['nkX'][1]]
nkY  = ['stick_y', 1.29, 0.0555, 1.311, settings['nkY'][0], settings['nkY'][1]]
accR = ['acc_r', 1.29, 0.0554, 1.256, settings['accR'][0], settings['accR'][1]]
accP = ['acc_p', 1.29, 0.0554, 1.211, settings['accP'][0], settings['accP'][1]]


##Functions

#Convert a wii remote button press to an xbox button press
def Button(wmBtn, val):
    global xboxButtons, Dpad, DpadVals, padPressed
    if wmBtn == 'home':
        if val == 1:
            switchControls()
    else:
        xBtn = xboxButtons[wmBtn]
        if 'D-' in xBtn:
            padPressed = True
            if val == 1:
                Dpad += DpadVals[xBtn]
            else:
                Dpad -= DpadVals[xBtn]
        else:
            controller.set_value(xBtn, val)

#Convert a wii remote axis input to xbox output
def Axis(data, pos):
    global xboxButtons
    xBtn = xboxButtons[data[0]]
    #Get xbox value
    val = pos-data[2]
    val *= data[3] if val>=0 else data[1]
    val *= data[5] #sensitivity
    if data[4]:
        val *= -1
    if val > 1:
        val = 1
    elif val < -1:
            val = -1
    if ',' in xBtn:
        xBtn = xBtn.split(',')
        Raw(xBtn[0], val, -0.5)
        Raw(xBtn[1], val, 0.5)
    elif xBtn != 'none':
        controller.set_value(xBtn, val)

#Take raw input from an axis and output it to the xbox controller
def Raw(btn, pos, s):
        val = (pos-s) * 4 * s
        if val < -1:
            val = -1
        controller.set_value(btn, val)

#Ready wii D-Pad input to send to the controller
def wiiDpad(strA, strB, pos):
    global wmPad
    if pos == -1:
        wmPad[0].append(strA)
    elif pos == 1:
        wmPad[0].append(strB)
    else:
        if strA in wmPad[0]:
            wmPad[0].remove(strA)
            wmPad[1].append(strA)
        if strB in wmPad[0]:
            wmPad[0].remove(strB)
            wmPad[1].append(strB)

#Switch to next control preset
def switchControls():
    global xboxButtons, controls
    if xboxButtons == controls[0]:
        xboxButtons = controls[1]
    else:
        xboxButtons = controls[0]
    sleep(0.5)


##Main code

#init joystick
try:
    j = pygame.joystick.Joystick(0)
    j.init()
    print('Enabled joystick: ' + j.get_name())
except pygame.error:
    print('no joystick found.')
    del controller
    quit()

#Main loop
try:
    while True:
        for e in pygame.event.get():
            if e.type == pygame.locals.JOYAXISMOTION: #Axes
                if axisRate == 3: #0+1:nunckuck(DPAD when disconnected), 4+5:rot
                    Axis(nkX, j.get_axis(0))
                    Axis(nkY, j.get_axis(1))
                    Axis(accR, j.get_axis(4))
                    Axis(accP, j.get_axis(5))
                    axisRate = 0
                else:
                    axisRate += 1
            elif e.type == pygame.locals.JOYHATMOTION: #D-pad
                wiiDpad('down', 'up', e.value[1])
                wiiDpad('left', 'right', e.value[0])
                for btn in wmPad[0]:
                    Button(btn, 1)
                for btn in wmPad[1]:
                    Button(btn, 0)
                    wmPad[1].remove(btn)
            elif e.type == pygame.locals.JOYBUTTONDOWN: #Button press
                Button(wii[e.button], 1)
            elif e.type == pygame.locals.JOYBUTTONUP: #Button release
                Button(wii[e.button], 0)
            if padPressed:
                controller.set_value('Dpad', Dpad)
                padPressed = False
except KeyboardInterrupt:
    print("Exiting")

#Disconnect controller
del controller
