from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import make_response
from c0xffee.chk_trans import chk_tx, chk_tx_by_api, show_float, chk_slp_addr, update_data, chk_tx_exist, headsha, update_finished_nft_num, backup, get_nft_price, ttt, chk_addr, legacy_to_cash_addr, change_nft_price
from c0xffee.trash_img import trouble_maker, top_secret
import c0xffee.poop_img
import csv
import os

app = Flask(__name__)

'''
@app.route("/")
@app.route("/home")
def home():
    NFT_price = get_nft_price('nft_price.txt')
    return render_template("home.html", NFT_price=NFT_price)
'''
price_fname = 'poop_nft_price.txt'

'''
@app.route("/new_home")
def new_home():
    poop_NFT_price = get_nft_price(price_fname)
    return render_template("new_home.html", NFT_price=poop_NFT_price)
'''


@app.route("/sold_out")
def sold_out():
    return render_template("sold_out.html")


@app.route("/")
@app.route("/home")
@app.route("/poop")
def poop():
    return render_template("sold_out.html")


'''
@app.route("/")
@app.route("/home")
@app.route("/poop")
def poop():
    poop_NFT_price = get_nft_price(price_fname)
    return render_template("home.html", NFT_price=poop_NFT_price)
'''


@app.route("/payment", methods=['POST'])
def payment():
    title = "Waiting FOR your Payment"
    slp_addr = request.form["slp_addr"]
    NFT_price = get_nft_price(price_fname)
    if chk_slp_addr(slp_addr) or not chk_addr(slp_addr):
        warning = 'slp_addr_illegal!!'
        return render_template("home.html", NFT_price=NFT_price, warning=warning)
    amount = request.form["amount"]
    try:
        int(amount)
    except:
        warning = 'illegal_amount!!'
        return render_template("home.html", NFT_price=NFT_price, warning=warning)

    total_payment = show_float(float(amount)*NFT_price)
    nft_price = show_float(NFT_price)
    return render_template("payment.html.jinja", title=title, slp=slp_addr, amount=amount, nft_price=nft_price, total_payment=total_payment)
    # return title + slp_addr + pay_addr
    # return redirect(url_for("payment", title=title, slp=slp_addr, pay=pay_addr))


'''
@app.route("/test")
def test():
    url = request.args.get('url')
    return ttt(url)
'''


@app.route("/dbck", methods=['POST'])
def dbck():

    buyer_slp = request.form["buyer_slp"]
    tx_url = request.form["tx"]
    bch = request.form["bch"]
    bch_addr = request.form["bch_addr"]
    NFT_price = get_nft_price(price_fname)
    failed, *data = chk_tx_by_api(tx_url, bch_addr, float(bch), NFT_price)
    data = [data[0], buyer_slp, tx_url, bch, bch_addr] + data[1:] + [0]
    print(data)
    if chk_tx_exist(data[0]):
        warning = "Paymant already Finished"
        return render_template("home.html", NFT_price=NFT_price, warning=failed)

    if failed != '':
        data += [failed]
        fname = 'failed.csv'
        update_data(data, fname)
        return render_template("home.html", NFT_price=NFT_price, warning=failed+'contact us with tx_no:'+data[2].split('/')[-1])

    fname = 'all_payment.csv'
    update_data(data, fname)
    r = data
    schema = ['tx_no', 'web_slp_addr', 'web_tx_link',
              'chain_actually_pay', 'chain_tx_datetime', 'verified_nft_amount', 'finish_num']
    order_data = [r[0], r[1], r[2], r[7], r[11], r[12]]
    leng = len(order_data)
    print(failed)

    if failed == '':
        return render_template("successful.html", data=order_data, schema=schema, leng=leng)

    # buyer_slp + tx_url + bch + bch_addr + str(data)
    # render_template("dbck.html", buyer_slp=buyer_slp, tx=tx, bch=bch, bch_addr=bch_addr)
    # return buyer_slp + tx + bch + bch_addr


@app.route("/all_payments")
def all_payment():
    fname = 'all_payment.csv'
    with open(fname, 'r') as f:
        sth = f.read()
    return sth


@app.route("/failed_payments")
def failed_payment():
    fname = 'failed.csv'
    with open(fname, 'r') as f:
        sth = f.read()
    return sth


@app.route("/show_me_progress")
def show_me_progress():
    fname = 'all_payment.csv'
    visible_data = []
    with open(fname, newline='') as csvfile:
        rows = csv.reader(csvfile)
        rows = [r for r in rows if r != []]
        for r in rows:
            visible_data.append([r[0], r[1], r[2], r[7], r[11], r[12], r[13]])

    return render_template("show_me_progress.html", data=visible_data)


@app.route("/trash.png")
def trash_img():
    dir = 'trash_layers'
    new_dir = 'RECYCLE_CAN'
    idx = trouble_maker()
    img_bytes = top_secret(idx, dir, new_dir)
    #fname = new_dir + os.sep + idx + '.png'
    #img_data = open(fname, 'rb').read()
    resp = make_response(img_bytes)
    resp.headers['Content-Type'] = 'image/png'

    return resp


@app.route("/poop.png")
def poop_img():
    dir = 'poop_layers'
    new_dir = 'TOILET'
    idx = c0xffee.poop_img.trouble_maker()
    img_bytes = c0xffee.poop_img.top_secret(idx, dir, new_dir)
    #fname = new_dir + os.sep + idx + '.png'
    #img_data = open(fname, 'rb').read()
    resp = make_response(img_bytes)
    resp.headers['Content-Type'] = 'image/png'

    return resp


# ADMIN
@app.route("/secret_door", methods=['POST'])
def secret_door():
    try:
        secret = 'god_is_dead_rick&morty'
        secret = request.form["secret"]
        tx = request.form["tx"]
        finish_num = request.form["finish_num"]
    except:
        return 'fuck you!'
    if headsha(secret) == 'eb5751f0473ae0068eb45c7616dbf9bef8107a2650dc30469dd08ebb111e503d':
        update_finished_nft_num(tx, finish_num)
        backup()
        return '%s %s NFTs FINISHED' % (tx, finish_num)
    else:
        return str(hash(secret))+secret


@app.route("/change_price", methods=['POST'])
def change_price():
    now_price = get_nft_price(price_fname)
    try:
        secret = 'god_is_dead_rick&morty'
        secret = request.form["secret"]
        new_price = request.form["price"]
    except:
        return 'fuck you!'
    if headsha(secret) == 'eb5751f0473ae0068eb45c7616dbf9bef8107a2650dc30469dd08ebb111e503d':
        if change_nft_price(new_price, price_fname) == 'failed':
            return 'CHANGE PRICE ERROR'

        return 'PRICE IS CAHNGED : %f ==> %s ' % (now_price, new_price)
    else:
        return str(hash(secret))+secret


'''
@app.route("/wait2pay")
def wait2pay():
    title = 'wait2pay'
    return render_template("wait2pay.html", title=title)


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/t")
def t():
    return render_template("t.html")


@app.route("/paybutton")
def paybutton():
    return render_template("paybutton.html")


@app.route("/drop", methods=['POST', 'GET'])
def drop():
    if request.method == 'GET':
        title = 'Claiming NFTs Here'
        return render_template("home.html", title=title)
    else:
        title = "cool"
        slp_addr = request.form["slp_addr"]
        #path = c0xffee.absurd_maker()
        # return render_template("gotcha.html", title=title, slp=slp_addr, amount=amount)
'''

if __name__ == "__main__":

    app.debug = True
    app.run(port=9487)
