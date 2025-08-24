import re
from config import totalNumOfTeams

def is_valid_quest_code(quest_code):
    if quest_code.startswith('E'):
        return 1 <= int(quest_code[1:]) <= 20
    elif quest_code.startswith('M'):
        return 1 <= int(quest_code[1:]) <= 20
    elif quest_code.startswith('H'):
        return 1 <= int(quest_code[1:]) <= 16
    return False

def is_valid_team_number(teams):
    for team in teams:
        if int(team) > totalNumOfTeams or int(team) < 1:
            return False
    return True

def parse_submission(text):
    # Only process if header matches exactly
    if not text.lower().startswith("drabroski quest submission"):
        return None, None

    error_info = {
        "error": "invalid submission format",
        "text": text,
        "reason": ""
    }

    teams_match = re.search(r"Teams?(?:\(s\))?:\s*([\d,\s]+)", text, re.IGNORECASE)
    quest_match = re.search(r"Quest(?:s|\(s\))?:\s*([EMH]\d{1,2})", text, re.IGNORECASE)

    if not teams_match:
        error_info["reason"] = "Missing or incorrect team list"
        return None, error_info

    if not quest_match:
        error_info["reason"] = "Missing or incorrect quest code"
        return None, error_info

    try:
        teams = [int(t.strip()) for t in teams_match.group(1).split(",")]
        quest_code = quest_match.group(1).upper()

        if not is_valid_quest_code(quest_code):
            error_info["reason"] = f"Quest code out of allowed range: {quest_code}"
            return None, error_info
        
        if not is_valid_team_number(teams):
            error_info["reason"] = f"Team number out of allowed range: {teams}"
            return None, error_info

        return {
            "teams": sorted(teams),
            "quest": quest_code
        }, None

    except ValueError:
        error_info["reason"] = "Non-numeric team values"
        return None, error_info
