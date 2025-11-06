import tkinter as tk
import random
from collections import defaultdict

class RockPaperScissorsAI:
    def __init__(self):
        self.human_history = []
        self.ai_history = []
        self.pattern_memory = defaultdict(int)

    def get_ai_move(self):
       
        if len(self.human_history) < 3:
            return random.choice(['R', 'P', 'S'])
        
        recent_pattern = ''.join(self.human_history[-2:])
        pattern_counts = {'R': 0, 'P': 0, 'S': 0}
        
        for i in range(len(self.human_history) - 2):
            if ''.join(self.human_history[i:i+2]) == recent_pattern and i + 2 < len(self.human_history):
                next_move = self.human_history[i + 2]
                pattern_counts[next_move] += 1
        
        if sum(pattern_counts.values()) > 0:
            predicted_human_move = max(pattern_counts, key=pattern_counts.get)
            if predicted_human_move == 'R':
                return 'P'
            elif predicted_human_move == 'P':
                return 'S'
            else:
                return 'R'
        else:
            return random.choice(['R', 'P', 'S'])

    def play_round(self, human_move):
        ai_move = self.get_ai_move()
        self.human_history.append(human_move)
        self.ai_history.append(ai_move)
        return ai_move

    def determine_winner(self, human_move, ai_move):
        if human_move == ai_move:
            return "tie"
        elif (human_move == 'R' and ai_move == 'S') or \
             (human_move == 'P' and ai_move == 'R') or \
             (human_move == 'S' and ai_move == 'P'):
            return "human"
        else:
            return "ai"


class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors - Adaptive AI")
        self.root.geometry("400x420")
        self.root.config(bg="#f0f4f8")

        self.game = RockPaperScissorsAI()
        self.scores = {'human': 0, 'ai': 0, 'tie': 0}

        self.title_label = tk.Label(root, text="🎮 Rock Paper Scissors (AI Mode)", 
                                    font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#333")
        self.title_label.pack(pady=10)

        self.result_label = tk.Label(root, text="Make your move!", 
                                     font=("Arial", 14), bg="#f0f4f8", fg="#007acc")
        self.result_label.pack(pady=15)

        self.button_frame = tk.Frame(root, bg="#f0f4f8")
        self.button_frame.pack(pady=10)

        self.rock_btn = tk.Button(self.button_frame, text="Rock", width=10, bg="#cce7ff", 
                                  fg="black", command=lambda: self.play("R"))
        self.paper_btn = tk.Button(self.button_frame, text="Paper", width=10, bg="#cce7ff", 
                                   fg="black", command=lambda: self.play("P"))
        self.scissors_btn = tk.Button(self.button_frame, text="Scissors", width=10, bg="#cce7ff", 
                                      fg="black", command=lambda: self.play("S"))

        self.rock_btn.grid(row=0, column=0, padx=5)
        self.paper_btn.grid(row=0, column=1, padx=5)
        self.scissors_btn.grid(row=0, column=2, padx=5)

        self.score_label = tk.Label(root, text="Score - You: 0 | AI: 0 | Ties: 0", 
                                    font=("Arial", 12), bg="#f0f4f8", fg="#333")
        self.score_label.pack(pady=15)

        self.ai_feedback = tk.Label(root, text="", font=("Arial", 11, "italic"), bg="#f0f4f8", fg="gray")
        self.ai_feedback.pack(pady=5)

        self.reset_btn = tk.Button(root, text="Reset Game", width=15, bg="#f7d7d7", command=self.reset_game)
        self.reset_btn.pack(pady=10)

    def play(self, human_move):
        ai_move = self.game.play_round(human_move)
        result = self.game.determine_winner(human_move, ai_move)

        move_names = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
        result_text = f"You chose {move_names[human_move]}, AI chose {move_names[ai_move]}.\n"

        if result == "human":
            result_text += "🎉 You win this round!"
        elif result == "ai":
            result_text += "🤖 AI wins this round!"
        else:
            result_text += "🤝 It's a tie!"

        self.scores[result] += 1
        self.result_label.config(text=result_text)
        self.score_label.config(text=f"Score - You: {self.scores['human']} | AI: {self.scores['ai']} | Ties: {self.scores['tie']}")

        # AI learning feedback
        if len(self.game.human_history) > 5:
            self.ai_feedback.config(text="🤖 AI is learning your move patterns...")
        else:
            self.ai_feedback.config(text="")

        # After 10 rounds, declare winner
        if len(self.game.human_history) == 15:
            self.declare_final_winner()

    def declare_final_winner(self):
        if self.scores['human'] > self.scores['ai']:
            final_msg = f"🎉 Game Over! You won the match!\nFinal Score - You: {self.scores['human']} | AI: {self.scores['ai']}"
        elif self.scores['ai'] > self.scores['human']:
            final_msg = f"🤖 Game Over! AI won the match!\nFinal Score - You: {self.scores['human']} | AI: {self.scores['ai']}"
        else:
            final_msg = f"🤝 Game Over! It's a tie!\nFinal Score - You: {self.scores['human']} | AI: {self.scores['ai']}"

        self.result_label.config(text=final_msg)
        self.disable_buttons()

    def disable_buttons(self):
        self.rock_btn.config(state="disabled")
        self.paper_btn.config(state="disabled")
        self.scissors_btn.config(state="disabled")

    def reset_game(self):
        self.game = RockPaperScissorsAI()
        self.scores = {'human': 0, 'ai': 0, 'tie': 0}
        self.result_label.config(text="Make your move!")
        self.score_label.config(text="Score - You: 0 | AI: 0 | Ties: 0")
        self.ai_feedback.config(text="")
        self.rock_btn.config(state="normal")
        self.paper_btn.config(state="normal")
        self.scissors_btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    RockPaperScissorsGUI(root)
    root.mainloop()
