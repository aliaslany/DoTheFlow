
This project provides an API for automating Iranian web services (e.g., Digikala login with OTP, Divar listing extraction) using **browser-use CodeAgent** and **FastAPI**.

## Features

- AI-driven browser automation with `CodeAgent` (browser-use)
- Digikala login flow with manual OTP input
- Divar scraping: fetch first items from a city page
- FastAPI endpoints, ready to be called from bots or other services
- Extensible design for adding more government/private service workflows

## Tech Stack

- Python 3.9+
- FastAPI
- browser-use (`CodeAgent`, `ChatBrowserUse`)
- Playwright (Chromium)
- Async I/O with `asyncio`

## Getting Started

### 1. Clone and create venv

```
git clone https://github.com/your-username/iran-services-browser-automation.git
cd iran-services-browser-automation

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 2. Install dependencies

```
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure environment

Create a `.env` file (or export env vars) with your Browser Use API key:

```
export BROWSER_USE_API_KEY="YOUR_KEY_HERE"
export BROWSER_USE_TELEMETRY=0
export ANONYMIZED_TELEMETRY=false
export POSTHOG_DISABLED=true
```

Or hard-code in `app.py` while developing (not recommended for production).

## Running the API

```
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`.

## API Endpoints

### POST `/digikala-login`

Launches a browser and performs Digikala login with OTP prompt in the terminal.

**Request body:**

```
{
  "phone": "09000000000"
}
```

**Example curl:**

```
curl -X POST http://localhost:8000/digikala-login \
  -H "Content-Type: application/json" \
  -d '{"phone": "09000000000"}'
```

During the flow, the terminal will ask:

```
Enter OTP:
```

Enter the received code to let the agent continue.

### GET `/divar-items`

Opens Divar Tehran page and returns the first few items.

```
curl http://localhost:8000/divar-items
```

Response will contain a text summary with the extracted items.

## How It Works (High-Level)

- FastAPI receives a request on an endpoint.
- For each request, a `BrowserProfile` and `CodeAgent` are created.
- The `CodeAgent` executes the task instructions (Digikala login / Divar scraping) inside a Playwright-controlled browser.
- Custom `@controller.action` is used for OTP input from the user at runtime.

## Adding New Workflows

1. Create a new FastAPI endpoint in `app.py`.
2. Define a `task` string that describes the steps for the new website.
3. Instantiate a new `CodeAgent` with the shared `llm` and a `BrowserProfile`.
4. `await agent.run()` and return the result.

Example pattern:

```
@app.post("/new-service")
async def new_service(payload: NewPayload):
    browser_profile = BrowserProfile(headless=True)
    task = f\"\"\"
    Go to https://example.com
    Do X, then Y, then Z using payload  {payload.some_field}
    \"\"\"
    agent = CodeAgent(task=task, llm=llm, browser_profile=browser_profile)
    result = await agent.run()
    return {"result": str(result)}
```

## Roadmap / Ideas

- Add more Iranian government portals (hamta, tax, social security)
- Save workflows with `workflow-use` for replay and versioning
- Use a message queue (Redis, etc.) for high-throughput job handling
- Add a simple web UI for triggering and monitoring tasks
 
