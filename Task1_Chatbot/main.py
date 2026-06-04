import customtkinter as ctk 
import os
import sys
from datetime import datetime
from tkinter import Scrollbar

from chatbot import Chatbot

bot = Chatbot("MyChatBot")

#Configuration

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app=ctk.CTk()
app.title("My Chatbot - AI Assistant")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
app.minsize(600,400)

#Color Theme

class Theme:
    BG_COLOR = "#0a0f1a"
    SUB_BG_COLOR = "#131d2e"
    CHAT_BG = "#0D1521"

    ACCENT_BLUE = "#3498db"
    ACCENT_LIGHT = "#5dade2"
    DARK_BLUE = "#1f4e79"

    BUTTON_COLOR = "#2874a6"
    BUTTON_HOVER = "#3498db"
    BUTTON_TEXT = "#ffffff"

    TEXT_PRIMARY = "#e8f4fc"
    TEXT_SECONDARY = "#a0b4c4"
    TEXT_MUTED = "#5a6a7a"

    USER_BG = "#1e3a5f"
    USER_TEXT = "#ffffff"
    BOT_BG = "#1a2633"
    BOT_TEXT = "#c8dae6"
    TIMESTAMP = "#4a5a6a"

    STATUS_BG = "#0d1521"
    STATUS_TEXT = "#5a6a7a"

app.configure(fg_color=Theme.BG_COLOR)

#Main container

main_container = ctk.CTkFrame(
    app,
    fg_color=Theme.BG_COLOR,
    corner_radius=0,
    border_width=0
)
main_container.pack(fill="both", expand=True, padx=0,pady=0)

main_container.grid_rowconfigure(0, weight=10)
main_container.grid_rowconfigure(1, weight=0)
main_container.grid_rowconfigure(2, weight=0)
main_container.grid_columnconfigure(0, weight=1)

chat_frame = ctk.CTkFrame(
    main_container,
    fg_color=Theme.CHAT_BG,
    corner_radius=0,
    border_width=0
)
chat_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

chat_frame.grid_rowconfigure(0, weight=0)
chat_frame.grid_rowconfigure(1, weight=1)
chat_frame.grid_columnconfigure(0,weight=1)

#Messages textbox

chat_textbox = ctk.CTkTextbox(
    chat_frame,
    font=("Segoe UI",13),
    text_color=Theme.TEXT_PRIMARY,
    fg_color=Theme.CHAT_BG,
    border_width=0,
    corner_radius=0,
    wrap="word",
    state="disabled"
)

chat_textbox.grid(row=1, column=0, sticky="nsew", padx=(25,0), pady=(0,15))

scrollbar = Scrollbar(
    chat_frame,
    orient="vertical",
    command=chat_textbox.yview,
    troughcolor=Theme.CHAT_BG,
    activebackground=Theme.BUTTON_COLOR,
    background=Theme.BUTTON_COLOR,
    width=12
)

scrollbar.grid(row=1, column=1, sticky="ns", padx=(0,15), pady=(0,15))

#Text tags config

chat_textbox.configure(yscrollcommand=scrollbar.set) 

def add_message_to_chat(sender,message):
    chat_textbox.configure(state="normal")
    timestamp = datetime.now().strftime("%H:%M")
    chat_textbox.insert("end",f"[{timestamp}] ", "timestamp")

    if sender == "user":
        sender_label = "You"
    else:
        sender_label = bot.name
    
    chat_textbox.insert("end", f"{sender_label}: ",sender)
    chat_textbox.insert("end", f"{message}\n\n",sender)
    chat_textbox.configure(state="disabled")
    chat_textbox.see("end")

    update_status()

def update_status():
    count = bot.get_conversation_count()
    status_label.configure(
        text=f"Messages: {count} | Bot: Online"
    )

chat_title = ctk.CTkLabel(
    chat_frame,
    text="My Chatbot",
    font=("Segoe UI",18,"bold"),
    text_color=Theme.TEXT_PRIMARY
)
chat_title.grid(row=0, column=0, padx=25, pady=(20,10), sticky="w")

input_frame = ctk.CTkFrame(
    main_container,
    fg_color=Theme.SUB_BG_COLOR,
    corner_radius=0,
    border_width=0
)
input_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

input_frame.grid_rowconfigure(0, weight=1)
input_frame.grid_columnconfigure(0, weight=10)
input_frame.grid_columnconfigure(1, weight=1)

user_label = ctk.CTkLabel(
    input_frame,
    text="You:",
    font=("Segoe UI",14,"bold"),
    text_color=Theme.ACCENT_BLUE
)
user_label.grid(row=0, column=0, padx=(25,10), pady=20, sticky="w")

#Input box

user_input = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your message here...",
    placeholder_text_color=Theme.TEXT_MUTED,
    font=("Segoe UI",14),
    text_color=Theme.TEXT_PRIMARY,
    fg_color=Theme.BG_COLOR,
    border_color=Theme.DARK_BLUE,
    border_width=2,
    corner_radius=10,
    height=50
)

user_input.grid(row=0, column=0, padx=(70,15), pady=15, sticky="ew")

#Send button

send_button = ctk.CTkButton(
    input_frame,
    text="Send ➤",
    font=("Segoe UI",14,"bold"),
    text_color=Theme.BUTTON_TEXT,
    fg_color=Theme.BUTTON_COLOR,
    hover_color=Theme.BUTTON_HOVER,
    border_width=0,
    corner_radius=10,
    height=50,
    width=100
)

send_button.grid(row=0, column=1, padx=(0,25), pady=15, sticky="ew")

status_frame = ctk.CTkFrame(
    main_container,
    fg_color=Theme.STATUS_BG,
    corner_radius=0,
    border_width=0,
    height=30
)
status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)

status_frame.grid_rowconfigure(0,weight=1)
status_frame.grid_columnconfigure(0,weight=1)
status_frame.grid_columnconfigure(1,weight=0)

status_label = ctk.CTkLabel(
    status_frame,
    text=f"Messages: 0 | Bot: Online",
    font=("Segoe UI", 11),
    text_color=Theme.STATUS_TEXT
)
status_label.grid(row=0, column=0, padx=25, pady=(5,5), sticky="w")

version_label = ctk.CTkLabel(
    status_frame,
    text="v1.0 | Rule-Based Chatbot",
    font=("Segoe UI",10),
    text_color=Theme.TEXT_MUTED
)
version_label.grid(row=0, column=1, padx=(25,25), pady=(5,5), sticky="e")

#Event handlers

def on_send_click():
    user_message = user_input.get().strip()

    if user_message:
        add_message_to_chat("user",user_message)

        user_input.delete(0, "end")

        #Connection to chatbot

        bot_response = bot.process_input(user_message)

        add_message_to_chat("bot",bot_response)

    else:
        print("Empty message!")

def on_enter_key(event):
    on_send_click()

#Bind events

send_button.configure(command=on_send_click)
user_input.bind("<Return>", on_enter_key)

user_input.focus()

welcome_message = """Hello! Welcome to My Chatbot!

I'm a rule-based AI assistant built with Python.
Ask me about:
- Current time or date
- Jokes
- General questions
- Just say hi!

How can I help you today?"""
add_message_to_chat("bot",welcome_message)

app.mainloop()