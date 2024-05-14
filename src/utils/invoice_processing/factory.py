from abc import ABC, abstractmethod

from src.settings import (
    AIHANDLER_SERVICE_TOKEN,
    AIHANDLER_SERVICE_URL,
    QUICKSPEAK_SERVICE_TOKEN,
    QUICKSPEAK_SERVICE_URL,
)


class CreateRequestData(ABC):

    def __init__(self, acc_id: str, balance: float):
        self.token: str
        self.acc_id = acc_id
        self.balance = balance

    @abstractmethod
    def create_headers() -> dict:
        pass

    @abstractmethod
    def create_url() -> str:
        pass

    @abstractmethod
    def create_body() -> dict:
        pass


class CreateImvoRequest(CreateRequestData):

    def __init__(self, acc_id, balance):
        self.token = AIHANDLER_SERVICE_TOKEN
        self.acc_id = acc_id
        self.balance = balance

    def create_headers(self):
        return {"Authorization": self.token}

    def create_url(self):
        return f"{AIHANDLER_SERVICE_URL}/{self.acc_id}/balance"

    def create_body(self):
        return {"balance": self.balance}


class CreateQuickspeakRequest(CreateRequestData):

    def __init__(self, acc_id, balance):
        self.token = QUICKSPEAK_SERVICE_TOKEN
        self.acc_id = acc_id
        self.balance = balance

    def create_headers(self):
        return {"Authorization": f"Token: {self.token}"}

    def create_url(self):
        return QUICKSPEAK_SERVICE_URL

    def create_body(self):
        return {"balance": self.balance, "account": self.acc_id}


def factory(project: CreateRequestData, acc_id: str, balance: float) -> dict:
    project = project(acc_id, balance)
    headers = project.create_headers()
    body = project.create_body()
    url = project.create_url()
    return {"body": body, "headers": headers, "url": url}