import cv2
import numpy as np

def draw_pylon(x,y,ptype):
    if ptype==1:
        color=(0,255,255)
    else:
        color=(0,0,255)
    cv2.rectangle(img, (x-10,y-10), (x+10, y+10), color, -1)
    cv2.circle(img, (x,y),5,(255,255,255),-1)
    cv2.imshow('Image', img)


# Callback function for mouse events
def draw_rectangle(event, x, y, flags, param):
    global drawing, ix, iy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        draw_pylon(x,y,1)
    
    if event == cv2.EVENT_RBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        draw_pylon(x,y,2)

# Create a black image
img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('Image')

# Initialize mouse callback function
cv2.setMouseCallback('Image', draw_rectangle)

drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Starting coordinates

while True:
    cv2.imshow('Image', img)
    key = cv2.waitKey(1) & 0xFF

    # Press 'Esc' to exit
    if key == 27:
        break

cv2.destroyAllWindows()
