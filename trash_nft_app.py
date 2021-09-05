from flask import Flask, render_template, request, redirect, url_for
from c0xffee.chk_trans import chk_tx, show_float, chk_slp_addr, update_data, chk_tx_exist, headsha, update_finished_nft_num, backup, get_nft_price
import csv

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    NFT_price = get_nft_price()
    return render_template("home.html", NFT_price=NFT_price)


@app.route("/payment", methods=['POST'])
def payment():
    title = "Waiting FOR your Payment"
    slp_addr = request.form["slp_addr"]
    NFT_price = get_nft_price()
    if chk_slp_addr(slp_addr):
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


@app.route("/dbck", methods=['POST'])
def dbck():
    buyer_slp = request.form["buyer_slp"]
    tx_url = request.form["tx"]
    bch = request.form["bch"]
    bch_addr = request.form["bch_addr"]
    NFT_price = get_nft_price()    
    failed, *data = chk_tx(tx_url, bch_addr, float(bch), NFT_price)
    data = [data[0], buyer_slp, tx_url, bch, bch_addr] + data[1:] + [0]
    print(data)
    if chk_tx_exist(data[0]):
        warning = "Paymant already Finished"
        return render_template("home.html", NFT_price=NFT_price, warning=failed)

    update_data(data)
    r = data
    schema = ['tx_no', 'web_slp_addr', 'web_tx_link',
              'chain_actually_pay', 'chain_tx_datetime', 'verified_nft_amount', 'finish_num']
    order_data = [r[0], r[1], r[2], r[7], r[11], r[12]]
    leng = len(order_data)
    if failed:
        return render_template("successful.html", data=order_data, schema=schema, leng=leng)
        # buyer_slp + tx_url + bch + bch_addr + str(data)
    else:
        return render_template("home.html", NFT_price=NFT_price, warning=failed)
    # render_template("dbck.html", buyer_slp=buyer_slp, tx=tx, bch=bch, bch_addr=bch_addr)
    # return buyer_slp + tx + bch + bch_addr


@app.route("/all_payment")
def all_payment():
    fname = 'all_payment.csv'
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
