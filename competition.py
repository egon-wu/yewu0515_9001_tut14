'''
competition.py — Match Logic Module

Handles 1v1 competition between the player and an AI opponent
across different rounds: Qualifier, Group Stage, and Final.
'''

import random
import time
from player import Player
from tricks import get_available_tricks
from typing import Tuple

MAX_TURNS_PER_ROUND = 3  # Each side gets 3 chances per round

def generate_opponent(round_level: int) -> Player:
    names = {
        1: ["Ryan", "Chloe", "Sam"],
        2: ["Tom Penny", "Rob Dyrdek", "Sean"],
        3: ["Nyjah Huston", "Tony Hawk", "Andrew Reynolds"]
    }
    opponent_name = random.choice(names[round_level])
    opponent = Player(opponent_name, is_player=False)
    opponent.current_round = round_level
    return opponent

def run_round(player: Player, opponent: Player) -> Tuple[bool, str]:
    # Reset state before match
    player.reset_round()
    opponent.reset_round()
    opponent.score = 0.0

    print(f"\n🛹 Starting Round {player.current_round} - Match vs {opponent.name}")
    print("\n" + "=" * 50)

    for turn in range(1, MAX_TURNS_PER_ROUND + 1):
        print("\n" + "=" * 50)
        print(f"\n🔄 Turn {turn}")

        # 💡 Use different level moves each turn
        trick_level = {1: 1, 2: 2, 3: 3}[turn]
        trick_list = get_available_tricks(trick_level, is_player=True)

        # --- Player's turn ---
        print(f"\n{player.name}'s turn:")
        print(f"{player.name} Status:")
        print(f"- Current Round: Round {player.current_round}")
        print(f"- Score: {player.score:.1f}")
        print(f"- Health: {'❤' * player.health}{'🖤' * (3 - player.health)}")
        print(f"- Available Tricks:")
        for i, trick in enumerate(trick_list):
            print(f"  {i+1}. {trick}")

        while True:
            choice = input("Choose a trick by number: ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(trick_list)):
                print("❌ Invalid choice. Please enter a number between 1 and", len(trick_list))
            else:
                trick = trick_list[int(choice) - 1]
                print(f"✅ You selected: {trick}")
                break

        try:
            result = player.perform_trick(trick, allow_any=True)  
            print(f"🎯 Success: {result['success']}, Score change: {result['score']:.1f}")
            if result["damage"] > 0:
                print(f"💥 You took damage! Health reduced by {result['damage']}.")
                print(f"❤️ Remaining Health: {'❤' * player.health}{'🖤' * (3 - player.health)}")
            else:
                print(f"✅ No damage taken. Health: {'❤' * player.health}{'🖤' * (3 - player.health)}")
        except ValueError as e:
            print(e)
            continue

        if player.health == 0:
            print(f"{player.name} is injured and can't continue!")
            return False, f"{player.name} lost due to injury."

        # --- Opponent's turn ---
        print("\n" + "=" * 50)
        print(f"\n{opponent.name}'s turn:")
        time.sleep(1)
        opp_trick_list = get_available_tricks(trick_level, is_player=False)
        opp_trick = random.choice(opp_trick_list)
        result = opponent.perform_trick(opp_trick, allow_any=True)  


        print(f"{opponent.name} performed '{opp_trick}' - 🎯 Success: {result['success']}, Score: {result['score']:.1f}")
        if result["damage"] > 0:
            print(f"💥 {opponent.name} took damage! Remaining Health: {'❤' * opponent.health}{'🖤' * (3 - opponent.health)}")
        else:
            status = ["💀 Knocked Out", "💔 Critical", "💛 Injured", "💚 Full"][opponent.health]
            print(f"✅ {opponent.name} avoided damage. Health: {'❤' * opponent.health}{'🖤' * (3 - opponent.health)} ({opponent.health}/3, {status})")

        if opponent.health == 0:
            print(f"{opponent.name} is injured and can't continue!")
            return True, f"{opponent.name} lost due to injury."

    # After turns, compare scores
    print("\n⏱ End of Match")
    print(f"{player.name}'s score: {player.score:.1f}")
    print(f"{opponent.name}'s score: {opponent.score:.1f}")

    if player.score > opponent.score:
        return True, f"{player.name} wins the round!"
    elif player.score < opponent.score:
        return False, f"{opponent.name} wins the round!"
    else:
        if player.health > opponent.health:
            return True, f"Scores tied, but {player.name} had better form (more health)!"
        elif player.health < opponent.health:
            return False, f"Scores tied, but {opponent.name} had better form (more health)!"
        else:
            return False, f"Match ends in a tie. Judges favored {opponent.name}!"