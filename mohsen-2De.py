# app.py
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from browser_use import CodeAgent, BrowserProfile, ChatBrowserUse, Controller

app = FastAPI()
controller = Controller()

@controller.action("Get 2FA code from authenticator app")
async def get_2fa_code():
    return input("Enter OTP: ")

llm = ChatBrowserUse(
    api_key="bu_cd9hY7r7EnV-CfAOi3hSMDutjC_yeZejTuBUMIRirt8"
)

class DigikalaPayload(BaseModel):
    phone: str

@app.post("/digikala-login")
async def digikala_login(payload: DigikalaPayload):
    browser_profile = BrowserProfile(
        headless=False,
    )

    task = f"""
    Go to https://www.digikala.com/,
    login with phone {payload.phone},
    send the code and ALWAYS use get_2fa_code for authentication.
    """

    agent = CodeAgent(
        task=task,
        llm=llm,
        browser_profile=browser_profile,
        controller=controller,
        flash_mode=True,  # optional, for faster runs
    )

    result = await agent.run()
    return {"result": str(result)}

@app.get("/divar-items")
async def divar_items():
    browser_profile = BrowserProfile(
        headless=True,
    )

    task = """
    Go to https://divar.ir/s/tehran
    and return the first 3 items.
    """

    agent = CodeAgent(
        task=task,
        llm=llm,
        browser_profile=browser_profile,
        flash_mode=True,
    )

    result = await agent.run()
    return {"result": str(result)}
