import openai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print(f"Testing key: {key[:8]}...")

client = openai.OpenAI(api_key=key)
try:
    models = client.models.list()
    print(f"Success! First model: {models.data[0].id}")
except Exception as e:
    print(f"Key test failed: {str(e)}")