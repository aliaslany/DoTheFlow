import asyncio
import aiohttp
import os
import json

async def submit_dynamic_form():
    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ5MTE0NzAwMTgsInN1YiI6Im9fNDc1OTk3NTUzNTM2Mzg4MTcwIn0.r7g6NzGLYh9VnYqVuYvi4C6ZozLYbCVVBLYMNjur6Xc"
    BASE_URL = "https://api.skyvern.com/agent/runs"
    
    async with aiohttp.ClientSession(
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    ) as session:
        
        # Step 1: CREATE TASK - Debug response
        payload = {
            "url": "https://digikala.com/",
            "goal": """1. Fill registration form step-by-step starting with phone number 09376417998
2. Email: test@yourdomain.com, Password: SecurePass123!, Full name: John Doe
3. Click Continue/Next between steps
4. Buy Example Product (quantity 1), address: 123 Example St, City, Country
5. Wait for OTP/payment input from user
6. Submit and confirm success""",
            "max_pages": 10
        }
        
        async with session.post(f"{BASE_URL}", json=payload) as resp:
            print(f"📡 CREATE Response Status: {resp.status}")
            task_data = await resp.json()
            print("📄 RAW Response:", json.dumps(task_data, indent=2))
            
            # Try different possible task ID fields
            task_id = (task_data.get("id") or 
                      task_data.get("task_id") or 
                      task_data.get("taskId") or
                      task_data.get("data", {}).get("id"))
            
            if not task_id:
                print("❌ No task ID found! Check API key/response")
                return
            
            print(f"🚀 Task ID: {task_id}")
        
        # Step 2: MONITOR TASK
        while True:
            async with session.get(f"{BASE_URL}/tasks/{task_id}") as resp:
                task = await resp.json()
                print("📊 Task Status Response:", json.dumps(task, indent=2))
                
                status = task.get("status", "unknown")
                current_url = task.get("current_url", task.get("url", "N/A"))
                
                print(f"📍 Status: {status} | URL: {current_url}")
                
                # Human intervention triggers
                task_str = str(task).lower()
                if any(trigger in task_str for trigger in ["otp", "2fa", "captcha", "payment", "verify"]):
                    confirm = input("🔑 Handle OTP/Payment? (y/n): ")
                    if confirm.lower() == 'y':
                        code = input("Enter code: ")
                        async with session.post(
                            f"{BASE_URL}/tasks/{task_id}/input",  # Try /input endpoint
                            json={"input": code}
                        ) as input_resp:
                            print(f"Input response: {input_resp.status}")
                
                # Check completion
                if status in ["success", "completed", "failed", "cancelled"]:
                    print("✅ TASK FINISHED!")
                    print(f"Final result: {task.get('result', 'N/A')}")
                    print(f"Dashboard: https://app.skyvern.com/task/{task_id}")
                    break
            
            await asyncio.sleep(4)

if __name__ == "__main__":
    asyncio.run(submit_dynamic_form())
