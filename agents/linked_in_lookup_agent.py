from operator import imod
import os
from venv import create
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_community.chat_models import ChatOllama

from langchain_community.tools.tavily_search import TavilySearchResults
from party.linked_in import scrape_linked_in_profile
from tools.tools import get_profile_url_tavily

load_dotenv()
from langchain.agents import(
    create_react_agent,
    AgentExecutor,
)




from langchain import hub



def lookup(name: str) -> str:
    
   llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
   #llm = ChatOllama(model_name="mistral")

   template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""
                          
   prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

   tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

   react_prompt = hub.pull("hwchase17/react")

   agent = create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
   agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

   result = agent_executor.invoke(
       input={"input": prompt_template.format_prompt(name_of_person=name)}
   )

   linkedin_profile_url = result["output"]
   return linkedin_profile_url



if __name__ == "__main__":
    print("start")
    lookup("jaivinder linkedin amelia")
    print("end")

