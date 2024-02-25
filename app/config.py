from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password:str="localhost"
    databse_username:str="postgrace"
    secret_key:str="dasgasdg1232wr23hjrbw"
settings=Settings()
print(settings.database_password)
