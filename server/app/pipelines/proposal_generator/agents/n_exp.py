import os, argparse, json
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from rich import print

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embedding = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004', google_api_key=GEMINI_API_KEY)
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=GEMINI_API_KEY)
vector_db = Chroma(persist_directory="vector_store_1", collection_name="nitor_case_studies", embedding_function=embedding)
vector_search = vector_db.as_retriever(search_kwargs={"k": 1})


CASE_STUDY_TEMPLATE = '''
    You are a professional case study writer for Nitor Technology. Present information in a clear, concise, and impactful manner.
    Focus on business value and technical excellence while maintaining a professional tone.

    Context: {context}
    Query: {user_query}
    DO NOT PUT '*' IN THE

    Based on the above context and query, provide a structured case study with the following format (1-3 sentences per bullet point):
    Do not add company's name in the response.

    **Client Profile:**
    Industry: [Type]

    * **Tech Stack:**
    Primary Technologies: [List key technologies]
    Frameworks & Tools: [List main frameworks and tools used]

    * **Project Highlights:**
    Duration: [Time period]
    Team Size: [Number]
    Key Features: [List main features/deliverables]

    * **Business Need/Challenges:**
    [Describe main challenge]
    [Impact on business operations]
    [Specific pain points addressed]

    * **Nitor Solution:**
    [Implementation approach]
    [Key technical components]
    [Innovative aspects]

    * **Benefits Achieved:**
    [Quantitative metrics]
    [Qualitative improvements]
    [Business impact]

    Guidelines:
    - Keep each bullet point response between 1-3 sentences
    - Include specific metrics and numbers where possible
    - Focus on aspects most relevant to {user_query}
    - Maintain professional and clear language
    - Highlight technical expertise and business value
''' 


def search_nitor_relevant_experience(requirements):
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

if __name__ == "__main__":
    print("\n=== Nitor Relevant Experience Generator for Nitor Infotech ===\n")
    requirements = """
        -Automate Malaysian REPO/Reverse REPO transactions, ensuring GMRA compliance and support for key participants (Affin, interbank, Bursa Malaysia, BNM).
        -Prioritize automated trade execution, real-time compliance monitoring, and efficient collateral management.
        -Integrate seamlessly with market data (e.g., Bloomberg) and existing systems.
        -Ensure robust security, reliability, and scalability to handle increasing volumes and new instruments, complying with all Malaysian regulations.
    """
    results = search_nitor_relevant_experience(requirements)
    print(results)