from services.gemini_helper import call_gemini, clean_gemini_response


def rule_based_scoring(lead, offer):
    score = 0

    # Role relevance
    role = lead.get("role", "").lower()
    if any(keyword in role for keyword in ["head", "chief", "vp", "director"]):
        score += 20
    elif any(keyword in role for keyword in ["manager", "lead"]):
        score += 10

    # Industry match
    industry = lead.get("industry", "").lower()
    icp_list = [icp.lower() for icp in offer.get("ideal_use_cases", [])]

    if any(industry == icp for icp in icp_list):
        score += 20   # exact match
    elif any(industry in icp or icp in industry for icp in icp_list):
        score += 10   # adjacent (partial overlap)
    else:
        score += 0

    # Data completeness
    if all(lead.get(field) for field in ["name", "role", "company", "industry", "location", "linkedin_bio"]):
        score += 10

    return score
def ai_based_scoring(lead: dict, offer: dict) -> dict:
    # Load base prompt from file
    with open("services\prompt.txt", "r") as f:
        base_prompt = f.read()

    # Fill in prospect + offer details
    prompt = f"""
    Prospect:
    Name: {lead.get("name")}
    Role: {lead.get("role")}
    Company: {lead.get("company")}
    Industry: {lead.get("industry")}
    Location: {lead.get("location")}
    LinkedIn Bio: {lead.get("linkedin_bio")}

    Offer:
    {offer}

    Task:
    {base_prompt}
    """

    raw_response = call_gemini(prompt)
    parsed = clean_gemini_response(raw_response)

    intent = parsed.get("intent", "Low")
    reasoning = parsed.get("reasoning", "No reasoning provided.")

    # Map intent → capped AI score (max 50)
    score_map = {"High": 50, "Medium": 30, "Low": 10}
    ai_points = score_map.get(intent, 10)

    return {
        "intent": intent,
        "ai_points": ai_points,
        "reasoning": reasoning
    }