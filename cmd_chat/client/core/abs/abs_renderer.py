from abc import ABC, abstractmethod


class ClientRenderer(ABC):

    @abstractmethod
    def print_message(self, message: str) -> str:
        raise NotImplementedError("Need to implement print_message")

    @abstractmethod
    def clear_console(self, message: str) -> str:
        raise NotImplementedError("Need to implement clear_console")

    @abstractmethod
    def print_ip(self, url: str, username: str):
        raise NotImplementedError("Need to implement print_ip")

    @abstractmethod
    def print_username(self):
        raise NotImplementedError("Need to implement print_username")

    @abstractmethod
    def print_chat(self) -> list[str]:
        raise NotImplementedError("Need to implement print_chat")
