from flask import Flask, render_template, request, redirect, url_for
from c0xffee.chk_trans import chk_tx, show_float, chk_slp_addr, update_data, clean_data
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", NFT_price=NFT_price)


@app.route("/payment", methods=['POST'])
def payment():
    title = "Waiting FOR your Payment"
    slp_addr = request.form["slp_addr"]
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
    failed, *data = chk_tx(tx_url, bch_addr, float(bch), NFT_price)
    data = [buyer_slp, tx_url, bch, bch_addr] + data
    print(data)
    data = clean_data(data)
    update_data(data)
    if failed:
        return render_template("successful.html", data=data)
        # buyer_slp + tx_url + bch + bch_addr + str(data)
    else:
        return render_template("home.html", NFT_price=NFT_price, warning=failed)
    # render_template("dbck.html", buyer_slp=buyer_slp, tx=tx, bch=bch, bch_addr=bch_addr)
    # return buyer_slp + tx + bch + bch_addr


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
    NFT_price = 0.000001
    app.debug = True
    app.run(port=9487)
