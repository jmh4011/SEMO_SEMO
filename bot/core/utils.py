from typing import List

def shuffle_and_split(members: List[int], team_count: int) -> List[List[str]]:
    import random
    random.shuffle(members)
    teams: List[List[str]] = [[] for _ in range(team_count)]
    for i, uid in enumerate(members):
        teams[i % team_count].append(f"<@{uid}>")
    return teams
