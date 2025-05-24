'''
tricks.py — Skateboarding Tricks Module

This module defines the data attributes of all skateboard tricks
'''

from typing import Dict, List
import random

# Define all trick data
TRICKS = {
    # 🟢 Beginner (Round 1)
    "Ollie": {"base_score": 20, "success_rate": 0.95, "risk": 0.0, "unlock_round": 1},
    "Manual": {"base_score": 15, "success_rate": 0.9, "risk": 0.05, "unlock_round": 1},
    "Shuvit": {"base_score": 25, "success_rate": 0.85, "risk": 0.05, "unlock_round": 1},
    "Pop Shuvit": {"base_score": 30, "success_rate": 0.8, "risk": 0.1, "unlock_round": 1},
    "Frontside 180": {"base_score": 30, "success_rate": 0.85, "risk": 0.1, "unlock_round": 1},
    "Backside 180": {"base_score": 30, "success_rate": 0.85, "risk": 0.1, "unlock_round": 1},
    "Kickturn": {"base_score": 10, "success_rate": 0.95, "risk": 0.0, "unlock_round": 1},
    "Pivot": {"base_score": 15, "success_rate": 0.9, "risk": 0.05, "unlock_round": 1},

    # 🟡 Intermediate (Round 2)
    "Kickflip": {"base_score": 40, "success_rate": 0.75, "risk": 0.2, "unlock_round": 2},
    "Heelflip": {"base_score": 45, "success_rate": 0.7, "risk": 0.25, "unlock_round": 2},
    "Varial Kickflip": {"base_score": 50, "success_rate": 0.65, "risk": 0.3, "unlock_round": 2},
    "Fakie Ollie": {"base_score": 35, "success_rate": 0.8, "risk": 0.15, "unlock_round": 2},
    "Fakie Bigspin": {"base_score": 50, "success_rate": 0.6, "risk": 0.3, "unlock_round": 2},
    "Frontside Shuvit": {"base_score": 35, "success_rate": 0.8, "risk": 0.15, "unlock_round": 2},
    "Nollie": {"base_score": 40, "success_rate": 0.75, "risk": 0.2, "unlock_round": 2},

    # 🔴 Advanced (Round 3)
    "Hardflip": {"base_score": 60, "success_rate": 0.55, "risk": 0.4, "unlock_round": 3},
    "Tre Flip": {"base_score": 70, "success_rate": 0.5, "risk": 0.45, "unlock_round": 3},
    "Inward Heelflip": {"base_score": 70, "success_rate": 0.45, "risk": 0.5, "unlock_round": 3},
    "Laser Flip": {"base_score": 80, "success_rate": 0.4, "risk": 0.55, "unlock_round": 3},
    "Bigspin": {"base_score": 60, "success_rate": 0.5, "risk": 0.4, "unlock_round": 3},
    "Impossible": {"base_score": 65, "success_rate": 0.45, "risk": 0.5, "unlock_round": 3},

    # 🖤 Expert (Round 3 only)
    "Double Kickflip": {"base_score": 85, "success_rate": 0.35, "risk": 0.6, "unlock_round": 3},
    "Hospital Flip": {"base_score": 75, "success_rate": 0.4, "risk": 0.5, "unlock_round": 3},
    "360 Hardflip": {"base_score": 90, "success_rate": 0.3, "risk": 0.65, "unlock_round": 3},
    "Gazelle Flip": {"base_score": 95, "success_rate": 0.25, "risk": 0.7, "unlock_round": 3},
    "Darkslide": {"base_score": 100, "success_rate": 0.2, "risk": 0.75, "unlock_round": 3},
    "Nollie Bigspin Heelflip": {"base_score": 100, "success_rate": 0.15, "risk": 0.8, "unlock_round": 3}
}

def get_available_tricks(round_level: int, is_player: bool = True) -> List[str]:
    '''
    Return a list of available tricks based on current round and role (player/opponent).

    Parameters:
        round_level (int): Current round (1 = Qualifier, 2 = Group Stage, 3 = Final)
    '''
    available = []
    for name, data in TRICKS.items():
        # Players can only use tricks they've unlocked; opponents can use harder tricks earlier
        if is_player:
            if data["unlock_round"] <= round_level:
                available.append(name)
        else:
            # Opponents can use all tricks in the final round
            if round_level == 3 or data["unlock_round"] <= round_level:
                available.append(name)
    return available

def calculate_trick_result(trick_name: str) -> Dict[str, float]:
    '''
    Calculate the outcome of performing a trick (success, score gained/lost, injury).
        trick_name (str): Name of the trick
    '''
    
    trick_data = TRICKS[trick_name]
    success = random.random() <= trick_data["success_rate"]
    score = 0
    damage = 0

    if success:
        # Success: base score plus a random bonus (0–20%)
        score = trick_data["base_score"] * (1 + random.uniform(0, 0.2))
    else:
        # Failure: penalty based on risk, and possible injury
        score = -trick_data["base_score"] * trick_data["risk"]
        if random.random() < trick_data["risk"]:
            damage = 1

    return {
        "success": success,
        "score": round(score, 1),
        "damage": damage
    }

def print_trick_list(tricks: List[str]) -> None:
    '''Pretty-print trick list with attributes'''
    print("Available Tricks:")
    for name in tricks:
        data = TRICKS[name]
        print(f"- {name}: Base Score {data['base_score']}, Success Rate {data['success_rate']*100}%, Risk {data['risk']*100}%")

# Test block
if __name__ == "__main__":
    print("[Test] Tricks available in Round 1 for player:")
    print_trick_list(get_available_tricks(1))

    print("\n[Test] Example result for performing 'Kickflip':")
    result = calculate_trick_result("Kickflip")
    print(f"Result: {result}")