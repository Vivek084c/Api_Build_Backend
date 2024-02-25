from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str="localhost"
    database_port: str="5432"
    database_password: str="vivek123"
    database_name: str="FastApi"
    database_username: str="postgres"
    secret_key: str="sdgasdg83223asdfa9sdg3dsga1231ddgds"
    algorithm: str="HS256"
    access_token_expire_minutes: int=60


settings = Settings()