import base64
from datetime import datetime
from io import BytesIO
from typing import Union
import csv
from fastapi import FastAPI, Body, Request, File, Response, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
from requests import request
import dataframe_image as dfi

app = FastAPI()
templates = Jinja2Templates(directory="htmlDirectory")

out = pd.DataFrame(columns=('Customer Id','MM/YYYY','MinBalance','MaxBalance','EndingBalance'))

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.post("/submitCSV")
async def handleCSV(file: bytes = File(...)):
    global out
    df = pd.read_csv(BytesIO(file))
    ids = df["Customer Id"].dropna()
    ids = ids.unique()
    
    for id in ids:
        cust = df[df['Customer Id'] == id]
        CustomerId = id
        MMYYYY = cust['Date'].iloc[0]
        MMYYYY = datetime.strptime(MMYYYY, "%m/%d/%Y").strftime("%m/%Y")

        EndingBalance = 0
        MinBalance = float('inf')
        MaxBalance = float('-inf')
        for transaction in cust['Amount']:
            EndingBalance += transaction
            if MinBalance > EndingBalance:
                MinBalance = EndingBalance
            if MaxBalance < EndingBalance:
                MaxBalance = EndingBalance
        add = pd.Series({'Customer Id':CustomerId,'MM/YYYY':MMYYYY,'MinBalance':MinBalance,'MaxBalance':MaxBalance,'EndingBalance':EndingBalance})
        out = out.append(add, ignore_index=True)
    df_styled = out
    dfi.export(df_styled,"mytable.png")
        

@app.get("/getSummary")
def getSummary():
    global out
    
    return FileResponse("mytable.png", media_type='image/png')