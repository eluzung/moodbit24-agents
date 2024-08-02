import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv


class OpenAISQL:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing from the environment variables.")

        self.client = OpenAI(api_key=self.api_key)

        self.db_connection = psycopg2.connect(
            dbname="xu",
            host="localhost",
            port="5432"
        )
        self.db_cursor = self.db_connection.cursor()

    def get_table_structures(self):
        try:
            self.db_cursor.execute("""
                SELECT table_name, column_name, data_type, 
                       CASE WHEN column_name ~ '[A-Z]' THEN '"' || column_name || '"' ELSE column_name END AS quoted_name
                FROM information_schema.columns
                WHERE table_schema = 'public';
            """)
            columns = self.db_cursor.fetchall()
            table_structures = {}
            for table_name, column_name, data_type, quoted_name in columns:
                if table_name not in table_structures:
                    table_structures[table_name] = []
                table_structures[table_name].append(
                    f"{quoted_name} ({data_type})")
            return table_structures
        except Exception as e:
            print(f"Error fetching table structures:", e)
            return {}

    # def execute_query(self, query: str):
    #     try:
    #         self.db_cursor.execute(query)
    #         result = self.db_cursor.fetchall()
    #         return result
    #     except Exception as e:
    #         print("Error executing query:", e)
    #         return None

    def generate_sql_query(self, user_question: str):
        table_structures = self.get_table_structures()
        table_info = "\n".join([f"{table} columns: {', '.join(
            columns)}" for table, columns in table_structures.items()])

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"""You are a SQL expert for PostgreSQL. Generate a SQL query to answer the user's question based on the following table structures:
                    {table_info}
                    Important:
                    1. Use the exact column names as provided, including any quotes.
                    2. PostgreSQL is case-sensitive for column names. Use the names exactly as shown.
                    3. When joining tables, make sure to use the correct case and quotes for column names.

                    Only return the SQL query, nothing else."""},
                    {"role": "user", "content": user_question}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("Error generating SQL query:", e)
            return None

    # def process_result(self, user_question: str, sql_query: str, db_result):
    #     try:
    #         formatted_result = "\n".join([str(row) for row in db_result])
    #         prompt = f"""
    #         User question: {user_question}
    #         SQL query used: {sql_query}
    #         Database result: {formatted_result}

    #         Based on the above information, provide a concise answer to the user's question.
    #         """
    #         response = self.client.chat.completions.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "system", "content": "You are a helpful assistant that interprets database results."},
    #                 {"role": "user", "content": prompt}
    #             ]
    #         )
    #         return response.choices[0].message.content.strip()
    #     except Exception as e:
    #         print("Error processing result:", e)
    #         return None

    def query_and_process(self, user_question: str):
        sql_query = self.generate_sql_query(user_question)
        if not sql_query:
            return "Failed to generate SQL query."

        # db_result = self.execute_query(sql_query)
        # if db_result is None:
        #     return f"Failed to retrieve data from the database. SQL query: {sql_query}"

        # response = self.process_result(user_question, sql_query, db_result)
        return f"SQL query used: \n{sql_query}"


# Example usage
if __name__ == "__main__":
    agent = OpenAISQL()
    # user_question = "Which customer had the highest total amount of purchases"
    # result = agent.query_and_process(user_question)
    # print(result)
