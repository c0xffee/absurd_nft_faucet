import requests
from bs4 import BeautifulSoup


def clean_data(data):

    return data


def update_data(data):
    data = clean_data(data)


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

    nft_num = int(actually_pay//nft_price)
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

    return failed, out_addr, in_addr, actually_pay, received_bch, tx_gas, tx_ago, tx_date, nft_num

    # print(len(money))
'''
url = "https://blockchair.com/bitcoin-cash/transaction/542efdb29882888dc7b1c6dd9bc2573ab4eb509e4f97930c10894a7f31e1dff1?from=bitcoin.com"
url = input()
chk_tx(url, '123')
'''
