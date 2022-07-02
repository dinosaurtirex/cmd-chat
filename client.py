import requests 
import threading 
import time
import os 

class Client:
    
    def __init__(self, username: str):
        self.server = "95.165.158.131"
        self.port = 80
        self.username = username 
        
        self.talk_url = f"http://{self.server}:{self.port}/talk"
        self.info_url = f"http://{self.server}:{self.port}/update"
        
        
    def send_info(self):
        
        while True:
            user_input = input("You're message: ")
            requests.post(self.talk_url, data={
                "text": f'{self.username}: {user_input}'
            })
            
            
    def update_info(self):
        last_try = None
        while True:
            time.sleep(0.05)
            r = requests.post(self.info_url)
            if last_try == r.json():
                continue 
            last_try = r.json()
            os.system("cls")
            for msg in last_try["status"]:
                print(f"{msg}\n")
            
            
    def __call__(self):
        threads = [
            threading.Thread(target=self.send_info),
            threading.Thread(target=self.update_info)
        ]
        for th in threads:
            th.start()
        
        
if __name__ == '__main__':
    c = Client(input("Who are you? \t"))
    c()