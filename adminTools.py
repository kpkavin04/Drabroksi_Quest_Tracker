from datetime import datetime
import json
import argparse
from config import totalHighDiffTeams, totalMedDiffTeams, totalLowDiffTeams

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def flag_entry(message_id, reason, admin="admin"):
    flags = load_json("data/flags.json")
    flags[str(message_id)] = {
        "reason": reason,
        "admin": admin,
        "date": datetime.now().isoformat()
    }
    save_json(flags, "data/flags.json")

def override_total_score(team_id, new_total, admin="admin"):
    scores = load_json("data/scores.json")
    team = str(team_id)
    if team in scores:
        scores[team]["total_points"] = new_total
        save_json(scores, "data/scores.json")
        print(f"[Override Total Score] Total score of {team_id} has been overriden")

    flags = load_json("data/flags.json")
    flags[f"override_team_{team}"] = {
        "action": "total score overridden",
        "new_score": new_total,
        "admin": admin,
        "date": datetime.now().isoformat()
    }
    save_json(flags, "data/flags.json")

def override_quest_score(team_id, questCode, newQuestScore, admin="admin"):
    scores = load_json("data/scores.json")
    team = str(team_id)
    if team in scores:
        oldQuestScore = scores[team]["quests"][questCode]
        scores[team]["quests"][questCode] = newQuestScore 
        scores[team]["total_points"] += newQuestScore - oldQuestScore
        save_json(scores, "data/scores.json")
        print(f"[Override Quest Score] quest score of {team_id} has been overriden")

def sort_scores_by_team_id(score_file="data/scores.json"):
    scores = load_json(score_file)

    # Sort the dictionary by numeric team ID (not string)
    sorted_scores = dict(sorted(scores.items(), key=lambda item: int(item[0])))

    save_json(sorted_scores, score_file)
    print(f"[SORT] scores.json has been sorted by team ID.")

from config import totalHighDiffTeams, totalMedDiffTeams, totalLowDiffTeams

def display_leaderboard(score_file="data/scores.json"):
    scores = load_json(score_file)

    high_diff_teams = [2, 3, 6, 8, 10, 11, 12, 15, 16, 17, 19, 20, 25, 29, 37]     
    med_diff_teams = [1, 4, 5, 7, 9, 13, 14, 18, 21, 22, 23, 24, 26, 28, 30, 31, 32, 33, 35, 38, 40]  
    low_diff_teams = [27, 34, 36, 39]  

    # Group containers
    groups = {
        "High commitment": [],
        "Medium commitment": [],
        "Low commitment": []
    }

    # Mapping for quick membership check
    group_membership = {
        "High commitment": set(high_diff_teams),
        "Medium commitment": set(med_diff_teams),
        "Low commitment": set(low_diff_teams)
    }

    for team_id_str, data in scores.items():
        team_id = int(team_id_str)
        entry = {
            "team": team_id,
            "total_points": data["total_points"]
        }

        # Put team in the correct difficulty bucket
        for group_name, team_set in group_membership.items():
            if team_id in team_set:
                groups[group_name].append(entry)
                break

    print("\n=== Drabroski Leaderboard ===")
    for group_name, entries in groups.items():
        print(f"\n{group_name}:")
        if not entries:
            print("  No teams in this group.")
            continue

        # Sort entries by total_points descending
        sorted_entries = sorted(entries, key=lambda x: x["total_points"], reverse=True)

        # Extract top 3 unique scores
        top_scores = []
        for e in sorted_entries:
            if e["total_points"] not in top_scores:
                top_scores.append(e["total_points"])
            if len(top_scores) == 3:
                break

        # Include all teams whose score is in the top 3 tiers
        final_leaderboard = [e for e in sorted_entries if e["total_points"] in top_scores]

        for team in final_leaderboard:
            print(f"  Team {team['team']} - {team['total_points']} pts")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Admin tools for Drabroski Quest Tracker")

    subparsers = parser.add_subparsers(dest="command", help="Admin commands")

    # --override-total
    total_parser = subparsers.add_parser("override-total", help="Override total score for a team")
    total_parser.add_argument("team_id", type=int, help="Team ID")
    total_parser.add_argument("new_total", type=float, help="New total score")
    total_parser.add_argument("--admin", type=str, default="admin", help="Admin name")

    # --override-quest
    quest_parser = subparsers.add_parser("override-quest", help="Override quest score for a team")
    quest_parser.add_argument("team_id", type=int, help="Team ID")
    quest_parser.add_argument("quest_code", type=str, help="Quest Code (e.g. H1, M2)")
    quest_parser.add_argument("new_score", type=float, help="New quest score")
    quest_parser.add_argument("--admin", type=str, default="admin", help="Admin name")

    # --flag
    flag_parser = subparsers.add_parser("flag", help="Flag a message by message ID")
    flag_parser.add_argument("message_id", type=int, help="Telegram Message ID")
    flag_parser.add_argument("reason", type=str, help="Reason for flag")
    flag_parser.add_argument("--admin", type=str, default="admin", help="Admin name")

    # --sort
    sort_parser = subparsers.add_parser("sort", help="Sort scores.json by team ID")

    # --leaderboard
    leaderboard_parser = subparsers.add_parser("leaderboard", help="Show top 3 teams for each difficulty group")


    args = parser.parse_args()

    # Dispatch commands
    if args.command == "override-total":
        override_total_score(args.team_id, args.new_total, args.admin)
    elif args.command == "override-quest":
        override_quest_score(args.team_id, args.quest_code, args.new_score, args.admin)
    elif args.command == "flag":
        flag_entry(args.message_id, args.reason, args.admin)
    elif args.command == "sort":
        sort_scores_by_team_id()
    elif args.command == "leaderboard":
        display_leaderboard()

    else:
        parser.print_help()
