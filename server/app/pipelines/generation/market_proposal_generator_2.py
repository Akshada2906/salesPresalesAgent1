import os, argparse, json
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from .prompts.market_proposal_2 import PROPOSAL_TEMPLATE, CASE_STUDY_TEMPLATE
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embedding = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004', google_api_key=GEMINI_API_KEY)
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=GEMINI_API_KEY)
vector_db = Chroma(persist_directory="vector_store_1", collection_name="nitor_case_studies", embedding_function=embedding)
vector_search = vector_db.as_retriever(search_kwargs={"k": 1})


# For Nitor's Past Experience
def search_relevant_experience(requirements):
    try:
        docs = vector_search.invoke(requirements)
        docs_content = "\n".join([doc.page_content for doc in docs])
        template = PromptTemplate.from_template(CASE_STUDY_TEMPLATE)
        prompt_response = template.invoke({"context": docs_content, "user_query": requirements})

        response = llm.invoke(prompt_response.to_string())

        if not docs: return "No directly relevant past experience found."

        experience = "Nitor has successfully executed several similar projects:\n\n"
        return experience + response.content
    
    except Exception as e:
        print(f"Warning: Error in vector search: {e}")
        return "Unable to retrieve relevant past experience at this time."


# Generate Proposal
def generate_proposal_content(customer, title, completion, amount, requirements, relevant_experience):
    if not relevant_experience:
        print("Warning: relevant_experience is empty!")
        relevant_experience = "No directly relevant past experience found."
    
    template = PromptTemplate.from_template(PROPOSAL_TEMPLATE)
    prompt_response = template.invoke({
        "customer_name": customer, 
        "project_title": title, 
        "requirements": requirements,
        "completion_date": completion, 
        "amount": amount, 
        "relevant_experience": relevant_experience,
        '"role"': "Solutions Architect"
    })
    response = llm.invoke(prompt_response.to_string())
    
    return response.content


def clean_json_string(content: str) -> str:
    content = content.replace('```json', '').replace('```', '')
    content = content.strip()
    return content


def main(customer, title, requirements, completion, amount):
    relevant_experience = search_relevant_experience(requirements)
    proposal_content = generate_proposal_content(customer, title, completion, amount, requirements, relevant_experience)
    
    try:
        cleaned_content = clean_json_string(proposal_content)
        json_content = json.loads(cleaned_content)
        
        output = "proposal_template.json"
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2)
            
        return json_content
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw content:", proposal_content)
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate proposal template')
    parser.add_argument('--customer', required=True, help='Customer name')
    parser.add_argument('--title', required=True, help='Project title')
    parser.add_argument('--completion', required=True, help='Completion date')
    parser.add_argument('--amount', required=True, type=float, help='Project amount in USD')
    parser.add_argument('--requirements', required=True, help='Project requirements')
    args = parser.parse_args()
    proposal_content = main(args.customer, args.title, args.requirements, args.completion, args.amount)
    print(proposal_content)