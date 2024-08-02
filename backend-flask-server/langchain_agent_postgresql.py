import os
import re
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent


class LangchainAgent_postgresql:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API_KEY is missing from the environment variables.")

        self.llm = ChatOpenAI(
            temperature=0.0, model="gpt-3.5-turbo", api_key=api_key
        )

    def sql_query(self, input: str):
        try:
            # Update the connection URI to use PostgreSQL
            db = SQLDatabase.from_uri("postgresql://localhost:5432/xu")

            sql_agent = create_sql_agent(
                self.llm, db=db, agent_type="openai-tools",
                verbose=True, agent_executor_kwargs={"return_intermediate_steps": True}
            )

            response = sql_agent.invoke(
                {"input": input + " Must include the correct SQL query."})

            sql_query_match = re.search(
                r'```sql\n(SELECT[\s\S]*?)\n```', response["output"])

            sql_query = sql_query_match.group(
                1).strip() if sql_query_match else None

            try:
                if len(response.get("intermediate_steps", [])) > 2 and len(response["intermediate_steps"][2]) > 0:
                    sql_query1 = response["intermediate_steps"][2][0].tool_input.get(
                        'query')
                else:
                    sql_query1 = sql_query
            except IndexError:
                sql_query1 = sql_query

            if sql_query1:
                sql_query1 = sql_query1.replace('\n', ' ').replace('\\', '')
            # print("sql_query1", sql_query1)
            responseObj = {
                "sql_query1": sql_query1,
                # "output": response["output"],
                # "sql_query": sql_query,
                # "filtered_output": filtered_output
            }

            return responseObj
        except Exception as e:
            print("error", e)
            return str(e)


# Example usage
if __name__ == "__main__":
    agent = LangchainAgent_postgresql()
