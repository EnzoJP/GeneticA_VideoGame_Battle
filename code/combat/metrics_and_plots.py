def record_combat(damage_done, damage_taken, turns, won): 
    #combat stats
    return {
        "damage_done": damage_done,
        "damage_taken": damage_taken,
        "turns": turns,
        "won": won
    }

def calculate_win_rate (wins, losses):
    """Calculate the win rate as a percentage."""
    total = wins + losses
    if total == 0:
        return 0.0
    return (wins / total) * 100




