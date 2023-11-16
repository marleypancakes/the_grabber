import pyautogui
import tkinter as tk
import cv2 as cv
from cv2 import *
import numpy

from PIL import ImageTk, Image

# myScreenshot = pyautogui.screenshot()
# myScreenshot.save


transparent_color = 'grey15'
line = None
points = []
line_options = {}

# These functions and the code for the transparency window are sourced from 
# https://stackoverflow.com/a/69154451 user Matiiss

# def set_first(event):
#     points.extend([event.x, event.y])

# def append_and_draw(event):
#     global line
#     points.extend({event.x, event.y})
#     if len(points) == 4:
#         line = canvas.create_line(points, **line_options)
#     else:
#         canvas.coords(line, points)

# def clear_list(event=None):
#     global line
#     points.clear()
#     line = None

root = tk.Tk()
root.title("THE GRABBER")
# Make it transparent
root.attributes('-alpha', 0.01)
# Make it be on top
root.attributes('-topmost', True)
# Make it fullscreen
root.attributes('-fullscreen', True)

# Bind escape so u can close the window
root.bind('<Escape>', lambda e: root.quit())

top = tk.Toplevel(root)
top.attributes('-transparentcolor', transparent_color)
top.attributes('-topmost', True)
top.attributes('-fullscreen', True)

editor = None
src = None
tool = None
hasMap = False
# First onmousedown -> start selecting region

# Drag and release to size the window

# Focus the root cause events are bound here
root.focus_set()

# create canvas for drawing

canvas = tk.Canvas(top, bg=transparent_color, highlightthickness=0)
canvas.pack(fill='both', expand=True)

origin = ()

def get_origin(event):
    global origin
    origin = (event.x, event.y)
    print(origin)

def capture(event):
    global top
    global editor
    print(origin)
    width, height = event.x_root, event.y_root
    width = width - origin[0]
    height = height - origin[1] 

    dimensions = (origin[0], origin[1], width, height)
    dimensionstr = "{0}x{1}+{2}+{3}".format(dimensions[0], dimensions[1], dimensions[2], dimensions[3])
    print(dimensionstr)
    # root.geometry(dimensionstr)

    im = pyautogui.screenshot(region=dimensions)

    top.destroy()
    # top.attributes('-fullscreen', False)
    editor = tk.Toplevel(root)

    editor.resizable(True, True)
    print("Editor: " + editor.winfo_geometry())
    print("Root: " + root.winfo_geometry())
    # editor.geometry(dimensionstr)
    # root.geometry(dimensionstr)
    print(editor.winfo_geometry())
    im1 = ImageTk.PhotoImage(im)

    image1 = tk.Label(editor, image=im1)
    image1.image = im1
    image1.pack()
    lasso(im)

    # im_name = pyautogui.prompt(text='Name your image:')
    # im.save(r'C:\Users\Marley\development\the_grabber\Screenshots' + chr(92) + im_name + '.jpg')

def lasso(img):
    global src
    global tool
    global canvas
    global editor
    print("lasso is running")
    src = img.convert('RGB')
    src = numpy.array(src)
    src = cv.cvtColor(src, cv.COLOR_RGB2BGR)
    cv.imwrite("test.png", src)

    canvas.destroy()
    canvas2 = tk.Canvas(editor, bg=transparent_color, highlightthickness=0)
    # cv.imread()
    
    tool = cv.segmentation.IntelligentScissorsMB()
    tool.setEdgeFeatureCannyParameters(32, 100)
    tool.setGradientMagnitudeMaxLimit(200)
    tool.applyImage(src)

    hasMap = False

    # root.unbind_all('<Button-1>')
    # root.unbind_all('<B1-motion>')
    root.bind('<Button-1>', start_map)
    root.bind('<B1-Motion>', track_map)

    
def start_map(event):
        global src
        global tool
        print("Start_map is running")
        print(repr(src))
        startX, startY = event.x, event.y
        print("Startx: " + str(startX))
        print("Starty: " + str(startY))
        print("Boundx: " + str(src.size))
        print("Boundy: " + str(src.T.size))
        # if startX < src.size & startY < src.T.size:
        tool.buildMap((startX, startY))
        print("MAP BUILT")
        hasMap = True
    
def track_map(event):
    global src
    x, y = event.x, event.y
    dst = src.copy()
    if (hasMap & x >= 0 & x < src.size & y >= 0 & y < src.T.size):
        arr = numpy.array([])
        contour = cv.Mat(arr)
        print(tool)
        tool.getContour((x, y), contour)
        contours = cv.Mat(arr)
        contours.append(contour)
        color = cv.Scalar(0, 255, 0, 255)
        cv.polylines(dst, contours, False, color, 1, cv.LINE_8)
        contours.delete()
        contour.delete()
        
        cv.imshow('')



# bind all events to 'root' which "blocks" mouse 
# but is also almost invisible
root.bind('<Button-1>', get_origin)
# root.bind('<B1-Motion>', append_and_draw)
root.bind('<ButtonRelease-1>', capture)

root.mainloop()

