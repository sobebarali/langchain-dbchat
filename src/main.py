from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain

# Import configuration and database connection
from config.config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE
from database.connection import db

print("\n=== Initializing OpenAI LLM ===")
llm = ChatOpenAI(
    model=OPENAI_MODEL, 
    openai_api_key=OPENAI_API_KEY, 
    temperature=TEMPERATURE
)
print(f"Model initialized with: Model={OPENAI_MODEL}, Temperature={TEMPERATURE}")

print("\n=== Example Query ===")
example_query = "How many employees are there ?"
print(f"Query: {example_query}")


print("\n=== APPROACH 1: Basic SQL Query Chain ===")
print("Creating SQL query chain...")
chain = create_sql_query_chain(llm, db)
print("\n=== Chain Prompt Template ===")
chain.get_prompts()[0].pretty_print()

print("\n=== Generated SQL Query ===")
response = chain.invoke({"question": example_query})    
print(f"SQL Query: {response}")

print("\n=== Executing SQL Query ===")
result = db.run(response)
print(f"Query Result: {result}")

