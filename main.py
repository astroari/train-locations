from fastapi import FastAPI, Request, HTTPException, Query
from typing_extensions import Annotated
import pandas as pd
import io
from extractors import *


app = FastAPI()

PARSERS = {
       "inform@eurologistic.su": parse_eurologistic,
       "stg-host-6@railsoft.ru": parse_railsoft,
       "disl@incomtrans.su": parse_incomtrans,
       "disl@ilsi.pro": parse_ilsi,
       "e.mironova@ultradecor.com": parse_ultradecor
   }

def dispatch(sender_email, df):
       parser = PARSERS.get(sender_email)
       if parser is None:
           raise ValueError(f"Unknown sender: {sender_email}")
       return parser(df)

@app.get("/")
def home():
    return {"message": "Welcome to my test API"}


@app.post("/process")
async def process_file(request: Request, sender_email: Annotated[str, Query(title="Sender Email")], date_received: Annotated[str, Query(title="Date Received")]):
    contents = await request.body()  # bytes
    df = pd.read_excel(io.BytesIO(contents), header=None)
    try:
        data = dispatch(sender_email=sender_email, df=df)
        for record in data:
             record["date_received"] = date_received
             record["sender_email"] = sender_email
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return data