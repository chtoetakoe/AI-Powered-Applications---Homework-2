#  AI Powered Applications - Homework 2

fullstack Python + React application that demonstrates OpenAI **function calling** via a friendly financial assistant. The assistant can:

*  Calculate monthly mortgage payments
*  Search a product database (e.g., office supplies)

The LLM automatically determines when to call functions based on user queries and formats the results clearly in a chat interface.

---

##  Requirements

* Python 3.9+
* Node.js & npm
* OpenAI API key

---

##  How to Run



```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your OpenAI API key



```env
OPENAI_API_KEY= enter you api key
```

### 3. Run the backend server

```bash
uvicorn main:app --reload --port 8000
```

---

### 4. Set up and run the frontend

```bash
cd ../frontend
npm install
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173)

---



##  Tech Stack

* Backend: Python, FastAPI, OpenAI SDK (v0.28)
* Frontend: React, TypeScript, Plain CSS
* Function calling: `calculate_mortgage()`, `search_product_database()`


