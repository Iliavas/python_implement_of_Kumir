from PIL import Image, ImageTk
import threading
import re

from typing import List, Callable

def get_img(canv, pos: tuple = (0, 0)):
    img = Image.open('s.png')
    img = img.resize((27, 27))
    canv.image = ImageTk.PhotoImage(img)
    canv.create_image(*pos, image=canv.image, anchor='nw')


def start_th(func: Callable, args: List[str]):
    t = threading.Thread(target=func, args=args)
    t.start()


def split_string(string, start, substring, end):
    start_string = string[:start]
    start_string += substring
    start_string += string[end:]

    return start_string

def get_quoters_under_func(string: str)->List[str]:
    it = re.finditer(r'(\(.*\))', string)
    l = {}
    for i in it:
        l.update({i.start(): i.group()})
        string = split_string(string, i.start(), '', i.end())
    a = string.replace(',', '{')
    for i in l.keys():
        a = split_string(a, i, l[i], i)
    a = re.split('\{', a)

    return a