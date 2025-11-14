#!/usr/bin/env python3
"""
Car4Cash Eligibility Scoring Model

Uses simple, interpretable rules based on:
- Income and job stability
- Car age, mileage, and equity
- Existing debt burden (DSR)
- Loan to value (LTV)
- Credit history
- Previous customer flag
- Ownership and document readiness

Output example:
{
    "score": 78,
    "probability": 78.0,
    "risk": "Medium",
    "potential": "High",
    "bucket": "Strong",
    "dsr": 0.38,
    "ltv": 0.75,
    "features": [...],
    "summary": "..."
}
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional
from strands import tool


@dataclass
class Car4CashInput:
    income: int                       # monthly income (THB)
    employment_months: int            # months at current job
    car_year: int                     # car registration year, e.g. 2019
    car_mileage_km: int               # odometer in km
    is_car_fully_paid: bool           # True if no existing finance
    remaining_installment_months: int # if not fully paid, remaining months
    existing_monthly_debt: int        # all other monthly installments (THB)
    has_past_due: bool                # any history of overdue or NPL
    is_previous_customer: bool        # has been customer with your company
    prev_good_payer: bool             # if previous customer, did they pay well
    requested_loan_amount: int        # requested Car4Cash amount (THB)
    car_estimated_value: int          # estimated market value of the car (THB)
    owner_is_customer: bool           # registration name same as applicant
    has_full_documents: bool          # registration book, ID, etc ready
    current_year: Optional[int] = None  # override for testing


def _risk_and_bucket(score: int) -> tuple[str, str, str]:
    """
    Map score to:
    - potential: High / Medium / Low
    - risk: Low / Medium / High
    - bucket: Very Strong / Strong / Borderline / Weak
    """
    if score >= 80:
        return "High", "Low", "Very Strong"
    if score >= 65:
        return "Medium", "Medium", "Strong"
    if score >= 50:
        return "Medium", "Medium", "Borderline"
    return "Low", "High", "Weak"


def score_car4cash_eligibility(data: Car4CashInput) -> Dict[str, Any]:
    score = 0
    features: List[str] = []

    # ----------------------------
    # Derived values
    # ----------------------------
    year_now = data.current_year or datetime.now().year
    car_age = max(0, year_now - data.car_year)

    # Simple heuristic: Car4Cash installment roughly 3 percent of principal per month
    est_new_installment = int(data.requested_loan_amount * 0.03)

    income_safe = max(data.income, 1)  # avoid divide by zero
    dsr = (data.existing_monthly_debt + est_new_installment) / income_safe

    if data.car_estimated_value > 0:
        ltv = data.requested_loan_amount / data.car_estimated_value
    else:
        ltv = 1.5  # penalize unknown or zero car value

    # ----------------------------
    # Income scoring (max 25)
    # ----------------------------
    if data.income >= 40000:
        score += 25
        features.append("High and stable income (40k+).")
    elif data.income >= 25000:
        score += 20
        features.append("Good income level (25k to 40k).")
    elif data.income >= 15000:
        score += 15
        features.append("Moderate income (15k to 25k).")
    else:
        score += 8
        features.append("Low income band (below 15k).")

    # ----------------------------
    # Employment stability (max 10)
    # ----------------------------
    if data.employment_months >= 36:
        score += 10
        features.append("Strong job stability (3 years+ at current job).")
    elif data.employment_months >= 12:
        score += 7
        features.append("Good job stability (1 to 3 years).")
    elif data.employment_months >= 6:
        score += 4
        features.append("Short but acceptable job history (6 to 12 months).")
    else:
        features.append("Very short job history (under 6 months).")

    # ----------------------------
    # Car age (max 15)
    # ----------------------------
    if car_age <= 5:
        score += 15
        features.append(f"Newer car age (0 to 5 years, age {car_age}).")
    elif car_age <= 8:
        score += 10
        features.append(f"Mid age car (6 to 8 years, age {car_age}).")
    elif car_age <= 12:
        score += 5
        features.append(f"Older car (9 to 12 years, age {car_age}).")
    else:
        features.append(f"Very old car (over 12 years, age {car_age}).")

    # ----------------------------
    # Car mileage (max 10)
    # ----------------------------
    if data.car_mileage_km <= 120_000:
        score += 10
        features.append("Low mileage for age (up to 120k km).")
    elif data.car_mileage_km <= 180_000:
        score += 6
        features.append("Moderate mileage (120k to 180k km).")
    elif data.car_mileage_km <= 220_000:
        score += 3
        features.append("High mileage (180k to 220k km).")
    else:
        features.append("Very high mileage (over 220k km).")

    # ----------------------------
    # Equity in car (max 10)
    # ----------------------------
    if data.is_car_fully_paid:
        score += 10
        features.append("Car is fully paid off, full equity available.")
    else:
        if data.remaining_installment_months <= 12:
            score += 7
            features.append("Car nearly paid off, most equity available.")
        elif data.remaining_installment_months <= 24:
            score += 4
            features.append("Car mid-way through finance, some equity available.")
        else:
            features.append("Car has long remaining finance term, limited equity.")

    # ----------------------------
    # Debt burden (DSR) (max 20)
    # ----------------------------
    if dsr <= 0.35:
        score += 20
        features.append("Healthy DSR (under 35 percent after this loan).")
    elif dsr <= 0.45:
        score += 14
        features.append("Acceptable DSR (35 to 45 percent).")
    elif dsr <= 0.55:
        score += 8
        features.append("Stretched DSR (45 to 55 percent).")
    elif dsr <= 0.65:
        score += 4
        features.append("Very high DSR (55 to 65 percent).")
    else:
        features.append("Extremely high DSR (over 65 percent).")

    # ----------------------------
    # Credit history (max 8, or penalty)
    # ----------------------------
    if data.has_past_due:
        # Soft penalty by reducing potential points
        score -= 5
        features.append("Has history of overdue or problem accounts.")
    else:
        score += 8
        features.append("Clean payment history, no known overdue accounts.")

    # ----------------------------
    # Previous customer behavior (max 7)
    # ----------------------------
    if data.is_previous_customer and data.prev_good_payer:
        score += 7
        features.append("Previous customer with good payment behavior.")
    elif data.is_previous_customer:
        score += 4
        features.append("Previous customer with mixed payment record.")
    else:
        features.append("New customer (no internal track record).")

    # ----------------------------
    # Loan to value (LTV) (max 8)
    # ----------------------------
    if ltv <= 0.7:
        score += 8
        features.append("Conservative LTV (up to 70 percent of car value).")
    elif ltv <= 0.9:
        score += 5
        features.append("Reasonable LTV (70 to 90 percent).")
    elif ltv <= 1.0:
        score += 2
        features.append("Aggressive LTV (90 to 100 percent).")
    else:
        features.append("Requested amount exceeds estimated car value (LTV over 100 percent).")

    # ----------------------------
    # Ownership and documents (max 7, or penalty)
    # ----------------------------
    if data.owner_is_customer:
        score += 4
        features.append("Car registration is in the applicant's name.")
    else:
        score -= 8
        features.append("Car is not registered in the applicant's name. Higher risk.")

    if data.has_full_documents:
        score += 3
        features.append("Documents ready (registration book, ID, tax, insurance).")
    else:
        features.append("Documents not fully ready. May slow or block approval.")

    # ----------------------------
    # Clamp score and compute outputs
    # ----------------------------
    score = max(0, min(100, int(round(score))))
    probability = float(score)  # interpret score as approximate success probability
    potential, risk, bucket = _risk_and_bucket(score)

    # Build human summary
    summary_parts = [
        f"Internal score {score} out of 100, classified as {bucket} profile.",
        f"Estimated approval probability around {probability:.1f} percent with {risk} risk level.",
        f"Debt service ratio (DSR) is {dsr:.2f} and loan to value (LTV) is {ltv:.2f}.",
    ]

    if potential == "High":
        summary_parts.append("Customer is a high-potential Car4Cash prospect. Fast track and request full documents.")
    elif potential == "Medium":
        summary_parts.append("Customer is a medium-potential prospect. Consider approval with careful limit sizing.")
    else:
        summary_parts.append("Customer is a low-potential prospect. Manage expectations and consider alternative options.")

    summary = " ".join(summary_parts)

    return {
        "score": score,
        "probability": probability,
        "risk": risk,
        "potential": potential,
        "bucket": bucket,
        "dsr": round(dsr, 3),
        "ltv": round(ltv, 3),
        "features": features,
        "summary": summary,
    }


@tool
def eligibility_scoring_model(
    *,
    income: int,
    employment_months: int,
    car_year: int,
    car_mileage_km: int,
    is_car_fully_paid: bool,
    remaining_installment_months: int,
    existing_monthly_debt: int,
    has_past_due: bool,
    is_previous_customer: bool,
    prev_good_payer: bool,
    requested_loan_amount: int,
    car_estimated_value: int,
    owner_is_customer: bool,
    has_full_documents: bool,
    current_year: Optional[int] = None,
) -> Dict[str, Any]:
    """Expose the Car4Cash scoring model as a Strands tool."""
    payload = Car4CashInput(
        income=income,
        employment_months=employment_months,
        car_year=car_year,
        car_mileage_km=car_mileage_km,
        is_car_fully_paid=is_car_fully_paid,
        remaining_installment_months=remaining_installment_months,
        existing_monthly_debt=existing_monthly_debt,
        has_past_due=has_past_due,
        is_previous_customer=is_previous_customer,
        prev_good_payer=prev_good_payer,
        requested_loan_amount=requested_loan_amount,
        car_estimated_value=car_estimated_value,
        owner_is_customer=owner_is_customer,
        has_full_documents=has_full_documents,
        current_year=current_year,
    )
    return score_car4cash_eligibility(payload)

# ----------------------------------------------------
# Multiple example test cases (High + Medium + Low)
# ----------------------------------------------------
if __name__ == "__main__":
    print("\n==============================================")
    print("        RUNNING CAR4CASH SCORING TESTS        ")
    print("==============================================\n")

    # ---------------------------
    # HIGH-PROFILE CUSTOMER
    # ---------------------------
    high_profile = Car4CashInput(
        income=45000,
        employment_months=48,
        car_year=2020,
        car_mileage_km=65000,
        is_car_fully_paid=True,
        remaining_installment_months=0,
        existing_monthly_debt=5000,
        has_past_due=False,
        is_previous_customer=True,
        prev_good_payer=True,
        requested_loan_amount=180000,
        car_estimated_value=300000,
        owner_is_customer=True,
        has_full_documents=True,
    )
    high_result = score_car4cash_eligibility(high_profile)

    print("------------ HIGH PROFILE TEST -------------")
    print(f"Score: {high_result['score']}/100")
    print(f"Probability: {high_result['probability']:.1f}%")
    print(f"Risk: {high_result['risk']}")
    print(f"Potential: {high_result['potential']}")
    print(f"Bucket: {high_result['bucket']}")
    print(f"DSR: {high_result['dsr']}")
    print(f"LTV: {high_result['ltv']}")
    print("Key Factors:")
    for f in high_result["features"]:
        print(" -", f)
    print("Summary:", high_result["summary"])
    print("--------------------------------------------\n")

    # ---------------------------
    # MEDIUM-PROFILE CUSTOMER
    # ---------------------------
    medium_profile = Car4CashInput(
        income=22000,                      # decent income, not premium
        employment_months=14,              # stable
        car_year=2015,                     # mid-aged car
        car_mileage_km=140000,             # slightly high but ok
        is_car_fully_paid=False,
        remaining_installment_months=10,   # near finished finance
        existing_monthly_debt=6000,        # some debt
        has_past_due=False,                # clean payment
        is_previous_customer=False,
        prev_good_payer=False,
        requested_loan_amount=120000,
        car_estimated_value=180000,        # healthy LTV
        owner_is_customer=True,
        has_full_documents=True,
    )
    medium_result = score_car4cash_eligibility(medium_profile)

    print("----------- MEDIUM PROFILE TEST ------------")
    print(f"Score: {medium_result['score']}/100")
    print(f"Probability: {medium_result['probability']:.1f}%")
    print(f"Risk: {medium_result['risk']}")
    print(f"Potential: {medium_result['potential']}")
    print(f"Bucket: {medium_result['bucket']}")
    print(f"DSR: {medium_result['dsr']}")
    print(f"LTV: {medium_result['ltv']}")
    print("Key Factors:")
    for f in medium_result["features"]:
        print(" -", f)
    print("Summary:", medium_result["summary"])
    print("--------------------------------------------\n")

    # ---------------------------
    # LOW-PROFILE CUSTOMER
    # ---------------------------
    low_profile = Car4CashInput(
        income=10000,
        employment_months=3,
        car_year=2010,
        car_mileage_km=220000,
        is_car_fully_paid=False,
        remaining_installment_months=40,
        existing_monthly_debt=7000,
        has_past_due=True,
        is_previous_customer=False,
        prev_good_payer=False,
        requested_loan_amount=150000,
        car_estimated_value=120000,
        owner_is_customer=False,
        has_full_documents=False,
    )
    low_result = score_car4cash_eligibility(low_profile)

    print("------------- LOW PROFILE TEST -------------")
    print(f"Score: {low_result['score']}/100")
    print(f"Probability: {low_result['probability']:.1f}%")
    print(f"Risk: {low_result['risk']}")
    print(f"Potential: {low_result['potential']}")
    print(f"Bucket: {low_result['bucket']}")
    print(f"DSR: {low_result['dsr']}")
    print(f"LTV: {low_result['ltv']}")
    print("Key Factors:")
    for f in low_result["features"]:
        print(" -", f)
    print("Summary:", low_result["summary"])
    print("--------------------------------------------\n")
