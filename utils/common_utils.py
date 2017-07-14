import hashlib
import os


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def string_rgb_code(s):
    h = hashlib.new('ripemd160')
    h.update(s.encode('utf-8'))
    code = h.hexdigest()
    return code[-6:]


def string_rgb_code_with_invert(s):
    code = string_rgb_code(s)
    invert = int("FFFFFF", 16) - int(code, 16)
    return code, format(invert, 'x')


def classes_from_file(file):
    with open(file) as class_file:
        lines = class_file.readlines()

    return [line.split(':')[1] for line in lines]

