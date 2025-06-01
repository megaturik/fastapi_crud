from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str

    class Config:
        env_file = ".env"

    def get_database_url(self):
        return (
            f'postgresql://{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:5432/{self.postgres_db}'
        )


settings = Settings()
