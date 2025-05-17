#  AI Powered Applications - Homework 2

---


##  How to Run



```bash
cd backend
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


