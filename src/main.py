from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

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

print("\n=== APPROACH 2: SQL Query Chain with Execute Query Tool ===")
print("Initializing query tools...")
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
print("Executing chain...")
result = chain.invoke({"question": example_query})
print(f"Chain Result: {result}")

print("\n=== APPROACH 3: Advanced Chain with Natural Language Answer ===")
print("Setting up advanced chain components...")
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

print("Creating advanced processing chain...")
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

print("\n=== Executing Advanced Chain ===")
print("Processing query through natural language chain...")
result = chain.invoke({"question": example_query})
print("\n=== Final Natural Language Response ===")
print(result)

print("\n=== Execution Complete ===")


