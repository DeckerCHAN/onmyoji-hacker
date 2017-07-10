import datetime
import os
from tkinter import *
from xml.etree.ElementTree import Element, SubElement, ElementTree

from PIL import ImageTk

import utils
from capture import Capture
from image_feeder import RealCaptureFeeder


class Selector(object):
    def __init__(self, image_feeder, save_folder):

        self.save_folder = save_folder

        self.root = Tk()
        self.root.wm_title("TF Slim & VOC Dataset Sampling Tool")
        self.root.resizable(0, 0)

        self.drag_data = {"x": 0, "y": 0}

        self.canvas = Canvas(self.root, bg='blue')
        self.canvas.pack(side=LEFT, expand=1, fill=Y)
        self.image_feeder = image_feeder
        self.photo_image = None
        self.raw_image = None

        self.feed_image()

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
        self.labels_listbox.config(font=("Courier", 15))

        self.control_btns = Frame(self.right_control)
        self.control_btns.pack(side=BOTTOM, fill=X)

        self.add_label_btn = Button(self.control_btns, text="Save", width=10, command=self.save)
        self.add_label_btn.pack(side=LEFT)

        self.add_label_btn = Button(self.control_btns, text="Next", width=10, command=self.next)
        self.add_label_btn.pack(side=LEFT)

        self.last_created = None

        self.canvas.bind("<ButtonPress-1>", self.on_left_key_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_key_release)
        # self.canvas.bind("<B1-Motion>", self.on_token_motion)
        self.root.bind("<KeyPress>", self.keydown)

    def feed_image(self):
        self.raw_image = self.image_feeder.feed()
        self.photo_image = ImageTk.PhotoImage(self.raw_image)

        self.canvas.delete("all")
        self.canvas.config(width=self.raw_image.size[0], height=self.raw_image.size[1])
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=NW, tags="bg")

    def on_left_key_press(self, event):
        '''Begining drag of an object'''

        if len(self.labels_listbox.curselection()) != 1:
            return

        # record the item and its location
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_left_key_release(self, event):
        '''End drag of an object'''
        # reset the drag information
        if len(self.labels_listbox.curselection()) != 1:
            return

        tag = self.labels_listbox.get(self.labels_listbox.curselection())

        color = utils.string_rgb_code(tag)

        self.last_created = self.canvas.create_rectangle(
            self.drag_data["x"],
            self.drag_data["y"],
            event.x,
            event.y,
            outline='#' + color,
            width=5,
            tags=tag
        )

        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def save(self):

        utils.create_folder_if_not_exists(self.save_folder)

        classed_image = os.path.join(self.save_folder, "classed_images")
        utils.create_folder_if_not_exists(classed_image)

        voc_path = os.path.join(self.save_folder, "voc")
        utils.create_folder_if_not_exists(voc_path)

        jpeg_image_path = os.path.join(voc_path, "JPEGImages")
        utils.create_folder_if_not_exists(jpeg_image_path)

        annotation_path = os.path.join(voc_path, "Annotations")
        utils.create_folder_if_not_exists(annotation_path)

        file_name = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

        annotation_xml = Element('annotation')
        size_xml = SubElement(annotation_xml, 'size')
        width_xml = SubElement(size_xml, 'width')
        width_xml.text = str(self.raw_image.size[0])

        height_xml = SubElement(size_xml, 'height')
        height_xml.text = str(self.raw_image.size[1])

        depth_xml = SubElement(size_xml, 'depth')
        depth_xml.text = str(3)

        for i, label in enumerate(self.labels_listbox.get(0, END)):

            found = self.canvas.find_withtag(label)

            label_path = os.path.join(classed_image, label)

            utils.create_folder_if_not_exists(label_path)

            for j, found_index in enumerate(found):
                # Process crop image
                xmin, ymin, xmax, ymax = self.canvas.bbox(found_index)
                bbox = (xmin, ymin, xmax, ymax)
                crop = self.raw_image.crop(bbox)
                crop_path = os.path.join(label_path,
                                         str.format("{0}-{1}[{2}].jpg", label, file_name, j))

                # Remove iligeal part
                xmin = max(xmin, 0)
                ymin = max(ymin, 0)
                xmax = min(xmax, self.raw_image.size[0])
                ymax = min(ymin, self.raw_image.size[1])

                crop.save(crop_path)
                # Process xml object
                object_xml = SubElement(annotation_xml, 'object')

                name_xml = SubElement(object_xml, 'name')
                name_xml.text = str(label)

                difficult_xml = SubElement(object_xml, 'difficult')
                difficult_xml.text = str(0)

                bndbox_xml = SubElement(object_xml, 'bndbox')

                xmin_xml = SubElement(bndbox_xml, 'xmin')
                xmin_xml.text = str(xmin)

                ymin_xml = SubElement(bndbox_xml, 'ymin')
                ymin_xml.text = str(ymin)

                xmax_xml = SubElement(bndbox_xml, 'xmax')
                xmax_xml.text = str(xmax)

                ymax_xml = SubElement(bndbox_xml, 'ymax')
                ymax_xml.text = str(ymax)

                pass

        with open(os.path.join(annotation_path, str.format("{0}.xml", file_name)), 'w') as xml:
            tree = ElementTree(annotation_xml)
            tree.write(xml, encoding='unicode')

        self.raw_image.save(os.path.join(jpeg_image_path, str.format("{0}.jpeg", file_name)))

    def next(self):
        self.feed_image()

    def add_label(self):
        if self.inputs.get() and not self.inputs.get() in self.labels_listbox.get(0, END):
            self.labels_listbox.insert(END, str(self.inputs.get()))
            bg, fg = utils.string_rgb_code_with_invert(self.inputs.get())
            self.labels_listbox.itemconfig(END, foreground='#' + fg, background='#' + bg)

    def del_label(self):
        if len(self.labels_listbox.curselection()) == 1:
            index = self.labels_listbox.curselection()[0]
            tag = self.labels_listbox.get(self.labels_listbox.curselection())
            self.canvas.delete(tag)
            self.labels_listbox.delete(index)

    def keydown(self, event):
        if event.char == 'c' and self.last_created is not None:
            self.canvas.delete(self.last_created)
            self.last_created = None
            print('Clear!')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    capture = Capture(100, 100, 780, 440)

    imf = RealCaptureFeeder(capture)

    selector = Selector(imf, 'data/samples')
    selector.run()
