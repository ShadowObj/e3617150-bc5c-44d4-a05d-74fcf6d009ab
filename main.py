from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from argparse import ArgumentParser

def extend(broswer: Chrome, account: str,passwd: str, seq: int):
    print(f"Now Login With Account No.{seq+1}")
    broswer.get("https://panel.ct8.pl")
    broswer.implicitly_wait(30)
    broswer.execute_script('document.cookie="django_language=en";')
    broswer.find_element(By.NAME, "username").send_keys(account)
    broswer.find_element(By.NAME, "password").send_keys(passwd)
    broswer.find_element(By.ID, "submit").click()
    broswer.implicitly_wait(30)
    expiration = broswer.find_element(By.XPATH, '//*[@id="dashboard"]/div[1]/div[1]/div/table/tbody/tr[3]/td[2]').get_attribute("textContent")
    if not expiration == "":
        print(f"Expiration Date Of No.{seq+1}: {expiration}")
    else:
        print(f"No.{seq+1} Expire Failed")
    return 0

def main():
    parser = ArgumentParser(
        description="Ct8pl Automatic Expirer"
    )
    parser.add_argument("-u","--user",help='Usernames(Split By "::")',required=True,type=str)
    parser.add_argument("-p","--passwd",help='Passwords(Split By "::")',required=True,type=str)
    parser.add_argument("-DRV","--driver",help="Chromedriver Path(Default in $PATH)",required=False,type=str)
    parser.add_argument("--noheadless",help="Run Chrome Without Headless Mode",required=False,action="store_true")
    args = parser.parse_args()
    chromeOptions = Options()
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disabled-gpu")
    chromeOptions.add_argument("--window-size=1200x600")
    chromeOptions.add_argument("blink-settings=imagesEnabled=false")
    if not args.noheadless:
        chromeOptions.add_argument("--headless")
    if args.driver:
        broswer = Chrome(
            executable_file=args.driver,
            options=chromeOptions)
    else:
        broswer = Chrome(options=chromeOptions)
    if "::" in args.user:
        users = args.user.split("::")
        passwds = args.passwd.split("::")
        if not len(users) == len(passwds):
            print("Check The Usernames And Passwords!")
            return
        for i in range(0,len(users)):
            extend(broswer, users[i], passwds[i], i)
    else:
        extend(broswer, args.user, args.passwd, 0)
 
if __name__ == "__main__":
    main()
