# Wii Controller on Xbox

Allows a wii controller to be used on an xbox without having to buy any extra hardware.  
This is done by connecting a wii controller to a computer with bluetooth, running a `wm2xbox` and connecting the computer to an xbox.

## Setup

- Install Python with the pygame and pyxinput libraries and download the repository.
- Change `controlsFile` variable to the conrol layout that you want to use.
- Connect the wii remote and run the xbox companion app then connect remotely to it.
- Run `wm2xbox.py`

## Custom controls

A custom control scheme can be added in the `controls` folder.  
To map a wii remote button to an xbox button the syntax is as follows `wiiButton:xboxButton`.  
Put each mapping on a new line.
