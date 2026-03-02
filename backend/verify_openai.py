"""
OpenAI API Key Verification Script
Tests if your API key is valid and has available quota.
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY is not set in .env")
    exit(1)

print(f"🔑 API Key found: {api_key[:8]}...{api_key[-4:]}")

try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    print("\n📡 Testing API connection...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'hello' in one word."}],
        max_tokens=5,
    )

    reply = response.choices[0].message.content.strip()
    print(f"✅ API key is WORKING! Response: \"{reply}\"")
    print(f"   Model: {response.model}")
    print(f"   Tokens used: {response.usage.total_tokens}")

except Exception as e:
    error_type = type(e).__name__
    error_msg = str(e)

    if "insufficient_quota" in error_msg:
        print(f"\n❌ QUOTA EXHAUSTED — Your API key has run out of credits.")
        print("   → Add billing at https://platform.openai.com/account/billing")
    elif "invalid_api_key" in error_msg or "Incorrect API key" in error_msg:
        print(f"\n❌ INVALID API KEY — The key is not recognized by OpenAI.")
        print("   → Check your key at https://platform.openai.com/api-keys")
    elif "rate_limit" in error_msg.lower():
        print(f"\n⚠️  RATE LIMITED — Too many requests. Wait and try again.")
    else:
        print(f"\n❌ ERROR ({error_type}): {error_msg}")
