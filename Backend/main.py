from datetime import datetime
from io import BytesIO
from typing import Union
import csv
from fastapi import FastAPI, Body, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

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
        print(add)
        pd.concat([df, pd.DataFrame([add], columns=add.index)]).reset_index(drop=True)
    print(out)
