import re
import requests
from argparse import ArgumentParser

def extend(username: str,passwd: str, seq: int, verify = True, showtoken = False):
    default_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "Origin": "https://panel0.serv00.com",
        "Referer": "https://panel0.serv00.com/login/?next=/"
    }
    # request.Session can keep Cookie by itself
    client = requests.Session()
    client.cookies.set("django_language","en")
    print(f"Now Login With Account No.{seq+1}")
    res = client.get("https://panel0.serv00.com/login/?next=/", verify=verify)
    pattern = re.compile('[a-zA-Z0-9]{64}')
    csrf_middleware_token = pattern.findall(res.text)[0]
    if showtoken:
        print(f"CSRF_TOKEN: {client.cookies.get('csrftoken')}")
        print(f"CSRF_MIDDLEWARE_TOKEN: {csrf_middleware_token}")

    res = client.post("https://panel0.serv00.com/login/",{
        "csrfmiddlewaretoken": csrf_middleware_token,
        "username": username,
        "password": passwd,
        "next": "/"
    }, headers=default_header,verify=verify)
    if (not "Please enter a correct username and password. Note that both fields may be case-sensitive." in res.text) & res.ok:
        print(f"Login Succeed! Code:{str(res.status_code)}")
    else:
        print("Login Failed! Check Your Username And Password.")
#        print(f"Response: {res.text}")
        return

    res = client.get("https://panel0.serv00.com/dashboard",headers=default_header,verify=verify)
    if res.ok:
        print(f"Succeed to Get Dashboard Data!")
    else:
        print(f"Failed to Get Dashboard Data! Code:{str(res.status_code)}")
        print(f"Response: {res.text}")
    print(f"Expire To {re.search('[A-Za-z.]+ [0-9:, ]+ [a-z.]+', res.text).group(0)}")

def main():
    parser = ArgumentParser(
        description="Serv00.com Free Server Extender"
    )
    parser.add_argument("-U","--user",help='Usernames(Split By "::")',required=True,type=str)
    parser.add_argument("-P","--passwd",help='Passwords(Split By "::")',required=True,type=str)
    parser.add_argument("--showtoken",action="store_true",help="Show CSRF_TOKEN and CSRF_MIDDLEWARE_TOKEN(For Debug)")
    parser.add_argument("--noverify",action="store_false",help="Verify Server-side TLS Cert Or Not(For Debug)")
    args = parser.parse_args()
    if "::" in args.user:
        users = args.user.split("::")
        passwds = args.passwd.split("::")
        if not len(users) == len(passwds):
            print("Check The Usernames And Passwords!")
            return
        for i in range(0,len(users)):
            extend(users[i], passwds[i], i, args.noverify, args.showtoken)
    else:
        extend(args.user, args.passwd, 0, args.noverify, args.showtoken)

if __name__ == "__main__":
    main()