import os
import getpass
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, initialize_agent
from langchain.tools import Tool, BaseTool, tool, StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.chains import LLMMathChain
from langchain.agents.output_parsers.tools import ToolAgentAction
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.prompts import MessagesPlaceholder


class LangchainAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API_KEY is missing from the environment variables.")

        self.llm = ChatOpenAI(
            temperature=0.0, model="gpt-3.5-turbo", api_key=api_key)

    def sql_query(self, input: str):
        try:
            db = SQLDatabase.from_uri("sqlite:///test_db.db")
            # print(db.dialect)
            # print(db.get_usable_table_names())

            # validation_string_template = """
            # Double check the user's sqlite query for common mistakes, including:
            # - Using NOT IN with NULL values
            # - Using UNION when UNION ALL should have been used
            # - Using BETWEEN for exclusive ranges
            # - Data type mismatch in predicates
            # - Properly quoting identifiers
            # - Using the correct number of arguments for functions
            # - Casting to the correct data type
            # - Using the proper columns for joins

            # If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

            # Output the final SQL query only.

            # User Input: {input}
            # """

            # validation_prompt = ChatPromptTemplate.from_messages(
            #     [("system", "{validation_string_template}"), ("user", "{input}"), MessagesPlaceholder(variable_name="agent_scratchpad")]
            # )

            # sql_agent = create_sql_agent(self.llm, db=db, agent_type="openai-tools", verbose=True, prompt=validation_prompt, agent_executor_kwargs={"return_intermediate_steps": True})

            sql_agent = create_sql_agent(self.llm, db=db, agent_type="openai-tools",
                                         verbose=True, agent_executor_kwargs={"return_intermediate_steps": True})

            response = sql_agent.invoke({
                "input": input})

            responseObj = {
                "output": response["output"],
                "sql_query": response["intermediate_steps"][2][0].tool_input.get('query')
            }

            return responseObj
        except Exception as e:
            print("error", e)
            return str(e)

    # class UserInput(BaseModel):
    #     input: str = Field(description="String of user's input")

    # def generate_tasks(self, input: str):
    #     """Generate tasks for the given input"""

    #     output_parser = JsonOutputParser()

    #     format_instructions = output_parser.get_format_instructions()

    #     template_string = """
    #     you are a very helpful assistent. You will generate a lists of step by step instructions given the users input.

    #     Here is the User's input: {input}

    #     Please format the list of steps in JSON format and return a valid JSON object.

    #     {format_instructions}
    #     """

    #     prompt_template = PromptTemplate(template=template_string, input_variables=["input"], partial_variables={"format_instructions": format_instructions})

    #     chain = prompt_template | self.llm | output_parser

    #     return chain.invoke({"input": input})

        # def call_tools(self, input: str):
    #     try:
    #         print("Running tools")

    #         llm_math = LLMMathChain(llm=self.llm)

    #         math_tool = Tool(
    #             name="Calculator",
    #             func=llm_math.run,
    #             description="useful for when you need to answer questions about math",
    #         )

    #         task_tool = StructuredTool.from_function(
    #             name="Task Generator",
    #             func=self.generate_tasks,
    #             description="useful for when you need to generate tasks from a given input",
    #             args_schema=self.UserInput
    #         )

    #         tools = [math_tool, task_tool]

    #         zero_shot_agent = initialize_agent(
    #             tools=tools,
    #             llm=self.llm,
    #             agent="zero-shot-react-description",
    #             verbose=True
    #         )

    #         response = zero_shot_agent.run(input)

    #         return response

    #     except Exception as e:
    #         print("error", e)
    #         return str(e)
