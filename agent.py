from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.tools import Tool
from langchain_core.messages import AIMessage, HumanMessage
from dbquery import part_query, model_query, manufacturer_query, general_query
import os

class Agent:
    def __init__(self) -> None:
        key_file = open('key.txt', mode='r')
        key = key_file.readline().strip()
        os.environ['OPENAI_API_KEY'] = key
        # print(key)
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        print('fetching prompt')
        self.prompt = hub.pull("lpang2143/openai-functions-partselect-agent")
        print('fetched prompt')
        print(self.prompt.messages)
        self.tools = [
            Tool(
                name="part-query",
                func=lambda part_number, custom=os.environ['QUERY']: str(part_query(part_number, custom)),
                description="This allows you to query a vector database for useful dishwasher and fridge info by part number."
            ),
            Tool(
                name='model-query',
                func=lambda model_number, custom=os.environ['QUERY']: str(model_query(model_number, custom)),
                description="This allows you to query a vector database for useful dishwasher and fridge info by model number."
            ),
            Tool(
                name='manufacturer-query',
                func=lambda manufacturer, custom=os.environ['QUERY']: str(manufacturer_query(manufacturer, custom)),
                description="This allows you to query a vector database for useful dishwasher and fridge info by manufacturer."
            ),
            Tool(
                name='general_query',
                func=general_query,
                description="This allows you to query a vector database for useful dishwasher and fridge info by similarity search"
            )
        ]
        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
        self.chat_history = [AIMessage(content="Hi, how can I help you today?")]

        return
    
    def query(self, query: str):
        response = self.agent_executor.invoke({"input": query, "chat_history": self.chat_history.copy()})
        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=response['output']))
        # print(f"\n{self.chat_history}")
        return response
    
    def get_history(self):
        return self.chat_history

if __name__=='__main__':
    agent = Agent()
    print(agent.query('Can you output the chat history I just sent you?'))
    