import json
from parser import parse_submission
from config import totalNumOfTeams

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def calculate_score(team_count, quest):
    multiplier =  {1: 1, 2: 1.5, 3: 2}.get(team_count, 0)
    if quest[0] == 'E': 
        score = 10
    elif quest[0] == 'M':
        score = 20
    elif quest[0] == 'H':
        score = 30
    return score * multiplier


def score_submissions(message_file="data/raw_messages.json", score_file="data/scores.json"):
    messages = load_json(message_file)
    scores = load_json(score_file)

    for msg in messages:
        parsed, error = parse_submission(msg["text"])
        if not parsed or error:
            if error:
                print(error)
            continue

        teams = parsed["teams"]
        quest = parsed["quest"]

        # Cap team count at 3
        num_of_teams = min(len(teams), 3)
        new_score = calculate_score(num_of_teams, quest)

        for team in teams:
            t = str(team)

            if t not in scores:
                scores[t] = {
                    "total_points": 0,
                    "quests": {}
                }

            quests = scores[t]["quests"]

            if quest in quests: #case where the pair has already done the quest
                old_score = quests[quest]
                if new_score > old_score:
                    scores[t]["total_points"] += new_score - old_score
                    quests[quest] = new_score
            else: #case where the pair has yet to do the quest
                scores[t]["total_points"] += new_score
                quests[quest] = new_score

    save_json(scores, score_file)

if __name__ == "__main__":
    score_submissions()
