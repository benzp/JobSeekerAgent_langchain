import os
import json
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.tools import tool        # decorator to wrap Python functions as tools
from langchain.agents import create_agent
from tempfile import NamedTemporaryFile
from docx import Document



def TopMatchingJobs(aspirations: str, current_skills: str) -> str:
  
    tavily_search = TavilySearch(
        max_results=5,
        topic="general",
    )

    # --- Set up LLM (OpenAI chat model) ---
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)
    tools = [tavily_search]


    # --- Build a prompt / system instruction for the agent ---
    system_prompt = f"""
    You are an AI job-search assistant. Use the tool 'tavily_search' to search LinkedIn, Naukri and Monster job listings.
    Given the user's aspirational role text, create 1-2 suitable site:linkedin.com/jobs search queries,
    call the tavily_search tool with those queries across LinkedIn, Naukri and Monster, then produce a numbered list of the top 5 matching jobs with a higher matching score.
    Higher Matching Score Calculation: Compare against the required job description and skillsets required with the job listings against the current skills provided by the user. More the matching score, more the relevance.
    Return ONLY the numbered list (1..5) with Job Title, Company, Location, URL, Matching_Score, Matching rationale, One-liner summary of the key essence of the role requirement.
    While providing the output sort them according to the matching score in descending order.
    """

    # --- Create the agent ---
    # create_agent signature may vary; many versions accept llm=llm, tools=[...], system_prompt=...
    agent_executor = create_agent(model=llm, tools=tools, system_prompt=system_prompt)


    result = agent_executor.invoke({
        "messages": [
            {"role": "user", "content": f"User's Aspirational Role: {aspirations}; User's Current Experiences: {current_skills}"}
        ]
    })
    return result["messages"][-1].content


def extract_text_from_file(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if name.endswith(".docx"):
        with NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        doc = Document(tmp_path)
        text = "\n".join(p.text for p in doc.paragraphs)
        os.remove(tmp_path)
        return text
    else:
        raise ValueError("Unsupported file type. Use .docx only")


