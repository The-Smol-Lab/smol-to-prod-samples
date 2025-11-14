#!/usr/bin/env python3

"""
Simple Refinance Loan Eligibility Predictor
- Easy logic for field sales to understand
- Based only on 4 key factors:
      1. Income
      2. Months already paid
      3. Whether customer already owns a car
      4. Whether customer is previous customer

Output:
{
    "score": int,
    "probability": float,
    "risk": str,
    "bucket": str,
    "features": list,
    "summary": str
}
"""

from typing import Dict, Any, List, Optional


# ------------------------------
# Helper for bucket + risk
# ------------------------------
def _risk_and_bucket(score: int) -> tuple[str, str]:
    if score >= 80:
        return "Low", "Very Strong"
    if score >= 65:
        return "Medium", "Strong"
    if score >= 50:
        return "Medium", "Borderline"
    return "High", "Weak"


# ------------------------------
# Simple wrap formatter
# ------------------------------
def _wrap(score: int, features: List[Dict[str, Any]]) -> Dict[str, Any]:
    max_score = 100
    score = max(0, min(score, max_score))
    probability = round(score / max_score * 100, 1)

    risk, bucket = _risk_and_bucket(score)

    summary = (
        f"Loan Type: Refinance\n"
        f"Predicted Approval Probability: {probability} percent\n"
        f"Risk Category: {risk}\n"
        f"Profile Bucket: {bucket}\n"
        f"Internal Score: {score}/{max_score}\n"
    )

    return {
        "score": score,
        "probability": probability,
        "risk": risk,
        "bucket": bucket,
        "features": features,
        "summary": summary,
    }


# ------------------------------
# REFINANCE MODEL (Simplified)
# ------------------------------
def predict_refinance_success(
    income: int,
    months_paid: Optional[int] = None,
    is_previous_customer: bool = False,
    has_existing_car: bool = False,
    previous_product: Optional[str] = None,
) -> Dict[str, Any]:

    score = 0
    features: List[Dict[str, Any]] = []

    # 1. Income strength
    if income >= 50000:
        score += 35
        features.append({"feature": "income", "pts": 35})
    elif income >= 30000:
        score += 25
        features.append({"feature": "income", "pts": 25})
    else:
        score += 15
        features.append({"feature": "income", "pts": 15})

    # 2. Payment history
    if months_paid is not None:
        if months_paid >= 24:
            score += 25
            features.append({"feature": "months_paid", "pts": 25})
        elif months_paid >= 12:
            score += 15
            features.append({"feature": "months_paid", "pts": 15})
        else:
            score += 5
            features.append({"feature": "months_paid", "pts": 5})

    # 3. Customer already has a car → refinance natural fit
    if has_existing_car:
        score += 20
        features.append({"feature": "existing_car", "pts": 20})

    # 4. Previous customer bonus
    if is_previous_customer:
        score += 10
        features.append({"feature": "previous_customer", "pts": 10})

    # 5. Product match (if their old loan was also a car loan)
    if previous_product in {"New Car", "Used Car"}:
        score += 5
        features.append({"feature": "product_match", "pts": 5})

    return _wrap(score, features)


# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    result = predict_refinance_success(
        income=32000,
        months_paid=18,
        is_previous_customer=True,
        has_existing_car=True,
        previous_product="New Car",
    )

    print("\n=== Refinance Eligibility Example ===")
    print(result["summary"])
