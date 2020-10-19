from fastapi import FastAPI

from intervalUpdateDB import daily_update_db


app = FastAPI()

daily_update_db()

