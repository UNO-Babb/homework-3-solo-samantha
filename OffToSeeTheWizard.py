from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Game state
game_data = {
    "current_player": 1,
    "positions": [0, 0],  # Player positions (0-indexed, start at square 1)
    "log": [],  # Event log
    "special_squares": {  # Special square effects
        7: "Glinda's Crown",
        14: "Toto",
        21: "Wicked Witch",
        28: "Flying Monkeys"
    },
    "num_squares": 31  # Total number of squares
}

@app.route("/")
def index():
    return render_template("index.html", game_data=game_data)

@app.route("/roll_dice")
def roll_dice():
    try:
        dice_roll = random.randint(1, 6)
        player = game_data["current_player"] - 1  # Current player (0 or 1)
        game_data["positions"][player] += dice_roll  # Move player forward
        game_data["log"].append(f"Player {game_data['current_player']} rolled a {dice_roll}.")

        # Ensure players don't exceed the final square
        if game_data["positions"][player] >= game_data["num_squares"]:
            game_data["positions"][player] = game_data["num_squares"]
            game_data["log"].append(f"Player {game_data['current_player']} wins!")
            return jsonify(game_data)

        # Handle special squares
        current_square = game_data["positions"][player]
        if current_square in game_data["special_squares"]:
            effect = game_data["special_squares"][current_square]
            if effect == "Glinda's Crown":
                game_data["log"].append(f"Player {game_data['current_player']} landed on Glinda's Crown and earns another roll!")
                dice_roll = random.randint(1, 6)
                game_data["positions"][player] += dice_roll
                game_data["log"].append(f"Player {game_data['current_player']} rolled a {dice_roll} and moved forward again.")
            elif effect == "Toto":
                game_data["log"].append(f"Player {game_data['current_player']} landed on Toto. The next player earns an extra roll!")
            elif effect == "Wicked Witch":
                game_data["log"].append(f"Player {game_data['current_player']} landed on Wicked Witch and moves back 3 spaces.")
                game_data["positions"][player] = max(0, game_data["positions"][player] - 3)
            elif effect == "Flying Monkeys":
                game_data["log"].append(f"Player {game_data['current_player']} landed on Flying Monkeys. The next player moves back 3 spaces before their turn.")

        # Handle tornado (both players on the same square)
        if game_data["positions"][0] == game_data["positions"][1] and game_data["positions"][0] != 0:
            game_data["log"].append("Tornado! Both players move back 3 spaces.")
            for i in range(2):
                game_data["positions"][i] = max(0, game_data["positions"][i] - 3)

        # Switch turns
        game_data["current_player"] = 2 if game_data["current_player"] == 1 else 1

        return jsonify(game_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)