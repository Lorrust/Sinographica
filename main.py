from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original_data = pandas.read_csv("data/chinese_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer
    if finished():
        window.after_cancel(flip_timer)
        canvas.itemconfig(card_title, text="Congratulations!", fill="black")
        canvas.itemconfig(card_word, text="You learned the 100", fill="black")
        canvas.itemconfig(card_pinyin, text="most used Chinese characters!", fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        window.after(5000, window.destroy)
    else:
        current_card = random.choice(to_learn)
        window.after_cancel(flip_timer)
        canvas.itemconfig(card_title, text="Chinese", fill="black")
        canvas.itemconfig(card_word, text=current_card["Chinese"], fill="black")
        canvas.itemconfig(card_pinyin, text=current_card["Pinyin"], fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        flip_timer = window.after(3000, flip_card)
    
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_pinyin, text="", fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
    
def finished():
    if len(to_learn) == 0:
        return True
        

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(390, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(390, 263, text="", font=("Arial", 60, "bold"))
card_pinyin = canvas.create_text(390, 376, text="", font=("Arial", 30))
canvas.grid(row=0, column=0, columnspan=2)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, bd=0, command=is_known)
known_button.grid(row=1, column=1)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, bd=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()

window.mainloop()