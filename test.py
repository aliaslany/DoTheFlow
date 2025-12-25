from skyvern import Skyvern
import asyncio

async def submit_dynamic_form():
    skyvern = Skyvern(
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ5MTE0NzAwMTgsInN1YiI6Im9fNDc1OTk3NTUzNTM2Mzg4MTcwIn0.r7g6NzGLYh9VnYqVuYvi4C6ZozLYbCVVBLYMNjur6Xc"
    )
    
    print("🚀 Starting Digikala automation...")
    
    # Create task
    task = await skyvern.run_task(
        prompt="""1. Go to https://digikala.com/
2. Fill registration form: phone 09376417998
3. Email: test@yourdomain.com, Password: SecurePass123!
4. Complete registration steps
5. Search for "Example Product", buy quantity 1
6. Use address: 123 Example St, City, Country
7. Wait for OTP/payment confirmation""",
        engine="skyvern-2.0"
    )
    
    # Safe attribute access
    run_id = getattr(task, 'run_id', getattr(task, 'id', 'unknown'))
    print(f"🚀 Run ID: {run_id}")
    print(f"📊 Initial status: {getattr(task, 'status', 'unknown')}")
    
    # Monitor with SAFE checks
    max_attempts = 60  # 4min timeout
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Refresh task status
            refreshed_task = await skyvern.get_run(run_id)
            status = getattr(refreshed_task, 'status', 'unknown')
            
            print(f"📍 [{attempt+1}/60] Status: {status}")
            
            # Safe URL output
            current_url = getattr(refreshed_task, 'current_url', 'N/A')
            print(f"🌐 URL: {current_url}")
            
            # Safe output preview (handle None)
            output = getattr(refreshed_task, 'output', None)
            if output:
                print(f"📄 Output: {str(output)[:100]}...")
            else:
                print("📄 Output: (running, no output yet)")
            
            # Human intervention (safe string check)
            task_info = str(refreshed_task).lower()
            if any(trigger in task_info for trigger in ["otp", "2fa", "captcha", "payment", "verify", "کد"]):
                confirm = input("\n🔑 OTP/Payment needed? (y/n): ")
                if confirm.lower() == 'y':
                    code = input("Enter code: ")
                    try:
                        await skyvern.send_human_input(run_id, code)
                        print("✅ Input sent!")
                    except Exception as e:
                        print(f"❌ Input error: {e}")
            
            # Check completion (case insensitive)
            if status.lower() in ["succeeded", "success", "completed", "failed", "cancelled"]:
                print("\n✅ TASK FINISHED!")
                final_output = getattr(refreshed_task, 'output', 'No output')
                print(f"🎯 RESULT: {final_output}")
                print(f"📱 Dashboard: https://app.skyvern.com/run/{run_id}")
                return
            
        except Exception as e:
            print(f"❌ Error refreshing: {e}")
        
        await asyncio.sleep(4)
        attempt += 1
    
    print("⏰ Timeout - check dashboard manually")

if __name__ == "__main__":
    asyncio.run(submit_dynamic_form())
