import tkinter as tk
from PIL import Image, ImageTk
import random

class RockPaperScissorsGame:
    def __init__(self, master):
        self.master = master
        self.master.title("石头剪刀布游戏")

        self.player_score = 0
        self.computer_score = 0
        self.round_count = 0
        self.max_rounds = 0

        self.canvas = tk.Canvas(self.master, width=800, height=400)
        self.canvas.pack()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="请选择石头、剪刀或布")
        self.label.pack()

        self.rock_button = tk.Button(self.master, text="石头", command=lambda: self.play_round("rock"))
        self.rock_button.pack(side=tk.LEFT, padx=10)

        self.paper_button = tk.Button(self.master, text="布", command=lambda: self.play_round("paper"))
        self.paper_button.pack(side=tk.LEFT, padx=10)

        self.scissors_button = tk.Button(self.master, text="剪刀", command=lambda: self.play_round("scissors"))
        self.scissors_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.master, text="重新开始游戏", command=self.reset_game)
        self.restart_button.pack()

        self.score_label = tk.Label(self.master, text=f"玩家分数: {self.player_score}  电脑分数: {self.computer_score}")
        self.score_label.pack()

        self.rounds_entry = tk.Entry(self.master)
        self.rounds_entry.pack()

        self.start_button = tk.Button(self.master, text="开始比赛", command=self.start_game)
        self.start_button.pack()

    def play_round(self, player_choice):
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)

        result = self.determine_winner(player_choice, computer_choice)

        self.label.config(text=f"你选择了：{player_choice}  电脑选择了：{computer_choice}  结果：{result}")
        self.update_score(result)

        self.animate(player_choice, computer_choice, result)

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return "平局"
        elif (player_choice == "rock" and computer_choice == "scissors") or \
                (player_choice == "paper" and computer_choice == "rock") or \
                (player_choice == "scissors" and computer_choice == "paper"):
            return "你赢了！"
        else:
            return "电脑赢了！"

    def update_score(self, result):
        if result == "你赢了！":
            self.player_score += 1
        elif result == "电脑赢了！":
            self.computer_score += 1

        self.round_count += 1
        self.score_label.config(text=f"玩家分数: {self.player_score}  电脑分数: {self.computer_score}")

        if self.round_count >= self.max_rounds:
            self.end_game()

    def start_game(self):
        try:
            self.max_rounds = int(self.rounds_entry.get())
        except ValueError:
            self.max_rounds = 0

        self.label.config(text="比赛开始！")
        self.round_count = 0
        self.player_score = 0
        self.computer_score = 0
        self.score_label.config(text=f"玩家分数: {self.player_score}  电脑分数: {self.computer_score}")

    def end_game(self):
        self.label.config(text="比赛结束！")
        if self.player_score > self.computer_score:
            self.label.config(text="你赢了比赛！")
        elif self.computer_score > self.player_score:
            self.label.config(text="电脑赢了比赛！")
        else:
            self.label.config(text="比赛结束，平局！")

    def reset_game(self):
        self.round_count = 0
        self.player_score = 0
        self.computer_score = 0
        self.score_label.config(text=f"玩家分数: {self.player_score}  电脑分数: {self.computer_score}")
        self.label.config(text="游戏已重置，请重新开始比赛。")

    def animate(self, player_choice, computer_choice, result):
        try:
            self.canvas.delete("all")  # Clear the canvas

            # Define the image paths based on the choices
            images = {
                "rock": "images/rock.png",
                "paper": "images/paper.png",
                "scissors": "images/scissors.png"
            }

            # Load and resize player and computer hand images
            player_hand_img = Image.open(images[player_choice]).resize((150, 150), Image.LANCZOS)
            computer_hand_img = Image.open(images[computer_choice]).resize((150, 150), Image.LANCZOS)

            # Convert images to tkinter format
            player_hand_tk = ImageTk.PhotoImage(player_hand_img)
            computer_hand_tk = ImageTk.PhotoImage(computer_hand_img)

            # Display images on the canvas
            self.canvas.create_image(100, 100, image=player_hand_tk)
            self.canvas.create_image(300, 100, image=computer_hand_tk)

            # Show result text
            self.canvas.create_text(200, 180, text=result, fill="black", font=("Helvetica", 16))

            # Update the canvas to display the changes
            self.canvas.update_idletasks()

            # Animate the result text by changing its position
            for i in range(180, 300, 10):
                self.canvas.move("text", 0, i)
                self.master.after(50)  # Wait 50 milliseconds

        except FileNotFoundError as e:
            print(e)
            self.label.config(text="图片文件未找到，请检查路径。")

        # Free up the images to prevent memory leaks
        player_hand_tk._photo = None
        computer_hand_tk._photo = None


if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()



