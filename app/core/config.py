import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_URL = os.getenv('DB_URL')

class Settings: 
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
    # DATABASE_URL = f"mysql+pymysql://petdev:petdev@raza-pets-db:3306/petdev"
    # DATABASE_URL = f"mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>"
    # DATABASE_URL = f"mysql+mysqldb://root@/pet-db?unix_socket=/cloudsql/proto3swarch:ins-pet-db"
    # DATABASE_URL = DB_URL
settings = Settings()
