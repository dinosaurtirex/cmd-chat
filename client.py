import threading 
import requests 
import time
import rsa 
import os 

class Client:
    
    def __init__(self, username: str):
        self.server = "95.165.158.131"
        self.port = 80
        self.username = username 
        
        self.base_url = f"http://{self.server}:{self.port}"
        
        self.talk_url = f"{self.base_url}/talk"
        self.info_url = f"{self.base_url}/update"
        self.key_url = f"{self.base_url}/get_key"

        self.pubkey = None 
        
        
    def send_info(self):
        
        while True:
            user_input = input("You're message: ")
            message = f'{self.username}: {user_input}'
            requests.post(self.talk_url, data={
                "text": rsa.encrypt(message.encode('utf8'), self.pubkey)
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
                print(f"{rsa.decrypt(msg.encode(), self.seckey)}\n")
                
                
    def _key_request(self) -> None:
        
        with requests.get(self.key_url) as r:
            with open("public_rec.pem", 'wb') as f:
                f.write(r.text.encode())
                
                
    def _remove_keys(self) -> None:
        with open('public_rec.pem', 'wb') as f:
            pass 
                
                
    def _validate_keys(self) -> None:
        
        self._key_request()
        
        with open('public_rec.pem', "rb") as f:
            first_key = f.read()
            
        self.pubkey = rsa.PublicKey.load_pkcs1(first_key)
        self._remove_keys()
        
            
    def __call__(self):
        
        self._validate_keys()
          
        threads = [
            threading.Thread(target=self.send_info),
            threading.Thread(target=self.update_info)
        ]
        
        for th in threads:
            th.start()
        
        
if __name__ == '__main__':
    c = Client("sneaky") # input("Who are you? \t")
    c()