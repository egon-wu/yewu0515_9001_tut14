'''
player.py — Skateboard Player Class Module

Defines the Player class, used to manage the state of both the player and AI opponents,
including score, health, available tricks, and round progression.
'''

from typing import List
from tricks import get_available_tricks, calculate_trick_result

class Player:
    def __init__(self, name: str, is_player: bool = True):
        '''
        Initialize a player instance.
        
        Parameters:
            name (str): Player's name
            is_player (bool): Whether this is the user player (True) or an AI opponent (False)
        '''
        self.name = name
        self.score = 0.0
        self.health = 3          # Health (max is 3, decreases when injured)
        self.current_round = 1   # Current competition round (1 = Qualifier, 2 = Group Stage, 3 = Final)
        self.is_player = is_player
        self.available_tricks: List[str] = get_available_tricks(
            self.current_round, is_player=self.is_player
        )

    def perform_trick(self, trick_name: str, allow_any: bool = False) -> dict:
        if self.health <= 0:
            raise ValueError(f"{self.name} can no longer compete (health is 0)!")

        if not allow_any and trick_name not in self.available_tricks:
            raise ValueError(f"Trick {trick_name} is not unlocked or available!")

        result = calculate_trick_result(trick_name)
        self.score += result["score"]

        if result["damage"] > 0:
            self.take_damage(result["damage"])

        return result

    def take_damage(self, amount: int = 1):
        # Reduce health (minimum 0)
        self.health = max(0, self.health - amount)

    def heal(self, amount: int = 1):
        # Recover health (maximum 3)
        self.health = min(3, self.health + amount)

    def unlock_next_round(self):
        # Advance to the next round and update available tricks
        if self.current_round >= 3:
            print(f"{self.name} is already in the final and cannot advance further.")
            return
        self.current_round += 1
        self.available_tricks = get_available_tricks(
            self.current_round, is_player=self.is_player
        )

    def reset_round(self, reset_score: bool = False):
        '''
        Reset player state for a new opponent in the current round.
            reset_score (bool): Whether to reset score to zero 
        '''
        self.health = 3
        if reset_score:
            self.score = 0.0

    def __str__(self) -> str:
        # Return a status report of the player
        tricks_list = '\n  '.join([f"{i+1}. {trick}" for i, trick in enumerate(self.available_tricks)])
        return (
            f"{self.name} Status:\n"
            f"- Current Round: Round {self.current_round}\n"
            f"- Score: {self.score:.1f}\n"
            f"- Health: {'❤' * self.health}{'🖤' * (3 - self.health)}\n"
            f"- Available Tricks:\n  {tricks_list}"
            )


# Test code
if __name__ == "__main__":
    player = Player("Skateboard boy")
    print(player)
    
    try:
        print("\nTrying trick 'Ollie':")
        result = player.perform_trick("Ollie")
        print(f"Result: {result}")
        print(player)
    except ValueError as e:
        print(e)
    
    print("\nAdvancing to Group Stage...")
    player.unlock_next_round()
    print(player)