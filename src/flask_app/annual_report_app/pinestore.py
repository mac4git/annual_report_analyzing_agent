from src.flask_app.annual_report_app.helper import load_pdf_file, text_split, download_hugging_face_embeddings



from dotenv import load_dotenv
load_dotenv()
import os

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

from langchain_pinecone import PineconeVectorStore


extracted_data=load_pdf_file(data='downloads/')
text_chunks=text_split(extracted_data)
embeddings=download_hugging_face_embeddings()

index_name = "annualreportagent"
docsearch=PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)