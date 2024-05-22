# Description
This is a livestreaming and scoring system for the ASABE IQS competition
This system uses ros2 as a middleware for transfering data between the nodes on the network.
Python QT is used for all displays

# Installation
-------------
## ROS
    Standard ROS humble installation is used for the middle layer.

## PIP packages
    The unified backend and sql packages are pip packages that can be installed through pip install -e and the directory name


## Running
$ ros2 run management_console management_console 

QML application that has everything in it
Set pull, maneuverabilty order
Sets track state and whos running
Track state dictates what is going on
Button press in the sled would tell track is running

Wants content node between camera and obs node to give position node 

Management consile manages all track states
Select camera 1 or 2
When track state is 1 track specific tag
Ultra wide band tags from Thoreson to get position
    Set up through tablet otherwise 
    End up with X/Y location
    This uses the DWM node
    Had issues getting these to connect

QT stuff
    Overlay and liveboard
    Runs as nodes
    Runs on PYQt system
    Each node spins ros and QT thread
    QT is blocking, ros has callbacks that change parameters in QT
    Nick has nice QML's for this


Backend 
    Passes all data out

Chat GPT is good with PYQT

Renders as application
Screen capture through obs

