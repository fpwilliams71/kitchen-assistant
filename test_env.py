import os

print("Testing environment variables...")
print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}")
print(f"ELEVENLABS_API_KEY: {'Set' if os.getenv('ELEVENLABS_API_KEY') else 'Not Set'}")

# If using dotenv
from dotenv import load_dotenv
load_dotenv()
print("\nAfter loading .env:")
print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}")