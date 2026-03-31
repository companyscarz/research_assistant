from crewai import LLM
import os
from dotenv import load_dotenv
# from openai import OpenAi

load_dotenv()
groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

ollama_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)
