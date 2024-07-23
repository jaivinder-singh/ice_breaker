from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Tuple
import os
from dotenv import load_dotenv
from party.linked_in import scrape_linked_in_profile
from agents.linked_in_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary


def get_linked_data(name:str) -> Tuple[Summary,str]:

    linkedin_user_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linked_in_profile(linkedin_profile_url=linkedin_user_url,mock=True)
    print("Hello lanchain")



    summary_template = """
    given the Linkedin information  {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    \n
    {format_instructions}
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template, 
                                            partial_variables={"format_instructions":summary_parser.get_format_instructions()})

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    #llm = ChatOllama(model_name="llama3")
    #llm = ChatOllama(model_name="mistral")

    chain = summary_prompt_template | llm | summary_parser


    res: Summary = chain.invoke(input={"information": linkedin_data})
    #print(linkedin_data)
    print(res, linkedin_data.get("profile_pic_url"))
    return res, linkedin_data.get("profile_pic_url")
#print(os.environ['OPENAI_API_KEY'])

if __name__ == "__main__":
    load_dotenv()
    print("Entering get linkedin data")
    get_linked_data(name="Jaivinder Singh amelia")
