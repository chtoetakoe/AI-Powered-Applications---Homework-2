from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Literal
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables (like your OpenAI API key)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create the FastAPI app
app = FastAPI()

# Enable CORS so your frontend can talk to the backend without errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow any frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# A single chat message
class Message(BaseModel):
    role: Literal["user", "assistant", "system", "tool"]
    content: Optional[str] = None
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

# A list of messages sent to the chat endpoint
class ChatRequest(BaseModel):
    messages: list[Message]



def calculate_mortgage(principal, rate, years):
    """Calculate the monthly mortgage payment."""
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
    """Search for products that match the query."""
    results = [p for p in PRODUCTS if query.lower() in p["name"].lower()]
    return results[:max_results]


def convert_currency(amount: float, rate: float):
    """Convert one currency to another using a given exchange rate."""
    return round(amount * rate, 2)

# Map function names to actual implementations
function_map = {
    "calculate_mortgage": calculate_mortgage,
    "search_product_database": search_product_database,
    "convert_currency": convert_currency,
}

# ---- Tool Descriptions (OpenAI Function Calling Definitions) ----

functions = [
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
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
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert one currency to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "rate": {"type": "number"},
                },
                "required": ["amount", "rate"]
            },
        },
    },
]

# ---- Chat Endpoint ----

@app.post("/chat")
async def chat(req: ChatRequest):
    # Step 1: Send initial user messages to the OpenAI model
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[m.dict(exclude_none=True) for m in req.messages],
        tools=functions,
        tool_choice="auto"
    )

    message = completion.choices[0].message

    # Step 2: If the model calls a function, execute it
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Run the matching Python function
        result = function_map[name](**arguments)

        # Prepare the result as a tool response
        tool_response = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": name,
            "content": str(result)
        }

        # Add function response and call OpenAI again for final reply
        updated_messages = req.messages + [message.dict(), tool_response]

        follow_up = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=updated_messages
        )

        return {"reply": follow_up.choices[0].message.content}

    # Step 3: If no function is called, just return the LLM's message
    return {"reply": message.content}

# ---- Homepage ----

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1> Financial Assistant API</h1>
    <p>Send a POST request to <code>/chat</code> to interact with the assistant.</p>
    """
