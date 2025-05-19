#  AI Powered Applications – Homework 2

This is a fullstack AI assistant that uses **OpenAI function calling** via a **FastAPI backend** and a **React + TypeScript frontend**.

The assistant can:
-  Calculate monthly mortgage payments  
-  Search a simulated product database

Model used: **`gpt-4o-mini-2024-07-18`**

---

##  Project Structure

```
AI-POW-APP-HMW2/
├── backend/                  # FastAPI backend (no CLI)
│   ├── main.py               # API + function calling logic
│   ├── .env                  # OpenAI API key (not tracked by Git)
│   └── requirements.txt
└── frontend/                 # React + TypeScript frontend
    ├── src/
    │   ├── App.tsx
    │   └── App.css
    └── ...
```

---

##  Tech Stack

- **Backend**: Python, FastAPI, OpenAI SDK (`openai==0.28`)
- **Frontend**: React, TypeScript, Vite
- **OpenAI Model**: `gpt-4o-mini-2024-07-18`
- **Function Calling**:
  - `calculate_mortgage(principal, rate, years)`
  - `search_product_database(query, max_results)`

---

##  How to Run the Application

###  1. Backend Setup

```bash
cd backend
```

#### Step 1: Create Virtual Environment

- **macOS/Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **Windows (CMD)**:
- (Optional for Windows) Create Virtual Environment
Windows users may skip this step and use their global Python installation,
but using a virtual environment is still recommended for consistency.
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **Windows (PowerShell)**:
  ```bash
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Add OpenAI API Key

Create a `.env` file in the `backend/` folder:

```env
OPENAI_API_KEY=your-api-key-here
```

#### Step 4: Start the Backend Server

```bash
uvicorn main:app --reload --port 8000
```

Server will run at: [http://localhost:8000](http://localhost:8000)  
You can send POST requests to `/chat`.

---

###  2. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

Frontend will run at: [http://localhost:5173](http://localhost:5173)


