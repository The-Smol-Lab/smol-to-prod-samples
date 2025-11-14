#!/usr/bin/env python3

"""
Loan success scoring model with interpretability,
categorization, and recommended next steps.

Run:
    python loan_success_model_demo.py
"""

def predict_loan_success(income: int,
                         age: int,
                         occupation: str,
                         residence_status: str,
                         marital_status: str) -> dict:
    """
    Computes:
      - score (0 to 100)
      - probability (percentage)
      - bucket (Very Low / Low / Medium / High)
      - recommended action
      - interpretation ranges
    """

    score = 0
    max_score = 100

    # ---- Income Score (max 40 points) ----
    if income < 15000:
        score += 5
    elif income < 30000:
        score += 15
    elif income < 50000:
        score += 25
    else:
        score += 40

    # ---- Age Score (max 20 points) ----
    if age < 21:
        score -= 10
    elif age <= 25:
        score += 5
    elif age <= 45:
        score += 15
    elif age <= 60:
        score += 10
    else:
        score -= 5

    # ---- Occupation Score (max 20 points) ----
    occ = occupation.lower()
    if occ in ["government officer", "civil servant", "bank employee"]:
        score += 20
    elif occ in ["private employee", "engineer", "teacher"]:
        score += 15
    elif occ in ["freelancer", "self-employed"]:
        score += 8
    else:
        score += 5

    # ---- Residence Stability (max 10 points) ----
    res = residence_status.lower()
    if res in ["own", "family"]:
        score += 10
    elif res == "rent":
        score += 5
    else:
        score += 2

    # ---- Marital Status (max 10 points) ----
    ms = marital_status.lower()
    if ms == "married":
        score += 10
    elif ms in ["single", "divorced"]:
        score += 5
    else:
        score += 3

    # Bound score
    score = max(0, min(score, max_score))
    prob = round((score / max_score) * 100, 2)

    # ---- Categorize into risk buckets ----
    if prob < 40:
        bucket = "Very Low"
        action = "Avoid approval unless strong guarantor provided."
    elif prob < 60:
        bucket = "Low"
        action = "Request more supporting documents or guarantor."
    elif prob < 80:
        bucket = "Medium"
        action = "Proceed with normal underwriting."
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
    print("=== Loan Success Probability Demo ===")

    demo_data = {
        "income": 40000,
        "age": 32,
        "occupation": "engineer",
        "residence_status": "rent",
        "marital_status": "single",
    }

    result = predict_loan_success(
        income=demo_data["income"],
        age=demo_data["age"],
        occupation=demo_data["occupation"],
        residence_status=demo_data["residence_status"],
        marital_status=demo_data["marital_status"],
    )

    print("\n--- Result ---")
    print(f"Score: {result['score']} / 100")
    print(f"Success Probability: {result['probability']}%")
    print(f"Bucket: {result['bucket']}")
    print(f"Recommended Action: {result['action']}")
    print("\nRanges:")
    for k, v in result["ranges"].items():
        print(f"  {k}: {v}")
    print()
