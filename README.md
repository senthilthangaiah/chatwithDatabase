# chatwithDatabase
Query your Database in plain english.


markdown
Copy code
# Chat with Your Data

A Streamlit-based application that allows users to interact with their SQLite database using natural language queries. Powered by Azure OpenAI and Sentence Transformers.

## Features

- Execute natural language queries against an SQLite database
- Generate SQL statements using OpenAI's GPT-3.5
- Display query results in a dataframe
- Identify x and y axes for plotting

## Installation

1. Clone the repository:

```sh
git clone https://github.com/senthilthangaiah/chatwithDatabase.git
cd chatwithDatabase
```
Create a virtual environment:
```sh

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required dependencies:
```sh

pip install -r requirements.txt

```
Set up your environment variables. Create a .env file in the root directory and add the following:
```dotenv


AZURE_OPENAI_API_KEY=your_openai_api_key
```

Usage
Run the Streamlit application:
```sh

streamlit run app.py
```
Open your browser and navigate to the displayed URL (default is http://localhost:8501).

Interact with your database by entering natural language queries in the chat interface.

## Project Structure
```css
main.py: Contains the core logic for interacting with the database and generating SQL queries using OpenAI.
app.py: Streamlit application code.
requirements.txt: List of dependencies required to run the project.
.env: Environment variables for Azure OpenAI API keys (not included in the repository for security reasons).
```

## License
This project is licensed under the MIT License.

## Acknowledgements
OpenAI
Streamlit
Sentence Transformers
go
Copy code

### `requirements.txt`

```txt
pandas
streamlit
langchain
sentence-transformers
torch
openai
python-dotenv
```

.env.example
```dotenv

AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_VERSION=your_azure_openai_api_version
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

.gitignore
```gitignore

venv/
__pycache__/
.env
*.sqlite3
*.db
```

## Directory Structure
Ensure your project directory is structured as follows:

```csharp

chat-with-your-data/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
