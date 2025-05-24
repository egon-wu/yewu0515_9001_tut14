'''
game.py — Main Skateboarding Championship Script

Controls the full tournament flow:
- Setup player
- Loop through 3 rounds
- Handle victory/loss logic
'''

from player import Player
from tricks import get_available_tricks
from competition import generate_opponent, run_round

def intro():
    print("=" * 60)
    print("🛹 Welcome to the World Skateboarding Championship! 🛹")
    print("You'll face 3 intense 1v1 battles: Qualifier, Group Stage, and Final.")
    print("Win each round by scoring more or surviving your opponent!")
    print("=" * 60)

def outro(win: bool):
    print("\n🎬 Championship Results")
    if win:
        print("🏆 Congratulations! You are the new world skateboarding champion!")
    else:
        print("💀 You’ve been eliminated from the championship.")
    print("Thanks for playing. See you next season!")

def main():
    intro()

    player_name = input("Enter your skater name: ").strip()
    player = Player(player_name)

    round_titles = {
        1: "🏁 Qualifier Round",
        2: "🔥 Group Stage",
        3: "👑 Grand Final"
    }

    for round_num in range(1, 4):
        print(f"\n=== {round_titles[round_num]} ===")

        player.current_round = round_num
        player.available_tricks = get_available_tricks(player.current_round, is_player=True)

        opponent = generate_opponent(round_num)
        did_win, result_msg = run_round(player, opponent)

        print("\n🧾 Match Summary:", result_msg)

        if not did_win:
            outro(False)
            return

if __name__ == "__main__":
    main()