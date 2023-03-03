import requests
import warnings
import os
from bs4 import BeautifulSoup
from argparse import ArgumentParser

def login(user: str, passwd: str):
    warnings.filterwarnings("ignore")
    reqObj = requests.Session()
    loginHtml = reqObj.get('https://panel.ct8.pl/login/',verify=False)
    soup = BeautifulSoup(loginHtml.text, 'lxml')
    token = soup.select_one('#language_modal > div > div > form > div.modal-body > input[type=hidden]')['value']
    req = reqObj.post('https://panel.ct8.pl/login/',data={
        'csrfmiddlewaretoken': token,
        'username': user,
        'password': passwd
    },verify=False)
    if req.status_code == 302:
        print(f'{user} Login Success!')
    else:
        req.raise_for_status()
    req = reqObj.get('https://panel.ct8.pl/',verify=False)
    if req.status_code == 200:
        print(f'{user} Extend Success!')
    else:
        req.raise_for_status()
    return 0

def main():
    parser = ArgumentParser(
        description='Extend Ct8.pl Account Automatically.'
    )
    parser.add_argument('-u','--user',help="Ct8.pl Usernames,Split By ':'",required=True)
    parser.add_argument('-p','--passwd',help="Passwords Of Ct8.pl Accounts,Split By ':'",required=True)
    args = parser.parse_args()
    if ':' in args.user:
        users = args.user.split(':')
        passwds = args.passwd.split(':')
        if len(users) != len(passwds):
            print('Your Usernames And Passwords Cannot Correspond To One By One!')
            return 1
        for i in range(len(users)):
            login(users[i], passwds[i])
    else:
        login(args.user, args.passwd)

if __name__ == '__main__':
    main()
