from flask import Flask, request
from flask_cors import CORS
from langchain_agent import LangchainAgent
from langchain_agent_postgresql import LangchainAgent_postgresql
from openai_sql import OpenAISQL


app = Flask(__name__)
CORS(app, origins=["*"])

langchain_agent = LangchainAgent()
langchain_agent_postgresql = LangchainAgent_postgresql()
openai_sql = OpenAISQL()


@app.route('/', methods=['POST'])
def test():
    return 'testing works'


@app.route('/tools', methods=['POST'])
def tools():
    try:
        input = request.get_json().get('input')

        response = langchain_agent.call_tools(input)
        return response
    except Exception as e:
        return str(e)


@app.route('/sql-query', methods=['POST'])
def sql_query():
    try:
        input = request.get_json().get('input')
        response = langchain_agent.sql_query(input)
        return response
    except Exception as e:
        return str(e)


@app.route('/sql-query-postgresql', methods=['POST'])
def sql_query_postgresql():
    try:
        input = request.get_json().get('input')
        response = langchain_agent_postgresql.sql_query(input)
        return response
    except Exception as e:
        return str(e)


@app.route('/gpt4-sql', methods=['POST'])
def gpt4_sql():
    try:
        input = request.get_json().get('input')
        response = openai_sql.query_and_process(input)
        return response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=8080)
