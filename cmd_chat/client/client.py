import os 
import ast 
import time
import platform
import threading

from colorama import init
from websocket import create_connection

from cmd_chat.client.core.crypto import RSAService
from cmd_chat.client.config import (
    COLORS,
    RENDER_TIME
)


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
        self.close_response = str({
            "action": "close",
            "username": self.username
        })

    def __get_os(self) -> str:
        """ checking what kind of platform you need
        """
        if "Linux" in str(platform.platform()):
            return "Linux"
        return "Windows"

    def send_info(self):
        """ sending message to websocket
        """
        ws = create_connection(f"{self.ws_url}/talk")
        while True:
            try:
                user_input = input("You're message: ")
                message = f'{self.username}: {user_input}'
                socket_message = str({
                    "text": self._encrypt(message),
                    "username": self.username
                })
                ws.send(
                    payload=socket_message.encode()
                )
            except KeyboardInterrupt:
                ws.send(self.close_response)
                ws.close()
                quit()
            except Exception as exc:
                ws.send(self.close_response)
                ws.close()
                print("Something went wrong! ", exc)
                quit()

    def __print_message(self, message: str) -> str:
        """ generating string with message in required format
        """
        message = message.split(":")
        if message[0] == self.username:
            return COLORS["my_username_color"] + message[0] + ": " + message[1] + COLORS["text_color"]
        return message[0] + ": " + message[1] + COLORS["text_color"]

    def __clear_console(self):
        # For windows clear command its cls
        # For linux clear command its clear
        if self.__get_os() == "Linux":
            os.system("clear")
        else:
            os.system("cls")

    def __print_ip(
        self,
        ip: str
    ) -> str:
        return f"IP: " + COLORS["ip_color"] + ip + COLORS["text_color"]
    
    def __print_username(
        self,
        username: str
    ) -> str:
        return f"USERNAME: " + COLORS["ip_color"] + username + COLORS["username_color"]

    def __print_chat(self, response: list[str]) -> str:
        for i, msg in enumerate(response["messages"]):
            actual_message = self._decrypt(msg)
            if i == 0:
                for user in response["users_in_chat"]:
                    print(self.__print_ip(user.split(",")[0]))
                    print(self.__print_username(user.split(",")[1]))
                print(f"\n{self.__print_message(actual_message)}")
            else:
                print(f"{self.__print_message(actual_message)}")

    def update_info(self):
        """ connecting to websocket,
            wating for updates, 
            updating every RENDER_TIME seconds
        """
        ws = create_connection(f"{self.ws_url}/update")
        last_try = None
        while True:
            try:
                time.sleep(RENDER_TIME)
                response = ast.literal_eval(ws.recv().decode('utf-8'))
                if last_try == response:
                    continue
                last_try = response
                self.__clear_console()
                if len(last_try["messages"]) > 0:
                    self.__print_chat(
                        response = last_try
                    )
            except KeyboardInterrupt:
                ws.send(self.close_response)
                ws.close()
                quit()
            except Exception as exc:
                ws.send(self.close_response)
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
