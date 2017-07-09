from tkinter import *

from PIL import ImageTk, Image


class Selector(object):
    def __init__(self, image):
        self.root = Tk()
        self.root.wm_title("Sampling")
        self.root.resizable(0, 0)

        self.drag_data = {"x": 0, "y": 0, "item": None}

        self.canvas = Canvas(self.root, width=image.size[0], height=image.size[1], bg='blue')
        self.canvas.pack(side=LEFT, expand=1, fill=Y)

        self.right_control = Frame(self.root)
        self.right_control.pack(side=RIGHT, fill=Y, expand=1)

        self.inputs = Entry(self.right_control)
        self.inputs.pack(side=TOP, fill=X)

        self.func_btns = Frame(self.right_control)
        self.func_btns.pack(side=TOP, fill=X)

        self.add_label_btn = Button(self.func_btns, text="Add", width=10, command=self.add_label)
        self.add_label_btn.pack(side=LEFT)

        self.del_label_btn = Button(self.func_btns, text="Delete", width=10, command=self.del_label)
        self.del_label_btn.pack(side=LEFT)

        self.labels_listbox = Listbox(self.right_control)
        self.labels_listbox.pack(side=TOP, fill=BOTH)

        self.control_btns = Frame(self.right_control)
        self.control_btns.pack(side=BOTTOM, fill=X)

        self.add_label_btn = Button(self.control_btns, text="Clear", width=10, command=self.clear_all)
        self.add_label_btn.pack(side=LEFT)

        self.add_label_btn = Button(self.control_btns, text="Next", width=10, command=self.next)
        self.add_label_btn.pack(side=LEFT)

        self.image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=self.image, anchor=NW, tags="bkg")

        self.canvas.bind("<ButtonPress-1>", self.on_token_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_token_release)
        # self.canvas.bind("<B1-Motion>", self.on_token_motion)
        self.root.bind("<KeyPress>", self.keydown)

    def create_token(self, tag, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x, y) = coord
        self.canvas.create_rectangle(x - 25, y - 25, x + 25, y + 25,
                                     outline=color, width=5, tags=tag)

    def save_to_file(self):
        for i, listbox_entry in enumerate(self.labels_listbox.get(0, END)):
            raise NotImplementedError

    def on_token_press(self, event):
        '''Begining drag of an object'''

        if len(self.labels_listbox.curselection()) !=1:
            return

        # record the item and its location
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_token_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_token_motion(self, event):
        '''Handle dragging of an object'''
        # compute how much the mouse has moved
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        # move the object the appropriate amount but never the bg
        if self.drag_data["item"] == 1:
            return
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)
        # record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def clear_all(self, event):
        raise NotImplementedError

    def next(self, event):
        raise NotImplementedError

    def add_label(self):
        if self.inputs.get():
            self.labels_listbox.insert(END, str(self.inputs.get()))

    def del_label(self):
        if len(self.labels_listbox.curselection()) == 1:
            self.labels_listbox.delete(self.labels_listbox.curselection()[0])

    def keydown(self, event):
        if event.char == 'c':
            print('Clear!')


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    img = Image.open('../data/haoyou/crop-20170706-045754.248068.jpg').resize((400, 400))

    selector = Selector(img)
    selector.run()
