"""FastAPI implementation of the FinTrust transaction API."""

import uuid
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionIn(BaseModel):
    account_id: str = Field(min_length=1)
    amount: float = Field(gt=0, le=1_000_000)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    description: str = ""

    @field_validator("account_id")
    @classmethod
    def account_id_is_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Account ID cannot be blank")
        return value


class TransactionOut(TransactionIn):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: str
    created_at: str


class StatusUpdate(BaseModel):
    status: Literal["approved", "rejected"]


app = FastAPI(title="FinTrust Transaction API", version="1.0.0")
app.state.transactions = []


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = request.headers.get(
        "X-Request-ID", str(uuid.uuid4())
    )
    return response


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/transactions", response_model=TransactionOut, status_code=201)
async def create_transaction(body: TransactionIn):
    transaction = {
        "id": str(uuid.uuid4()),
        **body.model_dump(),
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    app.state.transactions.append(transaction)
    return transaction


@app.get("/transactions", response_model=list[TransactionOut])
async def list_transactions(account_id: str | None = Query(default=None)):
    if account_id:
        return [
            item for item in app.state.transactions if item["account_id"] == account_id
        ]
    return app.state.transactions


def _find_transaction(transaction_id):
    transaction = next(
        (item for item in app.state.transactions if item["id"] == transaction_id),
        None,
    )
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.get("/transactions/{transaction_id}", response_model=TransactionOut)
async def get_transaction(transaction_id: str):
    return _find_transaction(transaction_id)


@app.patch("/transactions/{transaction_id}/status", response_model=TransactionOut)
async def update_status(transaction_id: str, body: StatusUpdate):
    transaction = _find_transaction(transaction_id)
    transaction["status"] = body.status
    return transaction
