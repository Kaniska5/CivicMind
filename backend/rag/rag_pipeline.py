import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent


class RAGPipeline:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )
            self.llm = ChatGroq(
                model="llama-3.1-8b-instant",
                groq_api_key=api_key,
                temperature=0.3
            )
            self.vector_store = FAISS.load_local(
                str(BASE_DIR / "data" / "vector_store"),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            # Build policy chain once at init instead of rebuilding per request
            self._policy_chain = self._build_policy_chain()
            logger.info("RAGPipeline initialised successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to initialise RAGPipeline: {e}") from e

    def _build_policy_chain(self):
        self._policy_retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        self._policy_prompt = PromptTemplate(
            template="""
            You are a helpful assistant that explains Indian government schemes.
            Use the context below to answer the question clearly and simply.

            Context: {context}
            Question: {question}

            Answer in plain language:
            """,
            input_variables=["context", "question"]
    )

    def query_policy(self, question: str) -> str:
        try:
            docs = self._policy_retriever.invoke(question)
            context = "\n".join([d.page_content for d in docs])
            prompt = self._policy_prompt.format(context=context, question=question)
            result = self.llm.invoke(prompt)
            return result.content
        except Exception as e:
            logger.error(f"query_policy failed: {e}")
            raise

    def query_grievance(self, issue: str) -> dict:
        try:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})

            dept_prompt = f"""
            Given this citizen grievance: "{issue}"
            Identify the most appropriate Indian government department.
            Reply with only the department name.
            """
            dept_response = self.llm.invoke(dept_prompt)
            department = dept_response.content

            doc_query = f"What documents are required for grievance related to {department}?"
            retriever_result = retriever.invoke(doc_query)
            docs_context = "\n".join([d.page_content for d in retriever_result])

            checklist_prompt = f"""
            Based on this context: {docs_context}
            List the documents needed to file a complaint with {department}.
            """
            checklist = self.llm.invoke(checklist_prompt).content

            letter_prompt = f"""
            Write a formal complaint letter to {department} regarding: "{issue}"
            Include placeholders for citizen name, address, and date.
            """
            letter = self.llm.invoke(letter_prompt).content

            steps_prompt = f"""
            What are the next steps after filing a complaint with {department}?
            Give a short 3-step guide.
            """
            steps = self.llm.invoke(steps_prompt).content

            return {
                "department": department,
                "documents_required": checklist,
                "complaint_letter": letter,
                "next_steps": steps
            }
        except Exception as e:
            logger.error(f"query_grievance failed: {e}")
            raise

    def query_scheme_match(self, profile: dict) -> str:
        try:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 8})
            profile_text = (
                f"Age: {profile.get('age')}, "
                f"Gender: {profile.get('gender')}, "
                f"Income: {profile.get('annual_income')}, "
                f"Caste: {profile.get('caste_category')}, "
                f"State: {profile.get('state')}, "
                f"Occupation: {profile.get('occupation')}"
            )

            retrieval_query = f"welfare schemes eligible for: {profile_text}"
            retrieved_docs = retriever.invoke(retrieval_query)
            context = "\n".join([d.page_content for d in retrieved_docs])

            reasoning_prompt = f"""
            Citizen Profile: {profile_text}

            Available Schemes Information:
            {context}

            List every welfare scheme this citizen is eligible for.
            For each scheme mention:
            1. Scheme name
            2. Why they are eligible
            3. How to apply
            """
            response = self.llm.invoke(reasoning_prompt)
            return response.content
        except Exception as e:
            logger.error(f"query_scheme_match failed: {e}")
            raise
