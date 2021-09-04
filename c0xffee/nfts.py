from PIL import Image
import os
import random


def t():
    print(os.listdir())


def get_all_layers(path):
    print(os.listdir())
    imgs = [path+'\\'+img for img in os.listdir(path) if '.png' in img]

    return imgs


def fusion(imgs, fname):
    layers = []
    for img in imgs:
        tmp = Image.open(img)
        tmp = tmp.convert('RGBA')
        layers.append(tmp)

    canvas = Image.new('RGBA', layers[0].size, (0, 0, 0, 0))
    for layer in layers:
        canvas.paste(layer, layer)

    canvas.save(fname)


def absurd_maker(imgs, fname):
    path = 'layers'

    random.shuffle(imgs)
    n = random.randint(0, len(imgs))
    imgs = imgs[:n]

    fname = fusion(imgs, fname)
    fname = path + '\\' + fname

    return fname
