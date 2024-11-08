from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import SystemMessage

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


print("\n=== APPROACH 2: SQL Query Chain with Context ===")
context = db.get_context()
prompt_with_context = chain.get_prompts()[0].partial(table_info=context["table_info"])
print("\n=== Chain Prompt Template with Context ===")
print(prompt_with_context.pretty_repr())

print("\n=== Executing SQL Query with Context ===")
result = chain.invoke({"question": example_query})
print(f"Query Result: {result}")


print("\n=== APPROACH 3: SQL Query Chain with Execute Query Tool ===")
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


print("\n=== APPROACH 5: ReAct Agent ===")
print("Initializing SQL toolkit and creating agent...")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# First agent with state_modifier
print("\n=== Agent 1: Using state_modifier ===")
print("This approach modifies the entire agent state before LLM processing")
prompt_template1 = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message1 = prompt_template1.format(dialect="SQLite", top_k=5)
agent_executor1 = create_react_agent(
    llm, tools, state_modifier=system_message1
)
print("Agent created with state_modifier that adds system message to state")

print("\nStreaming agent's response...")
events = agent_executor1.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    print("\n=== ReAct Agent 1 Response ===")
    event["messages"][-1].pretty_print()

# Second agent with messages_modifier
print("\n=== Agent 2: Using messages_modifier (Legacy Approach) ===")
print("This approach only modifies the messages before LLM processing")
print("Note: messages_modifier is deprecated in favor of state_modifier")

SQL_PREFIX = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables."""

system_message2 = SystemMessage(content=SQL_PREFIX)
agent_executor2 = create_react_agent(
    llm, tools, messages_modifier=system_message2
)
print("Agent created with messages_modifier that adds system message to messages")

print("\nStreaming agent's response...")
events = agent_executor2.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    print("\n=== ReAct Agent 2 Response ===")
    event["messages"][-1].pretty_print()