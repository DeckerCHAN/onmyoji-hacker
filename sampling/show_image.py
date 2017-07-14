import os
from tkinter import *

from PIL import ImageTk, Image



root = Tk()
img = ImageTk.PhotoImage(Image.open('../data/haoyou/crop-20170706-045754.248068.jpg'))
panel = Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
root.mainloop()
