import os 
import time
import platform
import threading
from colorama import init
from colorama import Fore
from websocket import create_connection
from core.crypto import RSAService


init()


class Client(RSAService):

    def __init__(self, server: str, port: int, username: str):
        super().__init__()
        # Server info 
        self.server = server
        self.port = port
        self.username = username
        # Urls 
        self.base_url = f"http://{self.server}:{self.port}"
        self.talk_url = f"{self.base_url}/talk"
        self.info_url = f"{self.base_url}/update"
        self.key_url = f"{self.base_url}/get_key"
        self.ws_url = f"ws://{self.server}:{self.port}"

    def __get_os(self) -> str:
        if "Linux" in str(platform.platform()):
            return "Linux"
        return "Windows"

    def send_info(self):
        ws = create_connection(f"{self.ws_url}/talk")
        while True:
            try:
                user_input = input("You're message: ")
                message = f'{self.username}: {user_input}'
                socket_message = str({
                    "text": self._encrypt(message),
                    "username": self.username
                })
                ws.send(payload=socket_message.encode())
            except KeyboardInterrupt:
                ws.close()
                quit()
            except Exception as exc:
                ws.close()
                print("Something went wrong! ", exc)
                quit()

    def print_message(self, message: str) -> str:
        message = message.split(":")
        if message[0] == self.username:
            return Fore.MAGENTA + message[0] + ": " + message[1] + Fore.WHITE
        return message[0] + ": " + message[1] + Fore.WHITE

    def __clear_console(self):
        # For windows clear command its cls
        # For linux clear command its clear
        if self.__get_os() == "Linux":
            os.system("clear")
        else:
            os.system("cls")

    def update_info(self):
        ws = create_connection(f"{self.ws_url}/update")
        last_try = None
        while True:
            try:
                time.sleep(0.05)
                r = eval(ws.recv())
                if last_try == r:
                    continue
                last_try = r
                self.__clear_console()
                if len(last_try['status']) > 0:
                    for i, msg in enumerate(last_try["status"]):
                        actual_message = self._decrypt(msg)
                        if i == 0:
                            for user in last_try["users_in_chat"]:
                                print("IP:", Fore.MAGENTA + user.split(",")[0] + Fore.WHITE)
                                print("USERNAME: ", Fore.GREEN + user.split(",")[1] + Fore.WHITE)
                            print(f"\n{self.print_message(actual_message)}")
                        else:
                            print(f"{self.print_message(actual_message)}")
            except KeyboardInterrupt:
                ws.close()
                quit()
            except Exception as exc:
                ws.close()
                print("Something went wrong! ", exc)
                quit()

    def _validate_keys(self) -> None:
        self._request_key(self.key_url, self.username)
        self._remove_keys()

    def run(self):
        # Running two threads,
        # One for sending info
        # Second one for updating info
        self._validate_keys()
        threads = [
            threading.Thread(target=self.send_info),
            threading.Thread(target=self.update_info)
        ]
        for th in threads:
            th.start()


if __name__ == '__main__':
    Client(
        server=input("server ip:\n"),
        port=int(input("server port: \n")),
        username=input("username:\n").replace(" ", "").lower()
    ).run()
