import os, time, json
from langchain_community.document_loaders import CSVLoader
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from .prompts.sales_bot_prompt import system_prompt
from dotenv import load_dotenv
from rich import print

# from ...core.llm_provider import azure_llm

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
embedding = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004', google_api_key=GEMINI_API_KEY)

# llm = azure_llm
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=GEMINI_API_KEY)

loader = CSVLoader(file_path=r'app\data\Nitor_Consolidated_List_of_Case_Studies_V2.csv')
data = loader.load()


config = {"configurable": {"session_id": "session_1"}}
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# def create_paragraph_from_row(llm, row_content):    
#     prompt = """Convert the following pipe-separated case study information into a natural, flowing paragraph. 
#         Maintain all technical details but make it read smoothly.
        
#         Format of input case study:
#         Customer Type (ISV/Enterprise) | Customer Name | Industry | Service Area | Project/Case Study Title | Short Description | Key Words | Tech Stacks
        
#         Input: {row_content}
        
#         Convert this into a well-structured paragraph that a business person can easily understand. 
#         Focus on the business value, challenge, solution, and technologies used.
#         Do not add any other text or comments.
#     """
#     response = llm.invoke(prompt.format(row_content=row_content))
#     time.sleep(30)
#     return response.content


def create_or_get_vector_storage(data, persist_directory, collection_name):
    # chunks = []
    # for doc in data:
    #     chunk = doc.page_content
    #     chunks.append(chunk)

    # documents = [Document(page_content=chunk, metadata={}) for chunk in chunks]
    # keyword_retriever = BM25Retriever.from_documents(documents)

    # if os.path.exists(persist_directory):
    #     vector_store = Chroma(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embedding)
    # else:
    #     vector_store = Chroma.from_documents(documents=documents, embedding=embedding, persist_directory=persist_directory, collection_name=collection_name)
    vector_store = Chroma(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embedding)
    return vector_store


def create_prompt_template():
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_query}")
    ])



vectorDB = create_or_get_vector_storage(data, "vector_store_1", "nitor_case_studies")

def main(user_query):
    prompt = create_prompt_template()
    chain = prompt | llm
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    
    vectorstore_retreiver = vectorDB.as_retriever(search_kwargs={"k": 10})
    docs = vectorstore_retreiver.invoke(user_query)
    relevant_chunks = [doc.page_content for doc in docs]
    
    response = chain_with_history.invoke(
        {
            "input": user_query,
            "context": relevant_chunks,
            "user_query": user_query
        }, 
        config=config
    )
    
    try:
        # Clean up the response to get just the JSON content
        if isinstance(response.content, str):
            # Remove markdown code block if present
            if "```json" in response.content:
                json_str = response.content.split("```json\n")[1].split("\n```")[0]
            else:
                json_str = response.content
            return json_str
        return json.dumps(response.content)
    except Exception as e:
        # Fallback response
        return json.dumps({
            "message": "Error processing response",
            "companies_list": []
        })


if __name__ == "__main__":
    while True:
        print('\n---------------------------------------')
        que = input('Ask : ')
        if que == 'exit': break
        answer = main(que.lower())
        print(answer)