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
   git clone <repository-url>
   cd <repository-name>
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

This project implements four different approaches to generate and execute SQL queries from natural language questions:

### Approach 1: Basic SQL Query Chain

- **Description**: Uses a simple SQL query chain to convert a natural language question into an SQL query and execute it.
- **Use Case**: Suitable for basic query generation and execution without additional processing.

### Approach 2: SQL Query Chain with Context

- **Description**: Enhances the basic SQL query chain by incorporating context from the database.
- **Use Case**: Useful for generating queries that require additional context from the database schema.

### Approach 3: SQL Query Chain with Few-Shot Examples

- **Description**: Utilizes few-shot learning by providing examples to improve query generation.
- **Use Case**: Ideal for scenarios where example-based learning can enhance query accuracy.

### Approach 4: SQL Query Chain with Execute Query Tool

- **Description**: Combines query generation and execution in a single step using a tool.
- **Use Case**: Streamlines the process of generating and executing queries.

### Approach 5: Advanced Chain with Natural Language Answer

- **Description**: Provides a natural language answer to the user's question by processing the SQL result.
- **Use Case**: Suitable for applications where users expect a human-readable answer.

### Approach 6: ReAct Agent

- **Description**: Uses a ReAct agent to interact with the SQL database, providing more flexibility and intelligence in query handling.
- **Use Case**: Suitable for complex scenarios where the agent needs to adapt its behavior based on the context and provide more intelligent responses.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
