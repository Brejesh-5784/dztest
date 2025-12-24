import base64
import os
import sys
import json
from datetime import datetime

# --- Libraries ---
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# --- IMPORT YOUR CUSTOM SCHEMA ---
# We add the current directory to sys.path to ensure 'src' is found
sys.path.append(os.getcwd()) 

try:
    from src.schemas.prescription import PrescriptionData
except ImportError:
    print("❌ Error: Could not find 'src.schemas.prescription'.")
    print("   Make sure you are running this script from the 'HEALTHCARE-AGENT-SYSTEM' root folder.")
    exit(1)

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError("❌ GOOGLE_API_KEY not found. Please check your .env file.")

# 2. Define the Extraction Function
def extract_prescription_data(image_path: str) -> PrescriptionData:
    """
    Extracts structured medical data using your custom PrescriptionData schema.
    """
    # Using Gemini 1.5 Flash for speed (switch to 'gemini-1.5-pro' for complex handwriting)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Binds YOUR specific schema to the LLM output
    structured_llm = llm.with_structured_output(PrescriptionData)

    # Sanitize path
    clean_path = image_path.strip('"').strip("'").strip()

    if not os.path.exists(clean_path):
        raise FileNotFoundError(f"Could not find image at: {clean_path}")

    try:
        with open(clean_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Error reading image file: {e}")

    # --- UPDATED PROMPT TO MATCH YOUR SCHEMA ---
    expert_prompt = """
    You are an expert Pharmacist and Medical Data Transcriber. 
    Analyze this prescription image and extract data strictly into the requested JSON format.

    **Critical Extraction Rules:**
    1. **Context**: Identify the Doctor and Patient names clearly.
    2. **Medications**: List every drug found. If dosage (e.g., 500mg) or frequency (e.g., BD, 1-0-1) is missing, try to infer it from context, but do not hallucinate.
    3. **Handwriting Analysis**: You MUST determine if this document is handwritten or digitally printed. Set 'is_handwritten' to True or False accordingly.
    4. **Safety**: If a drug name is totally illegible, ignore it to prevent medical errors.
    
    Use the provided schema.
    """

    message = HumanMessage(
        content=[
            {"type": "text", "text": expert_prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
        ]
    )

    print(f"🤖 Analyzing image with Gemini Vision...")
    result = structured_llm.invoke([message])
    return result

# 3. Helper: Save to JSON
def save_prescription_to_file(data: PrescriptionData, source_image_path: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.basename(source_image_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_filename = f"{output_dir}/{file_name_without_ext}_{timestamp}.json"

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(data.model_dump_json(indent=4))
    
    print(f"💾 Saved extraction to: {output_filename}")

# 4. Main Execution Block
if __name__ == "__main__":
    print("--- 🏥 Healthcare Agent: Prescription Digitizer ---")
    
    while True:
        user_input = input("\n👉 Drag and drop your image file here (or type 'exit'): ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting...")
            break
            
        # Handle path cleanup
        image_path = user_input.strip('"').strip("'")
        
        if os.path.exists(image_path):
            print(f"📄 Processing: {image_path}...")
            try:
                # Step A: Extract using YOUR schema
                data = extract_prescription_data(image_path)
                
                # Step B: Display Results
                print("\n✅ Extracted Data:")
                # We access fields directly from your Pydantic model
                print(f"   Patient: {data.patient_name}")
                print(f"   Doctor:  {data.doctor_name}")
                print(f"   Type:    {'✍️ Handwritten' if data.is_handwritten else '🖨️ Digital'}")
                print(f"   Drugs Found: {len(data.medications)}")
                
                # Step C: Save
                save_prescription_to_file(data, image_path)
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print(f"❌ File not found at: {image_path}")