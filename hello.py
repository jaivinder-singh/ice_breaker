from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os

from party.linked_in import scrape_linked_in_profile

print("Hello lanchain")

summary_template = """
given the Linkedin information  {information} about a person from I want you to create:
1. a short summary
2. two interesting facts about them
"""

summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

#llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

#llm = ChatOllama(model_name="llama3")
llm = ChatOllama(model_name="mistral")

chain = summary_prompt_template | llm | StrOutputParser()
linkedin_date = scrape_linked_in_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco",mock=True)

res = chain.invoke(input={"information": linkedin_date})

print(res)

#print(os.environ['OPENAI_API_KEY'])