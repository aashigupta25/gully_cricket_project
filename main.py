from asyncio import streams
from concurrent.futures import thread
from email.mime import image
import tkinter
from turtle import width
import cv2 # pip install opencv-python
import PIL.Image, PIL.ImageTk #pip install pillow
from functools import partial
import threading
import time
import imutils

stream = cv2.VideoCapture("clip.mp4")
flag = True

SET_WIDTH = 650
SET_HEIGHT = 368

def play(speed):
    global flag
    print("You clicked on Play. speed is", {speed})
    
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width= SET_WIDTH, height= SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image= frame, anchor = tkinter.NW)
    if flag:
        canvas.create_text(120, 25, fill= "black", font = "Times 20 italic bold", text = "Decision Pending")
    flag = not flag    


def pending(decision):
    # Display Pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray()(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image= frame, anchor = tkinter.NW)
    
    # wait for 1 second
    time.sleep(1)

    # Display sponsor
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray()(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image= frame, anchor = tkinter.NW)

    # Wait for 1.5 second
    time.sleep(1.5)

    # Display out or notout image
    if decision == 'out':
        decisionImg = "out.png"

    else:
        decisionImg = "not_out.png"

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)   
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray()(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image= frame, anchor = tkinter.NW)


def out():
    thread = threading.Thread(target= pending, args=("out,"))
    thread.daemon = 1
    thread.start()

    print("Player is out")

def not_out():
    thread = threading.Thread(target= pending, args=("not out,"))
    thread.daemon = 1
    thread.start()

    print("Player is Not Out")

window = tkinter.Tk()
window.title("Gully Cricket Decision Umpire")
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width= SET_WIDTH, height= SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor= tkinter.NW, image = photo)
canvas.pack()

btn = tkinter.Button(window, text = " <<Previous (fast)", width = 50, command= partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text = " <<Previous (slow)", width = 50, command= partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text = " Next (slow)>>", width = 50, command= partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text = " Next (fast)>>", width = 50, command= partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text = " Give Out", width = 50, command= out)
btn.pack()

btn = tkinter.Button(window, text = " Give Not Out", width = 50, command = not_out)
btn.pack()

window.mainloop()