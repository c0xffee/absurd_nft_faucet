from PIL import Image
import os
import random
import secrets
import io


def making_NFT(imgs, dir, new_dir, bkup_dir, fname, bkup_name):

    up = 0
    if 'upside_down' in imgs:
        up = 1
        imgs.remove('upside_down')

    imgs = [i for i in imgs if i != 'nothing']

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

    imgByteArr = io.BytesIO()
    canvas.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()

    return imgByteArr


def choose_one(li):
    random.shuffle(li)

    return li[-1]


def trash_body(trash):
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

    bkg = secrets.choice(range(4))
    color = secrets.choice(range(6))
    eyes = secrets.choice(range(8))
    up = secrets.choice([0]*49+[1])
    idx = str(bkg) + str(color) + str(eyes) + str(up)

    return(idx)


def top_secret(idx, fname, bkup_name):

    bkg = ['bkg_classic.png', 'bkg_cool.png', 'bkg_love.png', 'bkg_sky.png']
    color = ['color_gold.png', 'color_kirby.png', 'color_poop.png',
             'color_rainbow.png', 'color_slime.png', 'nothing']
    eyes = ['eyes_crying.png', 'eyes_fuck.png', 'eyes_happy.png', 'eyes_question.png',
            'eyes_sleepy.png', 'eyes_unknown.png', 'eyes_what.png', 'eyes_wow.png']
    up = ['nothing', 'upside_down']

    all_components = [bkg, color, eyes, up]

    poop = []
    for i in range(len(idx)):
        poop.append(all_components[i][int(idx[i], 16)])
        #print(int(idx[i], 16), end='')
        # print(all_components[i])

    body = ['body_Blush.png', 'body_outline.png']
    poop += body

    return making_NFT(poop, dir, new_dir, bkup_dir, fname, bkup_name)


def chk_duplicates(idx):
    fname = 'publish_nft_datas.csv'
    with open(fname, 'r') as f:
        datas = [i for i in f.read().split('\n') if i != ''][1:]

    for d in datas:
        if datas == []:
            return True

        old_idx = d.split(',')[1]
        if idx == old_idx:
            return True

    return False


#fname = child_tok + '.png'
def make_a_poop(fname, nft_name):

    while True:
        idx = trouble_maker()
        print(idx)
        if not chk_duplicates(idx):
            break

    bkup_name = nft_name + '-' + idx + '.png'
    top_secret(idx, fname, bkup_name)
    path = new_dir + os.sep + nft_name

    return path, idx


def name_creator():
    fname = 'c0xffee\\eng-names.txt'
    with open(fname, 'r') as f:
        name_li = [n for n in f.read().split() if n != '']

    return secrets.choice(name_li)


def make_nft_name(name, num):
    return '%s [#%d]' % (name, num)


# need 2 change
dir = 'poop_layers'
new_dir = 'TOILET\\original'
bkup_dir = 'TOILET\\bkup'
#idx = '710111c1'
#idx = input('idx:')

'''
for i in range(10000):
  idx = trouble_maker()
  print(idx)
  fname = idx + '.png'
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
