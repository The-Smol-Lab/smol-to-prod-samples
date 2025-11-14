#!/usr/bin/env python3

"""
Simple Refinance Loan Eligibility Predictor
Easy logic for field sales to understand.

If customer owns NO car:
    -> Refinance probability is ALWAYS 0
"""

from typing import Dict, Any, List, Optional


# --------------------------------------
# Helper for bucket + risk
# --------------------------------------
def _risk_and_bucket(score: int) -> tuple[str, str]:
    if score >= 80:
        return "Low", "Very Strong"
    if score >= 65:
        return "Medium", "Strong"
    if score >= 50:
        return "Medium", "Borderline"
    return "High", "Weak"


# --------------------------------------
# Output wrapper
# --------------------------------------
def _wrap(score: int, probability: float, features: List[Dict[str, Any]]) -> Dict[str, Any]:
    max_score = 100
    score = max(0, min(score, max_score))
    probability = max(0, probability)

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


# --------------------------------------
# Refinance model
# --------------------------------------
def predict_refinance_success(
    income: int,
    months_paid: Optional[int] = None,
    is_previous_customer: bool = False,
    has_existing_car: bool = False,
    previous_product: Optional[str] = None,
) -> Dict[str, Any]:

    score = 0
    features: List[Dict[str, Any]] = []

    # -------------------------------
    # 0. Hard rule: no car → no refinance
    # -------------------------------
    if not has_existing_car:
        # Still compute score for transparency
        # But probability is forced to 0 downstream
        features.append({"feature": "no_car", "pts": 0})
    else:
        score += 20
        features.append({"feature": "existing_car", "pts": 20})

    # -------------------------------
    # 1. Income strength
    # -------------------------------
    if income >= 50000:
        score += 35
        features.append({"feature": "income", "pts": 35})
    elif income >= 30000:
        score += 25
        features.append({"feature": "income", "pts": 25})
    else:
        score += 15
        features.append({"feature": "income", "pts": 15})

    # -------------------------------
    # 2. Payment history
    # -------------------------------
    if has_existing_car:
        if months_paid is None:
            months_paid = 0

        if months_paid >= 24:
            score += 25
            features.append({"feature": "months_paid", "pts": 25})
        elif months_paid >= 12:
            score += 15
            features.append({"feature": "months_paid", "pts": 15})
        elif months_paid > 0:
            score += 5
            features.append({"feature": "months_paid", "pts": 5})
        else:
            features.append({"feature": "months_paid", "pts": 0})
    else:
        # Never owned a car
        features.append({"feature": "months_paid", "pts": 0})

    # -------------------------------
    # 3. Previous customer bonus
    # -------------------------------
    if is_previous_customer:
        score += 10
        features.append({"feature": "previous_customer", "pts": 10})

    # -------------------------------
    # 4. Previous product fit
    # -------------------------------
    if previous_product in {"New Car", "Used Car"}:
        score += 5
        features.append({"feature": "product_match", "pts": 5})

    # -------------------------------
    # FINAL PROBABILITY
    # -------------------------------
    if not has_existing_car:
        # Hard override
        probability = 0.0
    else:
        probability = round(score, 1)  # simple linear conversion

    return _wrap(score, probability, features)


# --------------------------------------
# Example usage
# --------------------------------------
if __name__ == "__main__":
    result = predict_refinance_success(
        income=50000,
        months_paid=18,           # ignored because no car
        is_previous_customer=False,
        has_existing_car=True,     # customer owns NO car
        previous_product=True,
    )

    print("\n=== Refinance Eligibility Example ===")
    print(result["summary"])
