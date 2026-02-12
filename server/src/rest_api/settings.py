import os


class Settings:
    SERVER_MODE = os.getenv("APP_SERVER_MODE", "prod").lower()

    @property
    def is_dev(self) -> bool:
        return self.SERVER_MODE == "dev"


settings = Settings()
