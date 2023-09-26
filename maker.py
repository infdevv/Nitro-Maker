import requests
import random
import string
import os
import time
from time import sleep

# Lets make a cool banner

import pyfiglet


class CodeGenerator:
    def __init__(self, code_type: str, use_proxies=None, num_codes=None):
        self.type = code_type
        self.num_codes = num_codes
        self.use_proxies = use_proxies
        self.session = requests.Session()
        self.proxy_api = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"

    def __get_proxies(self):
        req = self.session.get(self.proxy_api).text
        if req:
            with open("./data/proxies.txt", "a+") as file:
                file.truncate(0)
                for proxy in req.split("\n"):
                    proxy = proxy.strip()
                    proxy = f"https://{proxy}"
                    file.write(f"{proxy}\n")

    def generate_codes(self, scrape=None):
        if scrape == "True":
            self.__get_proxies()

        for _ in range(int(self.num_codes)):
            try:
                if self.use_proxies == "True":
                    prox = {"http": random.choice(open("./data/proxies.txt", "r").read().splitlines())}
                else:
                    prox = None

                if self.type == "boost":
                    code = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(24)])
                else:
                    code = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)])

                req = self.session.get(f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                                       proxies=prox, timeout=10).status_code

                if req == 200:
                    print(f"[ Valid ]: https://discordapp.com/api/entitlements/gift-codes/{code}")
                    with open("valid.txt", "w+") as file:
                        file.write(f"Valid: https://discordapp.com/api/entitlements/gift-codes/{code}\n")
                    break
                if req == 404:
                    print(f"[ Invaild ]: {code}")
                if req == 429:
                    print(f"[ Rate Limited ]: {code}")
                    print("Retrying in 50 seconds.")
                    time.sleep(50)

            except Exception as e:
                print(f"Error: {e}")

        print(f"Successfully checked {self.num_codes} codes.")
        os.system("clear")


if __name__ == "__main__":
    # Banner time ( not hammer time )
    print(pyfiglet.figlet_format("GEN v1"))

    print(" A lite version of https://github.com/lnxcz/nitro-generator that runs constantly \n Writes to valid.txt if the code is valid \n Makes Classic codes \n")

    while True:
        code_type = "classic"
        use_proxies = False

        scrape_proxies=False


        num_codes = 999999
        CodeGenerator(code_type, use_proxies, num_codes).generate_codes(scrape=scrape_proxies)
