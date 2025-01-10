from flask import Flask, render_template, jsonify, request
from src.flask_app.annual_report_app.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_openai import OpenAI
from dotenv import load_dotenv
from src.flask_app.annual_report_app.prompt import *
import os
import logging

# Set logging level to WARNING or ERROR to suppress debug/info logs
logging.basicConfig(level=logging.WARNING)

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "annualreportagent"
docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever=docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k":3}
)

prompt=ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","{input}"),
    ]
)

chain_type_kwargs={"prompt": prompt}

llm=OpenAI(temperature=0.5,max_tokens=90)

question_answer_chain=create_stuff_documents_chain(llm,prompt)
rag_chain=create_retrieval_chain(retriever,question_answer_chain)



@app.route("/")
def index():
    return render_template('annual_report_bot.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=rag_chain.invoke({"input":msg})
    print(result["answer"])
    return str(result["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)