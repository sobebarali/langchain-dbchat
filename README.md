# AI-Powered SQL Query Generator

This project demonstrates how to build an AI-powered SQL query generator using LangChain and OpenAI. The system takes natural language questions and converts them into executable SQL queries.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Approaches](#approaches)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

The AI-Powered SQL Query Generator is designed to simplify the process of querying databases by allowing users to input natural language questions. The system leverages the power of AI to translate these questions into SQL queries, which can then be executed on a database.

## Features

- Convert natural language to SQL queries
- Support for multiple SQL databases (PostgreSQL, MySQL, etc.)
- Easy integration with existing systems

## Prerequisites

- Python 3.8+
- OpenAI API key
- PostgreSQL/MySQL database (or your preferred SQL database)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sobebarali/langchain-dbchat
   cd langchain-dbchat
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set up your environment variables:

   - Create a `.env` file in the root directory of the project.
   - Add the following keys to the `.env` file:
     ```plaintext
     OPENAI_API_KEY="your_openai_api_key"
     LANGCHAIN_API_KEY="your_langchain_api_key"
     LANGCHAIN_TRACING_V2=true
     ```

2. Configure your database connection:
   - Update the `config.py` file with your database credentials.

## Usage

1. Start the application:

   ```bash
   python src/main.py
   ```

2. Input your natural language question and receive the corresponding SQL query.

## Approaches

This project implements several approaches to generate and execute SQL queries from natural language questions:

### Approach 1: Basic SQL Query Chain

- **Description**: Uses a simple SQL query chain to convert a natural language question into an SQL query and execute it.
- **Use Case**: Suitable for basic query generation and execution without additional processing.

### Approach 2: SQL Query Chain with Validation

- **Description**: Enhances the basic SQL query chain by incorporating a validation step. It uses a system prompt to check the generated SQL query for common mistakes, such as using `NOT IN` with `NULL` values, incorrect use of `UNION` vs. `UNION ALL`, data type mismatches, and more. If any mistakes are found, the query is rewritten; otherwise, the original query is reproduced.
- **Use Case**: Ideal for ensuring the accuracy and reliability of SQL queries before execution. This approach is particularly useful in environments where query correctness is critical, and errors could lead to incorrect data retrieval or processing.
- **Components**:
  - **System Prompt**: Defines the rules and checks for validating SQL queries.
  - **Validation Chain**: Combines the system prompt with the language model and an output parser to validate and potentially rewrite the query.

### Approach 3: SQL Query Chain with Context

- **Description**: Enhances the basic SQL query chain by incorporating context from the database.
- **Use Case**: Useful for generating queries that require additional context from the database schema.

### Approach 4: SQL Query Chain with Few-Shot Examples

- **Description**: Utilizes few-shot learning by providing examples to improve query generation.
- **Use Case**: Ideal for scenarios where example-based learning can enhance query accuracy.

### Approach 5: SQL Query Chain with Execute Query Tool

- **Description**: Combines query generation and execution in a single step using a tool.
- **Use Case**: Streamlines the process of generating and executing queries.

### Approach 6: Advanced Chain with Natural Language Answer

- **Description**: Provides a natural language answer to the user's question by processing the SQL result.
- **Use Case**: Suitable for applications where users expect a human-readable answer.

### Approach 7: ReAct Agent with State and Message Modifiers

- **Description**: Implements two ReAct agents, one using a state modifier and the other using a messages modifier. The state modifier approach modifies the entire agent state before LLM processing, while the messages modifier approach modifies only the messages.
- **Use Case**: Useful for scenarios where different levels of context modification are required before processing by the language model. The state modifier is the preferred method as it provides a more comprehensive context adjustment.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
