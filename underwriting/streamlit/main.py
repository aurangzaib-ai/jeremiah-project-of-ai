import streamlit as st
from datetime import datetime
import json
import random
import os
import re
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# LLM configuration
@st.cache_resource
def load_llm():
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    return ChatOpenAI(model="gpt-4o-preview", temperature=0)

def configure_page():
    st.set_page_config(page_title="Underwriting Evaluation", layout="wide")

def generate_random_id():
    return f"{random.randint(10000, 99999)}"

def create_form():
    st.title("Applicant Evaluation")
    first_name = st.text_input("First Name", "John")
    last_name = st.text_input("Last Name", "Doe")
    age = st.number_input("Age", 18, 99, 30)
    credit_score = st.slider("Credit Score", 300, 850, 720)
    vehicle_make = st.text_input("Vehicle Make", "Toyota")
    vehicle_model = st.text_input("Vehicle Model", "Camry")
    vehicle_year = st.number_input("Vehicle Year", 1990, 2025, 2020)
    vehicle_value = st.number_input("Vehicle Value", 1000, 100000, 25000)

    if st.button("Evaluate Applicant", use_container_width=True):
        applicant = {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "credit_score": credit_score,
            "vehicle_make": vehicle_make,
            "vehicle_model": vehicle_model,
            "vehicle_year": vehicle_year,
            "vehicle_value": vehicle_value,
            "id": generate_random_id(),
            "date": str(datetime.now())
        }
        st.session_state.applicant = applicant
        st.session_state.evaluate = True
        st.rerun()

def evaluate_applicant():
    applicant = st.session_state.get("applicant")
    if not applicant:
        st.warning("No applicant data found.")
        return

    llm = load_llm()
    st.subheader("Evaluation Results")

    prompt_template = PromptTemplate(
        input_variables=["details"],
        template="""
You are an insurance underwriter. Return ONLY strict, valid JSON. Do not include any explanation or extra text.
{
  "Decision": "ACCEPT/DENY/ADJUDICATE",
  "Reasoning": "short reason",
  "Risk_Factors": ["factor1", "factor2"]
}
Applicant Details:
{details}
        """
    )

    details = f"Name: {applicant['first_name']} {applicant['last_name']}, Age: {applicant['age']}, Credit Score: {applicant['credit_score']}, Vehicle: {applicant['vehicle_make']} {applicant['vehicle_model']} {applicant['vehicle_year']}, Value: {applicant['vehicle_value']}"
    chain = LLMChain(llm=llm, prompt=prompt_template)

    try:
        result = chain.run(details)
        st.text_area("Raw LLM Output", result, height=200)

        json_match = re.search(r"\{[\s\S]*\}", result)
        if json_match:
            json_string = json_match.group()
            try:
                parsed = json.loads(json_string)
            except json.JSONDecodeError:
                st.warning("LLM returned malformed JSON. Using safe fallback.")
                parsed = {
                    "Decision": "ACCEPT",
                    "Reasoning": "Fallback: Malformed JSON.",
                    "Risk_Factors": ["Good Credit", "Clean Record"]
                }
        else:
            st.warning("No JSON detected in the response. Using safe fallback.")
            parsed = {
                "Decision": "ACCEPT",
                "Reasoning": "Fallback: No JSON returned.",
                "Risk_Factors": ["Good Credit", "Clean Record"]
            }

    except Exception as e:
        st.warning(f"LLM call failed: {str(e)}. Using safe fallback.")
        parsed = {
            "Decision": "ACCEPT",
            "Reasoning": "Fallback: LLM call failed.",
            "Risk_Factors": ["Good Credit", "Clean Record"]
        }

    decision = parsed.get("Decision", "ACCEPT")
    reasoning = parsed.get("Reasoning", "Auto-accepted due to fallback.")
    risk_factors = parsed.get("Risk_Factors", ["Good Credit", "Clean Record"])

    st.success(f"Decision: {decision}")
    st.info(f"Reasoning: {reasoning}")
    st.write(f"Risk Factors: {', '.join(risk_factors)}")

    st.download_button(
        "Download JSON",
        json.dumps({"Decision": decision, "Reasoning": reasoning, "Risk_Factors": risk_factors}, indent=2),
        file_name=f"evaluation_{applicant['id']}.json",
        mime="application/json",
        use_container_width=True
    )

def main():
    configure_page()
    if st.session_state.get("evaluate"):
        evaluate_applicant()
        if st.button("Evaluate Another", use_container_width=True):
            st.session_state.evaluate = False
            st.rerun()
    else:
        create_form()

if __name__ == "__main__":
    main()
