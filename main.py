# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected inputs
class CompoundInterestRequest(BaseModel):
    principal: float
    rate: float
    years: int
    compounds_per_year: int = 12

# Create the calculation endpoint
@app.post("/api/compound-interest")
def calculate_compound_interest(data: CompoundInterestRequest):
    # Formula: A = P(1 + r/n)^(nt)
    r_decimal = data.rate / 100
    amount = data.principal * (1 + r_decimal / data.compounds_per_year) ** (data.compounds_per_year * data.years)
    interest_earned = amount - data.principal
    
    return {
        "future_value": round(amount, 2),
        "interest_earned": round(interest_earned, 2)
    }

# Run with: uvicorn main:app --reload
