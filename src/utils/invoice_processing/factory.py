from abc import ABC, abstractmethod

from src.settings import (
    AIHANDLER_SERVICE_TOKEN,
    AIHANDLER_SERVICE_URL,
    QUICKSPEAK_SERVICE_TOKEN,
    QUICKSPEAK_SERVICE_URL,
    AIHANDLER_PAYMENT_TOKEN,
    QUICKSPEAK_PAYMENT_TOKEN,
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
    def create_token() -> str:
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

    def create_token(self):
        return AIHANDLER_PAYMENT_TOKEN


class CreateQuickspeakRequest(CreateRequestData):

    def __init__(self, acc_id, balance):
        self.token = QUICKSPEAK_SERVICE_TOKEN
        self.acc_id = acc_id
        self.balance = balance

    def create_headers(self):
        return {"Authorization": f"{self.token}"}

    def create_url(self):
        return f"https://api.qsbot.app/v1/payments/increase/{self.acc_id}/"

    def create_body(self):
        return {"amount": self.balance}

    def create_token(self):
        return QUICKSPEAK_PAYMENT_TOKEN


def factory(project: CreateRequestData, acc_id: str, balance: float) -> dict:
    project = project(acc_id, balance)
    headers = project.create_headers()
    body = project.create_body()
    url = project.create_url()
    token = project.create_token()
    return {"body": body, "headers": headers, "url": url, "token": token}
