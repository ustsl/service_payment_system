import enum
import os

from dotenv import load_dotenv
from envparse import Env

env = Env()

load_dotenv()


#### LOAD ENV DATA

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")

DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")


DB_NAME_TEST = os.getenv("DATABASE_NAME_TEST")
DB_USER_TEST = os.getenv("DATABASE_USER_TEST")
DB_PASSWORD_TEST = os.getenv("DATABASE_PASSWORD_TEST")
DB_HOST_TEST = os.getenv("DATABASE_HOST_TEST")
DB_PORT_TEST = os.getenv("DATABASE_PORT_TEST")


AIHANDLER_PAYMENT_TOKEN = os.getenv("AIHANDLER_PAYMENT_TOKEN")
QUICKSPEAK_PAYMENT_TOKEN = os.getenv("QUICKSPEAK_PAYMENT_TOKEN")

AIHANDLER_SERVICE_TOKEN = os.getenv("AIHANDLER_SERVICE_TOKEN")
QUICKSPEAK_SERVICE_TOKEN = os.getenv("QUICKSPEAK_SERVICE_TOKEN")

AIHANDLER_SERVICE_URL = os.getenv("AIHANDLER_SERVICE_URL")
QUICKSPEAK_SERVICE_URL = os.getenv("QUICKSPEAK_SERVICE_URL")


# DATABASE PRESET

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}",
)

MAIN_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


# SERVICE PRESET


class PaymentSystems(enum.Enum):
    CRYPTOCLOUD = "cryptocloud"
    ROBOKASSA = "robokassa"


class ServiceSystems(enum.Enum):
    LINGOBOT = "lingobot"
    QUICKSPEAK = "quickspeak"
    IMVO = "imvo"


# ADDITIONAL

PAGINATION_PAGE_SIZE = 30
