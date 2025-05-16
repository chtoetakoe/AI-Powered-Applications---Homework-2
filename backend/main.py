from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Literal
import openai
import os
import math
import json
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: Literal["user", "assistant", "system", "function"]
    content: Optional[str] = None
    name: Optional[str] = None

class ChatRequest(BaseModel):
    messages: list[Message]

functions = [
    {
        "name": "calculate_mortgage",
        "description": "Calculate monthly mortgage payments",
        "parameters": {
            "type": "object",
            "properties": {
                "principal": {"type": "number"},
                "rate": {"type": "number"},
                "years": {"type": "integer"},
            },
            "required": ["principal", "rate", "years"]
        },
    },
    {
        "name": "search_product_database",
        "description": "Search a product catalog by keyword",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "default": 3},
            },
            "required": ["query"]
        },
    },
]

def calculate_mortgage(principal, rate, years):
    monthly_rate = rate / 100 / 12
    payments = years * 12
    if monthly_rate == 0:
        return round(principal / payments, 2)
    monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -payments)
    return round(monthly_payment, 2)

PRODUCTS = [
    {"name": "Office Desk", "price": 250},
    {"name": "Ergonomic Chair", "price": 180},
    {"name": "LED Desk Lamp", "price": 40},
    {"name": "Laptop Stand", "price": 55},
    {"name": "Notebook Set", "price": 15},
]

def search_product_database(query: str, max_results: int = 3):
    results = [p for p in PRODUCTS if query.lower() in p["name"].lower()]
    return results[:max_results]

function_map = {
    "calculate_mortgage": calculate_mortgage,
    "search_product_database": search_product_database,
}

@app.post("/chat")
async def chat(req: ChatRequest):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[m.dict() for m in req.messages],
        functions=functions,
        function_call="auto"
    )

    message = response.choices[0].message

    if message.get("function_call"):
        name = message.function_call.name
        arguments = json.loads(message.function_call.arguments)
        result = function_map[name](**arguments)

        req.messages.append({
            "role": "function",
            "name": name,
            "content": str(result)
        })

        
        req.messages.insert(0, {
            "role": "system",
            "content": "Only return clear, concise answers. Do not show formulas unless the user asks for detailed calculations."
        })

        follow_up = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[m if isinstance(m, dict) else m.dict() for m in req.messages]
        )

        return {"reply": follow_up.choices[0].message.content}

    return {"reply": message.content}