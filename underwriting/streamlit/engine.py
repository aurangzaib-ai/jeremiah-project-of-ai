# engine.py

def evaluate_applicant_with_ai(prompt):
    """
    Mock underwriting evaluation function for free testing with app.py.
    """
    print("⚠️ GPT API call disabled. Showing free mock response.")
    return (
        "✅ Mock Underwriting Decision: Application Accepted.\n"
        "Reason: Excellent Credit, Clean Record, No Claims.\n"
        "Note: This is a free mock response for workflow testing. GPT evaluation requires an active API key with credits."
    )

if __name__ == "__main__":
    test_prompt = "Applicant: John Doe, Age: 37, Credit Score: 720, Vehicle: 2020 Toyota Camry. Evaluate risk and provide underwriting decision."
    result = evaluate_applicant_with_ai(test_prompt)
    print(result)
