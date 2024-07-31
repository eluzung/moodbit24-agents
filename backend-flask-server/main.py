from flask import Flask, request
from flask_cors import CORS
from langchain_agent import LangchainAgent
# from api import api_bp

app = Flask(__name__)
CORS(app, origins=["*"])

langchain_agent = LangchainAgent()

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
    
if __name__ == '__main__':
    app.run(port=8080)