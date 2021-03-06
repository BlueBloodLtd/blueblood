from time import sleep

from requests import Session, get
from bs4 import BeautifulSoup

#@ TODO breaking changes, this wouldn't work

ETHERSCAN_URL = "https://etherscan.io/"


def getPage(sess, *args):
    url = ETHERSCAN_URL + '/'.join(args)
    print("Retrieving", url)
    return BeautifulSoup(sess.get(url).text, 'html.parser')


def getContracts(sess, page=1):
    print('Page:', page)
    try:
        table = getPage(sess, 'contractsVerified', str(int(page))).find('table')
        headings = [X.text for X in table.find('thead').find_all('th')]
        lst = [dict(zip(headings, [X.text.strip() for X in row.find_all('td')])) for row in table.find('tbody').find_all('tr')]
    except Exception as err:
        print(err)
        lst = []
    return lst


def saveContract(sess, contract):
    page = getPage(sess, 'address', contract['Address']).find('pre')
    try:
        cur = conn.cursor()
        sql = "INSERT INTO verified_contracts (addr, code) VALUES (%s, %s);"
        # print('Code' , page.contents[0])
        cur.execute(sql, (contract['Address'], page.contents[0]))
        conn.commit()
        cur.close()
    except Exception as err:
        print(err)
        conn.rollback()


def main():
    resp = get(ETHERSCAN_URL + "contractsVerified")
    sess = Session()

    pageno = 805
    while True:
        pageno += 1
        for contract in getContracts(sess, pageno):
            try:
                saveContract(sess, contract)
            except Exception as err:
                print(err)
            sleep(5)
    conn.close()

if __name__ == "__main__":
    main()
