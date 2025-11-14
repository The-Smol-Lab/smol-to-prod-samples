#!/usr/bin/env python3

"""
New Car Loan Eligibility Scoring Model (Demo)
- For sales team use over phone
- Interpretable, rule-based, believable logic
- Outputs: score, probability, risk bucket, recommendations
"""

def predict_car_loan_eligibility(
        monthly_income: int,
        age: int,
        employment_type: str,
        job_tenure_years: float,
        has_existing_loans: bool,
        residence_status: str,
        marital_status: str) -> dict:
    """
    Computes overall eligibility score and risk bucket.
    All ranges & rules are realistic for new car loan screening.
    """

    score = 0
    max_score = 100

    # ---- Income Score (max 30 points) ----
    # New car monthly payment often 7k - 12k → minimum 2.5x safer
    if monthly_income < 15000:
        score += 5
    elif monthly_income < 25000:
        score += 15
    elif monthly_income < 40000:
        score += 22
    else:
        score += 30

    # ---- Age Score (max 15 points) ----
    if age < 20:
        score -= 10
    elif age <= 25:
        score += 5
    elif age <= 45:
        score += 15
    elif age <= 60:
        score += 10
    else:
        score -= 5

    # ---- Employment Type (max 20 points) ----
    emp = employment_type.lower()
    if emp in ["government officer", "civil servant", "state enterprise"]:
        score += 20
    elif emp in ["private employee", "engineer", "teacher", "office staff"]:
        score += 15
    elif emp in ["freelancer", "self-employed"]:
        score += 8
    else:
        score += 3

    # ---- Job Tenure (max 10 points) ----
    if job_tenure_years < 0.5:
        score += 2
    elif job_tenure_years < 1:
        score += 5
    elif job_tenure_years < 3:
        score += 7
    else:
        score += 10

    # ---- Existing Loans (max 10 points) ----
    if has_existing_loans:
        score += 3  # some existing loans is normal
    else:
        score += 10  # clean profile

    # ---- Residence Stability (max 10 points) ----
    res = residence_status.lower()
    if res in ["own", "family"]:
        score += 10
    elif res == "rent":
        score += 5
    else:
        score += 3

    # ---- Marital Status (max 5 points) ----
    ms = marital_status.lower()
    if ms == "married":
        score += 5
    elif ms in ["single", "divorced"]:
        score += 3
    else:
        score += 2

    # Final probability conversion
    score = max(0, min(score, max_score))
    prob = round((score / max_score) * 100, 2)

    # ---- Risk Bucketing ----
    if prob < 40:
        bucket = "Very Low"
        action = "Reject or request guarantor + high down payment."
    elif prob < 60:
        bucket = "Low"
        action = "Proceed with caution; request more documents."
    elif prob < 80:
        bucket = "Medium"
        action = "Standard underwriting."
    else:
        bucket = "High"
        action = "Fast-track approval recommended."

    return {
        "score": score,
        "probability": prob,
        "bucket": bucket,
        "action": action,
        "ranges": {
            "Very Low": "0 to 39 percent",
            "Low": "40 to 59 percent",
            "Medium": "60 to 79 percent",
            "High": "80 to 100 percent",
        }
    }


if __name__ == "__main__":
    print("=== New Car Loan Eligibility Demo ===")

    # Sample demo values (representative of a typical applicant)
    customer = {
        "monthly_income": 38000,
        "age": 30,
        "employment_type": "private employee",
        "job_tenure_years": 2.5,
        "has_existing_loans": True,
        "residence_status": "rent",
        "marital_status": "single",
    }

    result = predict_car_loan_eligibility(**customer)

    print("\n--- Result ---")
    print(f"Eligibility Score: {result['score']} / 100")
    print(f"Success Probability: {result['probability']}%")
    print(f"Bucket: {result['bucket']}")
    print(f"Recommended Action: {result['action']}")
    print("\nRanges:")
    for k, v in result["ranges"].items():
        print(f"  {k}: {v}")
    print()
