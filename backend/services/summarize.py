import os
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def generate_response(user_input):

    prompt_template = PromptTemplate(
        input_variables=["input"],
        template="""
        You are a summarizer bot. You are given a text and you need to summarize it in a concise manner, sich that the summarized text can be used as a informative 3-5 minute audio book content while travelling.
        User: {input}
        Assistant:
        """
    )
    prompt = prompt_template.format(input=user_input)
    response = llm.invoke(prompt)
    return response.content

