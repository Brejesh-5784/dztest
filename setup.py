import os
import sys

# Define the project name
PROJECT_NAME = "healthcare-agent-system"

# Define the file content for key files
REQUIREMENTS_TXT = """
langchain==0.1.0
langchain-openai
langchain-google-genai
langgraph
pinecone-client
pydantic
streamlit
python-dotenv
llama-index
llama-parse
"""

GITIGNORE = """
# Environments
.env
venv/
env/
__pycache__/
.DS_Store

# IDE
.vscode/
.idea/

# Data
data/raw_policies/*
data/medical_images/*
!data/raw_policies/.gitkeep
!data/medical_images/.gitkeep
"""

README_MD = """
# Multimodal Healthcare Prior Authorization System

## Overview
This system combines Vision-Language Models (VLMs), RAG, and Agentic Workflows to automate prior authorization.

## Components
1. **Vision Agent:** OCRs and structures medical images.
2. **Librarian Agent:** Retrieves policy rules from vector DB.
3. **Decider Agent:** Reasons between patient data and policy rules.
4. **Writer Agent:** Drafts approvals or appeals.

## Setup
1. `python -m venv venv`
2. `source venv/bin/activate` (or `venv\\Scripts\\activate` on Windows)
3. `pip install -r requirements.txt`
4. `cp .env.example .env` (and add your API keys)
"""

ENV_EXAMPLE = """
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_ENV=your_env_here
"""

PATIENT_DATA_PY = """
from pydantic import BaseModel, Field
from typing import Optional, List

class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str

class PatientData(BaseModel):
    patient_id: Optional[str] = Field(None, description="The unique ID of the patient")
    patient_name: Optional[str] = Field(None, description="Name of the patient")
    diagnosis_icd10: Optional[str] = Field(None, description="ICD-10 code found in document")
    medications: List[Medication] = []
    physician_signature_present: bool = Field(False, description="Is the doctor's signature detected?")
    confidence_score: float = Field(0.0, description="Confidence of the extraction (0-1)")
"""

CONFIG_PY = """
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
"""

MAIN_PY = """
import streamlit as st

st.set_page_config(page_title="Healthcare Prior Auth Agent", page_icon="🏥", layout="wide")

st.title("🏥 Multimodal Prior Authorization Agent")

with st.sidebar:
    st.header("Upload Medical Records")
    uploaded_file = st.file_uploader("Upload Prescription/X-Ray", type=['png', 'jpg', 'pdf'])
    
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Medical Record")
    st.info("Agent starting analysis...")
    # TODO: Connect to Agent Workflow here
"""

# Define the structure
structure = {
    PROJECT_NAME: {
        ".vscode": {
            "settings.json": '{\n  "editor.formatOnSave": true,\n  "python.formatting.provider": "none",\n  "[python]": {\n    "editor.defaultFormatter": "ms-python.black-formatter"\n  }\n}'
        },
        "data": {
            "raw_policies": {".gitkeep": ""},
            "medical_images": {".gitkeep": ""},
            "synthetic_ehr": {".gitkeep": ""},
            "vector_store": {".gitkeep": ""}
        },
        "notebooks": {
            "01_ocr_test.ipynb": "{}",
            "02_rag_retrieval.ipynb": "{}",
            "03_agent_loop.ipynb": "{}"
        },
        "src": {
            "__init__.py": "",
            "agents": {
                "__init__.py": "",
                "vision.py": "# Code for Subdivision 1: OCR & Vision extraction\n",
                "librarian.py": "# Code for Subdivision 2: Pinecone RAG retrieval\n",
                "decider.py": "# Code for Subdivision 3: Reasoning Engine\n",
                "writer.py": "# Code for Subdivision 4: Appeal/API writing\n"
            },
            "core": {
                "__init__.py": "",
                "config.py": CONFIG_PY,
                "llm_setup.py": "# Initialize LLM clients (OpenAI/Gemini) here\n",
                "prompts.py": "# Store all system prompts here\n"
            },
            "graph": {
                "__init__.py": "",
                "state.py": "# Define LangGraph State definitions here\n",
                "workflow.py": "# Define the graph nodes and edges here\n"
            },
            "schemas": {
                "__init__.py": "",
                "patient_data.py": PATIENT_DATA_PY
            }
        },
        "app": {
            "main.py": MAIN_PY,
            "style.css": "/* Custom medical UI styles */"
        },
        ".env.example": ENV_EXAMPLE,
        ".gitignore": GITIGNORE,
        "requirements.txt": REQUIREMENTS_TXT,
        "README.md": README_MD,
        "docker-compose.yml": "# Optional: Redis or Postgres config"
    }
}

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # It's a directory
            os.makedirs(path, exist_ok=True)
            print(f"📁 Created directory: {path}")
            create_structure(path, content)
        else:
            # It's a file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📄 Created file: {path}")

def main():
    print(f"🚀 Initializing {PROJECT_NAME}...")
    current_dir = os.getcwd()
    create_structure(current_dir, structure)
    print("\n✅ Project structure created successfully!")
    print("\nNext Steps:")
    print(f"1. cd {PROJECT_NAME}")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  (or .\\venv\\Scripts\\activate on Windows)")
    print("4. pip install -r requirements.txt")
    print("5. Rename .env.example to .env and add your API keys.")

if __name__ == "__main__":
    main()