from langchain_openai import ChatOpenAI
from config.config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE

# Initialize the LLM
llm = ChatOpenAI(
    model=OPENAI_MODEL, 
    openai_api_key=OPENAI_API_KEY, 
    temperature=TEMPERATURE
)

# Test the LLM
response = llm.invoke("What is the capital of France?")
print(response)