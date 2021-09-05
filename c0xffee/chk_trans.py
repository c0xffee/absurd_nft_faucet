import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
import csv
import shutil
import os


NFT_price = 0.000001


def backup():
    fname = 'all_payment.csv'
    dir = 'backup'
    new_name = datetime.now().isoformat().split('.')[
        0].replace(':', '-')+'.csv'
    shutil.copyfile(fname, dir+os.sep+new_name)


def update_finished_nft_num(tx, num):
    fname = 'all_payment.csv'
    r = csv.reader(open(fname))  # Here your csv file
    lines = list(r)
    print(lines)
    for i in range(len(lines)):
        if lines[i][0] == tx:
            print(lines[i])
            lines[i][-1] = str(num)
    print(lines)

    writer = csv.writer(open(fname, 'w', newline=''))
    writer.writerows(lines)


def headsha(sth):
    return hashlib.sha256(sth.encode('utf-8')).hexdigest()


def chk_tx_exist(tx):
    fname = 'all_payment.csv'
    with open(fname, 'r') as f:
        sth = f.read()
    if tx in sth:
        return True
    else:
        return False


def update_data(data):
    #data = clean_data(data)
    #schema = 'web_slp_addr,web_tx_link,web_bch,web_bch_addr,chain_out_bch_addr,chain_in_bch_addr,chain_actually_pay,chain_actually_get,chain_gas,chain_tx_ago,chain_tx_datetime,verified_nft_amount'
    fname = 'all_payment.csv'
    sdata = ','.join([str(i) for i in data])
    with open(fname, 'a+') as f:
        f.write(sdata+'\n')


def chk_slp_addr(slp_addr):
    wht_li = list(range(10))
    illegal = 0
    if len(slp_addr) != 55:
        illegal = 1
    if slp_addr[:13] != 'simpleledger:':
        illegal = 1
    if len([s for s in slp_addr[13:] if not (s.islower or s.isdigit())]) != 0:
        illegal = 1
    return illegal


def show_float(flo):
    return ('%.20f' % round(flo, 10)).rstrip('0')


def _2_satoshi(bch):
    return int(bch*pow(10, 8))


def beauti4(res):
    soup = BeautifulSoup(res.text, 'html.parser')

    addrs = soup.find_all('a', class_="hash", href=True)
    out_addr, in_addr = [addr['href'].split('/')[-1] for addr in addrs]
    data = soup.find_all('span', class_="wb-ba", text=True)
    received_bch = float(data[0].text)
    tx_ago = data[4].text
    tx_date = data[5].text
    tx_gas = float(data[2].text)
    sent_bch = received_bch + tx_gas
    sent_bch = round(sent_bch, 10)
    '''
    print(received_bch)
    print(tx_ago)
    print(tx_date)
    print(tx_gas)
    print(sent_bch)
    '''

    # print(money)
    # title = soup.find('h1', class_='entry-title').text

    return out_addr, in_addr, sent_bch, received_bch, tx_gas, tx_ago, tx_date


def chk_tx(url, temp_addr, send_bch, nft_price):
    res = requests.get(url)
    out_addr, in_addr, actually_pay, received_bch, tx_gas, tx_ago, tx_date = beauti4(
        res)
    tx_date = datetime.strptime(tx_date, "%b %d, %Y %I:%M %p").isoformat()[:-3]

    nft_num = int(actually_pay//nft_price)
    tx_no = url.split('/')[-1]
    failed = ''
    log = ''
    if 'seconds' not in tx_ago:
        failed += 'time failed;'
    if temp_addr != out_addr:
        failed += 'unmached wallet;'
    if in_addr != 'qzhppf89yx7d3fsaswceptz88xgf6p2j6v7ylllmxx':
        failed += 'This is not pay to me TT;'
    if actually_pay != send_bch:
        log = "actually_pay:%d != send_bch:%d" % (
            _2_satoshi(actually_pay), _2_satoshi(send_bch))
    '''
    if sent_bch != send_bch:
        if abs(send_bch - sent_bch) > sent_bch/100:
            failed = 1
    '''

    return failed, tx_no, out_addr, in_addr, actually_pay, received_bch, tx_gas, tx_ago, tx_date, nft_num


    # print(len(money))
'''
url = "https://blockchair.com/bitcoin-cash/transaction/542efdb29882888dc7b1c6dd9bc2573ab4eb509e4f97930c10894a7f31e1dff1?from=bitcoin.com"
url = input()
chk_tx(url, '123')
'''
