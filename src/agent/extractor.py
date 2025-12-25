import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.models import ExtractionResult

class AIInferenceAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL_NAME", "google/gemma-3-27b:free"),
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL"),
            temperature=0
        )
        self.parser = PydanticOutputParser(pydantic_object=ExtractionResult)

    def extract(self, text: str):
        """Uses the LLM to infer structure from the raw text."""
        prompt = ChatPromptTemplate.from_template(
            "You are a Product Architecture Expert. Your goal is to extract a structured hierarchy.\n"
            "Analyze the following documentation text:\n{text}\n\n"
            "INSTRUCTIONS:\n"
            "1. Identify top-level 'Modules' (major functional areas).\n"
            "2. Identify 'Submodules' (specific features/tasks) within those modules.\n"
            "3. Write detailed descriptions based ONLY on the provided text.\n"
            "4. Ensure the output matches the JSON format exactly.\n\n"
            "{format_instructions}"
        )
        
        # Chain execution
        chain = prompt | self.llm | self.parser
        
        # Truncate text to avoid context limits (approx 100k chars is safe for Gemma)
        return chain.invoke({
            "text": text[:100000],
            "format_instructions": self.parser.get_format_instructions()
        })