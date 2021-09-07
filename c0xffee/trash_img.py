from PIL import Image
import os
import random
import secrets
import io


def making_NFT(imgs, dir, new_dir, fname):

    up = 0
    if 'upside_down' in imgs:
        up = 1
        imgs.remove('upside_down')

    imgs = [i for i in imgs if i not in [
        'bone', 'fish', 'can', 'toast', 'politician']]

    # print(imgs)

    layers = []
    for img in imgs:
        img = dir+os.sep+img
        tmp = Image.open(img)
        tmp = tmp.convert('RGBA')
        layers.append(tmp)

    canvas = Image.new('RGBA', layers[0].size, (0, 0, 0, 0))
    for layer in layers:
        canvas.paste(layer, layer)

    if up == 1:
        canvas = canvas.transpose(Image.ROTATE_180)

    # canvas.save(new_dir+os.sep+fname)
    imgByteArr = io.BytesIO()
    canvas.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()

    return imgByteArr


def choose_one(li):
    random.shuffle(li)

    return li[-1]


def trash_body(trash, dir):
    trash_gears = [i for i in os.listdir(dir) if trash in i]
    options = [i for i in trash_gears if '_x' in i]
    color = [[i for i in trash_gears if 'color' in i][0]]
    body = list(set(trash_gears)-set(options)-set(color))
    body.sort(key=lambda x: len(x))
    # print(body)
    color = color[0]
    # print(body)

    '''
  print(trash_gears)
  print(options)
  print(color)
  print(body)
  '''

    trash = {'options': options, 'color': color, 'body': body}
    return trash


def flat(li):
    res = []
    for i in li:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res


def trash_maker():
    trash_king = []

    # bkg 8
    bkg = [i for i in os.listdir(dir) if 'bkg_' in i]
    trash_king.append(choose_one(bkg))

    # nya 2
    special = [i for i in os.listdir(dir) if 'special_' in i] + ['nothing']
    trash_king.append(choose_one(special))

    # types 5
    types = ['bone', 'fish', 'can', 'politician', 'toast']
    trash_type = choose_one(types)

    trash = trash_body(trash_type)

    # body transparent 2
    trash_king.append(choose_one([trash['color']]))
    trash_king += trash['body']

    # bone blood 2
    # bone&fish juice 2
    for op in trash['options']:
        trash_king.append(choose_one([op] + ['nothing']))

    # eyes 13
    eyes = [i for i in os.listdir(dir) if 'eyes_' in i] + ['nothing']
    trash_king.append(choose_one(eyes))

    trash_king = [i for i in trash_king if 'nothing' != i]

    # upside down 2

    return trash_king


def blk_box(poop, dir):
    for i in range(len(poop)):
        if i in [0, 1, 6]:

            continue
        if i == 2:
            trash = trash_body(poop[i], dir)
            t = poop[i]
            poop[i] = trash['body']
        if i == 3:
            if poop[i] == 'nothing':
                poop[i] = trash['color']
            else:
                poop[i] = 'nothing'
        if i == 4:
            if t == 'bone' and poop[i] == 'yes':
                poop[i] = 'bone_blood_x.png'
        if i == 5:
            if t == 'bone' or t == 'fish':
                if poop[i] == 'yes':
                    poop[i] = t + '_disgusting_x.png'
        if i == 7:
            if poop[i] == 'yes':
                poop[i] = 'upside_down'

    # print(poop)
    poop[2], poop[3] = poop[3], poop[2]
    poop = [p for p in poop if p != 'nothing']
    poop = flat(poop)

    return poop


def chk_dig(dig, rang):
    if dig not in range(rang):
        return False
    else:
        return True


def chk_idx(idx):
    if len(idx) != 8:
        return False

    normal_rang = [8, 2, 5, 2, 1, 1, 13, 2]
    bone_rang = [8, 2, 5, 2, 2, 2, 13, 2]
    fish_rang = [8, 2, 5, 2, 1, 2, 13, 2]

    now_rang = normal_rang
    if idx[2] == '0':
        now_rang = bone_rang
    elif idx[2] == '1':
        now_rang = fish_rang

    for i in range(len(idx)):
        try:
            dig = int(idx[i], 16)
            if not chk_dig(dig, now_rang[i]):
                return False
        except:
            return False

    return True


def super_rand_pick(p):
    tmp = []
    for i in range(len(p)):
        tmp += [i]*p[i]
    # print(tmp)
    return secrets.choice(tmp)


def trouble_maker():
    bkg_p = [17, 17, 17, 17, 10, 9, 8, 5]
    types_p = [23, 23, 23, 23, 8]
    eyes_p = [15, 15, 15, 10, 10, 10, 6, 6, 4, 4, 2, 2, 1]
    nya_p = [90, 10]
    trans_p = [95, 5]
    blood_p = [80, 20]
    juice_p = [65, 35]
    upside_down_p = [99, 1]
    all_p = [bkg_p, nya_p, types_p, trans_p,
             blood_p, juice_p, eyes_p, upside_down_p]
    while True:
        idx = ''
        for p in all_p:
            idx += format(super_rand_pick(p), 'x')
        if chk_idx(idx):
            break

    return(idx)


def top_secret(idx, dir, new_dir):

    bkg = ['bkg_mario_blocks.png', 'bkg_one_egg_man.png', 'bkg_super_power.png', 'bkg_earth.png',
           'bkg_nyanya_cat.png', 'bkg_danger.png', 'bkg_thats_fine.png', 'bkg_wonderful.png']
    bkg_p = [17, 17, 17, 17, 10, 9, 8, 5]

    types = ['bone', 'fish', 'can', 'toast', 'politician']
    types_p = [23, 23, 23, 23, 8]

    eyes = ['eyes_normal.png', 'eyes_ahey.png', 'eyes_weird.png', 'eyes_nothing.png', 'eyes_red.png', 'eyes_love.png', 'eyes__meme_glasses.png',
            'eyes_seaweed.png', 'eyes_green.png', 'eyes_colorful.png', 'eyes_rats_laser.png', 'eyes_rats_focus.png', 'nothing']
    eyes_p = [15, 15, 15, 10, 10, 10, 6, 6, 4, 4, 2, 2, 1]

    nya = ['nothing', 'special_nyanya_rainbow.png']
    nya_p = [90, 10]

    trans = ['nothing', 'yes']
    trans_p = [95, 5]

    blood = ['nothing', 'yes']
    blood_p = [80, 20]

    juice = ['nothing', 'yes']
    juice_p = [65, 35]

    upside_down = ['nothing', 'yes']
    upside_down_p = [99, 1]

    all_components = [bkg, nya, types, trans, blood, juice, eyes, upside_down]

    poop = []
    for i in range(len(idx)):
        poop.append(all_components[i][int(idx[i], 16)])
        #print(int(idx[i], 16), end='')
        # print(all_components[i])

    # print(poop)
    trash = blk_box(poop, dir)
    # print(trash)

    fname = idx + '.png'
    return making_NFT(trash, dir, new_dir, fname)


'''
dir = '512'
new_dir = 'RECYCLE_CAN'
#idx = '710111c1'
#idx = input('idx:')

for i in range(10000):
  idx = trouble_maker()
  print(idx)
  top_secret(idx)
'''


'''
c = 0
for i in range(500):
  trash = trash_maker()
  fname = str(c)+'.png'
  print(c, trash)
  making_NFT(trash, dir, new_dir, fname)
  c += 1
'''


# making_NFT(imgs, fname) : 照imgs圖片順j序疊在一起並輸出為fname的圖片
# imgs : 圖片檔名的list
