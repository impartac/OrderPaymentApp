import os

import dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


config_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(config_dir)
root = os.path.dirname(src_dir)
dev = os.path.join(root, 'dev', '.env')
dotenv.load_dotenv(dotenv_path=dev)


class Settings:
    LOGGER_LEVEL: str = os.getenv('LOGGER_LEVEL', 'INFO')

    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'db')
    POSTGRES_PORT: str = os.getenv('DB_PORT', '5432')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'DB')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postrges')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    
    KAFKA_URL: str = os.getenv('KAFKA_URL', 'kafka:9002')
    KAFKA_ORDER_MESSAGES_TOPIC: str = os.getenv('KAFKA_ORDER_MESSAGES_TOPIC', 'order_create_messages')
    KAFKA_PAYMENT_MESSAGE_TOPIC: str = os.getenv('KAFKA_PAYMENT_MESSAGE_TOPIC', 'payment_messages')

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()

async_engine = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10
)

session_maker = async_sessionmaker(
    bind=async_engine,
)

# ░░░░░░░░░░░░░░░░░░░░
# ░░░░░ЗАПУСКАЕМ░░░░░░░
# ░ГУСЯ░▄▀▀▀▄░РАБОТЯГИ░░
# ▄███▀░◐░░░▌░░░░░░░░░
# ░░░░▌░░░░░▐░░░░░░░░░
# ░░░░▐░░░░░▐░░░░░░░░░
# ░░░░▌░░░░░▐▄▄░░░░░░░
# ░░░░▌░░░░▄▀▒▒▀▀▀▀▄
# ░░░▐░░░░▐▒▒▒▒▒▒▒▒▀▀▄
# ░░░▐░░░░▐▄▒▒▒▒▒▒▒▒▒▒▀▄
# ░░░░▀▄░░░░▀▄▒▒▒▒▒▒▒▒▒▒▀▄
# ░░░░░░▀▄▄▄▄▄█▄▄▄▄▄▄▄▄▄▄▄▀▄
# ░░░░░░░░░░░▌▌░▌▌░░░░░
# ░░░░░░░░░░░▌▌░▌▌░░░░░
# ░░░░░░░░░▄▄▌▌▄▌▌░░░░░