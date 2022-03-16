from pydantic import BaseModel


class ConvertFromTo(BaseModel):
    valute_from: str
    valute_to: str
    amount: float


class Valute(BaseModel):
    name: str
    value: float
    actual_date: int
