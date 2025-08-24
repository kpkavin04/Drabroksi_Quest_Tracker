# Drabroski Quest Tracker

## usage directions
1. edit the config.py with the right API ID, API Hash, Group Username and team details
```
API_ID = 
API_HASH = 
SESSION_NAME = 
GROUP_USERNAME = 
totalNumOfTeams = 41
totalHighDiffTeams = 10
totalMedDiffTeams = 10
totalLowDiffTeams = 10
```

2. Retrieve raw messages that match the given template starting with "Drabroski Quest Submission"
``` python
python main.py
```

3. Assign points based on the quest submissions
```python
python scorer.py
```

4. Make use of adminTools.py to:
    1. sort the scores.json file according to the team number 
       ```python
            python adminTools.py sort
       ```
    2. produce a CLI leaderboard
       ```python
            python adminTools.py leaderboard
       ```


