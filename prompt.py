# PDF Loading & Parsing
from langchain_community.document_loaders import DirectoryLoader  # load PDFs from a directory
from tika import parser  # for parsing PDFs with Apache Tika

# Text Splitting
from langchain.text_splitter import RecursiveCharacterTextSplitter  # recommended splitter



# Document Schema
from langchain.schema import Document  # core Document object

# Embeddings
from langchain_openai import OpenAIEmbeddings  # OpenAI embeddings (text-embedding-3-small/large)
from langchain_community.embeddings import HuggingFaceEmbeddings

# Vector Store
from langchain_community.vectorstores import Chroma  # Chroma for vector DB storage/retrieval

# LLMs & Chat
from langchain_openai import ChatOpenAI  # OpenAI chat model
from langchain.prompts import ChatPromptTemplate  # for prompt engineering


# Evaluation
from langchain.evaluation import load_evaluator  # evaluate RAG pipeline results

# Environment & Config
import openai  # low-level OpenAI client 
from dotenv import load_dotenv  # load API keys from .env
import os  # environment vars + file paths
import shutil  # file operations (moving/deleting old DBs)
import argparse  # optional: CLI argument parsing
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

folder = Path("../Bug-a-boo/Slides") 

all_pdfs = []
for pdf in sorted(folder.glob("*.pdf")):
    pages = PyPDFLoader(str(pdf)).load_and_split()
    all_pdfs.extend(pages)  # append all page Documents to one list

CHROMA_PATH = "chroma" #directory to store the chroma database

#Create a new database from the documents
db = Chroma.from_documents(all_pdfs, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
from openai import OpenAI
client = OpenAI()
def get_debug_hints(code_snippet: str, tier: int) -> list:
    system_prompt = """
    You are an expert Python coding tutor. Your goal is to help students debug their code
    in a stepwise manner. Start with a high-level hint, then more detailed guidance,
    and only give a near-complete solution as a last resort.
    


    Student's code with error:
    {code_snippet}

    Instructions:
    Tier 1 (Nudge): Point to concept/slide title/one probing question.
    Tier 2 (Guided steps): Step‑by‑step to isolate error/ then use minimal code pointer/ then find exact cell link.
    Tier 3 (Near‑solution): Instead of providing full answer patch outline or 2–3 line fix/ cite where it can be found in context, including slide title and page number.
    Tier 4: Solution 
    
    Do not jump ahead to higher tiers unless requested.
    """
    user_prompt = f"""
    The user has provided this buggy Python code:

    {code_snippet}

    Please provide the Tier {tier} hint only.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    hints = completion.choices[0].message.content.split("\n")
    return hints

def get_relevant_tags(buggy_code: str, db, client, top_k: int = 3) -> list:
    """
    Retrieves tags (concepts, topics, or slide titles) related to buggy_code 
    using the vector database + OpenAI reasoning.
    """
    # Step 1: Retrieve similar documents
    results = db.similarity_search_with_score(buggy_code, k=top_k)

    if not results:
        return ["No relevant tags found"]

    # Collect the content of top docs
    context = "\n\n".join([doc.page_content for doc, score in results])

    # Step 2: Ask OpenAI to summarize context as tags
    system_prompt = """
    You are a teaching assistant. Given some retrieved slides or notes, 
    extract 3-5 concise tags (keywords, topics, or concepts). 
    Tags should be single words or short phrases (like 'for loop', 'print syntax', 'variables').
    """
    user_prompt = f"""
    Buggy code:
    {buggy_code}

    Retrieved context:
    {context}

    Please return a list of relevant tags only.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Return tags as a clean list
    tags = [tag.strip() for tag in completion.choices[0].message.content.split(",")]
    return tags

def interactive_debug():
    print("Welcome to Bug-a-boo's interactive Python debugging assistant!")
    print("Enter your Python code (end with a blank line):")

    # --- Input Section ---
    # Uncomment this block if you want to accept multi-line user input instead of hardcoding
    
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    buggy_code = "\n".join(lines)
    
    # buggy_code = "pritn('Hello, world!')"  # Example fallback

    # --- Hint Loop ---
    cont = 'y'
    for tier in range(1, 5):  # Tiers 1–4
        hint = get_debug_hints(buggy_code, tier)
        print(f"\nTier {tier} Hint:\n{hint}\n")

        if tier < 4:  # Only ask if not last tier
            cont = input("Do you want to see the next tier hint? (y/n): ")
            if cont.lower() != 'y':
                break

    # --- Wrap-Up Section ---
    print("\nYou've exhausted all hints (or chose to stop).")
    print("Here are some additional resources:\n")

    results = get_relevant_tags(buggy_code, db, client)
    print(results)

    # --- Context + Tags from Vector DB ---
    results = db.similarity_search_with_score(buggy_code, k=3)
    print("\nContext retrieved from slides:")
    for doc, score in results:
        print(f"- {doc.metadata.get('source', 'Unknown')} (score: {score:.2f})")

    tags = get_relevant_tags(buggy_code, db, client)
    print("\nRelevant tags from your slides:")
    for tag in tags:
        print(f"- {tag}")

if __name__ == "__main__":
    interactive_debug()
# -----------------------------