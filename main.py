from app import app
from routes.api import v1 as _
from dotenv import load_dotenv

load_dotenv(".env")

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
