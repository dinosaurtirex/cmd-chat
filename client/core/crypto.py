import os
import rsa
import requests
from cryptography.fernet import Fernet
from core.abs.abs_crypto import CryptoService


class RSAService(CryptoService):
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.symmetric_key = None
        self.fernet = None
        self.private_key_name = "private.pem"
        self.public_key_name = "public.pem"

        self.keys_path: list[str] = []
        self._generate_keys()

    def _encrypt(self, message: str) -> str:
        return self.fernet.encrypt(message.encode())

    def _decrypt(self, message: str) -> str:
        return self.fernet.decrypt(message.encode()).decode("utf-8")

    def _request_key(self, url: str, username: str):
        data = {
            "pubkey": self._open_generated_file(self.public_key_name),
            "username": username
        }
        r = requests.get(url, data=data, stream=True)
        message = r.raw.read(999)
        self.symmetric_key = rsa.decrypt(message, self.private_key)
        self.fernet = Fernet(self.symmetric_key)

    def __update_keys_path(self, path_list: list[str]) -> None:
        for file in path_list:
            self.keys_path.append(file)

    def __write_generated_key(self, name: str, key) -> None:
        with open(name, "wb") as f:
            f.write(key.save_pkcs1())

    def _open_generated_file(self, name: str) -> bytes:
        with open(name, "rb") as f:
            return f.read()

    def _generate_keys(self):
        (public_key, private_key) = rsa.newkeys(512)
        self.__write_generated_key(self.private_key_name, private_key)
        self.__write_generated_key(self.public_key_name, public_key)
        self.private_key = rsa.PrivateKey.load_pkcs1(
            self._open_generated_file(self.private_key_name)
        )
        self.public_key = rsa.PublicKey.load_pkcs1(
            self._open_generated_file(self.public_key_name)
        )
        self.__update_keys_path(["public.pem", "private.pem"])

    def _get_generated_keys(self):
        return self.private_key, self.public_key

    def _remove_keys(self):
        for key in self.keys_path:
            os.remove(key)
