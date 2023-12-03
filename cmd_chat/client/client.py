import ast 
import time
import threading

from websocket import create_connection

from cmd_chat.client.core.crypto import RSAService
from cmd_chat.client.core.default_renderer import DefaultClientRenderer
from cmd_chat.client.core.rich_renderer import RichClientRenderer

from cmd_chat.client.config import RENDER_TIME


class Client(RSAService, RichClientRenderer):

    def __init__(
        self, 
        server: str, 
        port: int, 
        username: str
    ):
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
        # Threads 
        self.__stop_threads = False 

    def send_info(self):
        """ sending message to websocket
        """
        ws = create_connection(f"{self.ws_url}/talk")
        while not self.__stop_threads:
            try:
                user_input = input("You're message: ")
                if user_input == "q":
                    self.__stop_threads = True 
                message = f'{self.username}: {user_input}'
                socket_message = str({
                    "text": self._encrypt(message),
                    "username": self.username
                })
                ws.send(payload=socket_message.encode())
            except KeyboardInterrupt:
                ws.send(self.close_response)
                ws.close()
                self.__stop_threads = True 
            except Exception as exc:
                ws.send(self.close_response)
                ws.close()
                print("Something went wrong! ", exc)
                self.__stop_threads = True 
                raise exc 

    def update_info(self):
        """ connecting to websocket,
            wating for updates, 
            updating every RENDER_TIME seconds
        """
        ws = create_connection(f"{self.ws_url}/update")
        last_try = None
        while not self.__stop_threads:
            try:
                time.sleep(RENDER_TIME)
                response = ast.literal_eval(ws.recv().decode('utf-8'))
                if last_try == response:
                    continue
                last_try = response
                self.clear_console()
                if len(last_try["messages"]) > 0:
                    self.print_chat(response = last_try)
            except KeyboardInterrupt:
                ws.send(self.close_response)
                ws.close()
                self.__stop_threads = True 
            except ConnectionAbortedError:
                # Reconnect if somehow client was disconnected
                ws = create_connection(f"{self.ws_url}/update")
                continue
            except Exception as exc:
                ws.send(self.close_response)
                ws.close()
                print("Something went wrong! ", exc)
                self.__stop_threads = True 
                raise exc 
            
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
