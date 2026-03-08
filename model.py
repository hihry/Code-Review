import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Load your API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# 2. Initialize the model
# We point the base_url to OpenRouter and use a ':free' model ID
llm = ChatOpenAI(
    model="upstage/solar-pro-3:free",
    base_url="https://openrouter.ai/api/v1", # One of the best free models
    openai_api_key=api_key,
)
# 3. Test it
# response = llm.invoke("tell me a joke")
# print(response.content)