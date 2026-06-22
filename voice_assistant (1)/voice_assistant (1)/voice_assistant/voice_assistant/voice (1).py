import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import speech_recognition as sr
import webbrowser
import os
import pyttsx3
import datetime
import wikipedia
import requests
import json
import sys
import subprocess
from PIL import Image, ImageTk
import pyautogui
import screen_brightness_control as sbc
import psutil
import winsound
import math

# ============= CONFIGURATION =============
ASSISTANT_NAME = "MIRA"
VERSION = "1.5"

# ---------------- Voice Engine ----------------
def speak(text):
    try:
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Female voice
        engine.setProperty('rate', 165)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        log(f"🤖 {ASSISTANT_NAME}: {text}", "assistant")
    except Exception as e:
        log(f"Voice error: {str(e)}", "error")

# ---------------- Speech Recognition ----------------
def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            update_status("🎤 Listening...", "listening")
            show_wave_animation(True)
            recognizer.pause_threshold = 0.8
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            show_wave_animation(False)

        command = recognizer.recognize_google(audio, language='en-in')
        log(f"👤 You: {command}", "user")
        return command.lower()
    except sr.WaitTimeoutError:
        log("Listening timeout", "system")
        return ""
    except sr.UnknownValueError:
        speak("I didn't catch that. Could you repeat?")
        return ""
    except Exception as e:
        log(f"Microphone error: {str(e)}", "error")
        return ""

# ---------------- Enhanced Assistant Brain ----------------
def assistant():
    update_status("🟢 Active", "active")
    speak(f"I am {ASSISTANT_NAME}, your voice assistant. How can I help you?")

    while True:
        command = listen()
        if not command:
            continue

        # Basic Commands
        if "open google" in command:
            speak("Opening Google Chrome")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open notepad" in command:
            speak("Opening Notepad")
            os.system("notepad")

        elif "open calculator" in command:
            speak("Opening Calculator")
            os.system("calc")

        elif "open camera" in command:
            speak("Opening Camera")
            os.system("start microsoft.windows.camera:")

        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        elif "date" in command:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}")

        elif "day" in command:
            day = datetime.datetime.now().strftime("%A")
            speak(f"Today is {day}")

        # System Commands
        elif "screenshot" in command:
            speak("Taking screenshot")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot = pyautogui.screenshot()
            screenshot.save(f"screenshot_{timestamp}.png")
            speak("Screenshot saved successfully")

        elif "brightness" in command:
            if "increase" in command:
                current = sbc.get_brightness()[0]
                new = min(100, current + 20)
                sbc.set_brightness(new)
                speak(f"Brightness increased to {new} percent")
            elif "decrease" in command:
                current = sbc.get_brightness()[0]
                new = max(0, current - 20)
                sbc.set_brightness(new)
                speak(f"Brightness decreased to {new} percent")

        # Web Search
        elif "search" in command or "wikipedia" in command:
            query = command.replace("search", "").replace("wikipedia", "").strip()
            if query:
                speak(f"Searching {query}")
                try:
                    result = wikipedia.summary(query, sentences=2)
                    speak(f"According to Wikipedia, {result}")
                    log(f"📚 Wikipedia: {result}", "info")
                except:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    speak("Here are the search results")

        # Weather
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            if city:
                try:
                    api_key = "your_api_key_here"  # Replace with your API key
                    weather_data = get_weather(city, api_key)
                    speak(weather_data)
                except:
                    speak("Sorry, I couldn't fetch weather information")

        # System Info
        elif "battery" in command:
            battery = psutil.sensors_battery()
            percent = battery.percent
            speak(f"Battery is at {percent} percent")

        elif "volume" in command:
            if "up" in command:
                winsound.Beep(1000, 200)
                speak("Volume increased")
            elif "down" in command:
                winsound.Beep(500, 200)
                speak("Volume decreased")

        # Math
        elif "calculate" in command or "what is" in command:
            try:
                # Simple math parsing
                if "plus" in command:
                    nums = command.replace("calculate", "").replace("what is", "").split("plus")
                    result = sum(float(n.strip()) for n in nums if n.strip().replace('.', '').isdigit())
                elif "multiply" in command:
                    nums = command.replace("calculate", "").replace("what is", "").split("multiply")
                    result = 1
                    for n in nums:
                        if n.strip().replace('.', '').isdigit():
                            result *= float(n.strip())
                else:
                    speak("I can calculate addition and multiplication")
                    continue
                speak(f"The result is {result}")
            except:
                speak("I couldn't calculate that")

        # Assistant Control
        elif "your name" in command:
            speak(f"My name is {ASSISTANT_NAME}, your personal voice assistant")

        elif "who made you" in command or "creator" in command:
            speak("I was created by a developer who wanted to make life easier")

        elif "thank you" in command:
            speak("You're welcome! Is there anything else I can help with?")

        elif "sleep" in command or "wait" in command:
            speak("I'll be here when you need me")
            update_status("🌙 Sleeping", "sleep")
            break

        elif "exit" in command or "quit" in command or "goodbye" in command:
            speak(f"Goodbye! Have a great day")
            root.after(1000, root.destroy)
            break

        elif "clear" in command:
            output.config(state="normal")
            output.delete(1.0, tk.END)
            output.config(state="disabled")

        else:
            if len(command) > 3:  # Ignore very short phrases
                speak("I didn't understand that command. Try saying help for available commands")

# ---------------- Helper Functions ----------------
def get_weather(city, api_key):
    """Fetch weather data"""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        weather_desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature}°C with {weather_desc}. Humidity is {humidity}%."
    else:
        return "City not found"

def show_wave_animation(show):
    if show:
        animation_label.config(image=wave_gif)
    else:
        animation_label.config(image=idle_gif)

def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    if voice_enabled:
        voice_btn.config(text="🔊 Voice ON", bg="#10b981")
        speak("Voice enabled")
    else:
        voice_btn.config(text="🔇 Voice OFF", bg="#ef4444")
        log("Voice disabled", "system")

# ---------------- UI Helpers ----------------
def log(message, msg_type="system"):
    """Add colored messages to log"""
    colors = {
        "user": "#60a5fa",        # Blue
        "assistant": "#34d399",   # Green
        "system": "#94a3b8",      # Gray
        "error": "#f87171",       # Red
        "info": "#fbbf24"         # Yellow
    }
    
    output.config(state="normal")
    tag = f"tag_{msg_type}"
    output.tag_config(tag, foreground=colors.get(msg_type, "#ffffff"))
    output.insert(tk.END, message + "\n", tag)
    output.config(state="disabled")
    output.see(tk.END)

def update_status(text, state="idle"):
    """Update status with color coding"""
    colors = {
        "idle": "#64748b",
        "active": "#10b981",
        "listening": "#3b82f6",
        "sleep": "#8b5cf6",
        "error": "#ef4444"
    }
    status_label.config(text=f"● {text}", fg=colors.get(state, "#64748b"))

# ---------------- Thread Starter ----------------
def start_assistant():
    threading.Thread(target=assistant, daemon=True).start()

def show_help():
    help_text = """Available Commands:
    • Open Google/YouTube/Notepad/Calculator/Camera
    • What's the time/date/day?
    • Take screenshot
    • Increase/decrease brightness
    • Search [topic] / Wikipedia [topic]
    • Weather [city]
    • Battery status
    • Calculate [math]
    • What's your name?
    • Sleep / Exit / Clear
    • Volume up/down"""
    
    help_window = tk.Toplevel(root)
    help_window.title(f"{ASSISTANT_NAME} - Help")
    help_window.geometry("400x500")
    help_window.configure(bg="#1e293b")
    
    tk.Label(help_window, text="📚 Command Guide", font=("Segoe UI", 16, "bold"),
             bg="#1e293b", fg="#38bdf8").pack(pady=10)
    
    help_box = ScrolledText(help_window, width=45, height=25, bg="#0f172a", 
                           fg="#cbd5e1", font=("Consolas", 10))
    help_box.pack(padx=15, pady=10)
    help_box.insert(1.0, help_text)
    help_box.config(state="disabled")

# ============= ENHANCED UI DESIGN =============
root = tk.Tk()
root.title(f"🎙️ {ASSISTANT_NAME} - Voice Assistant v{VERSION}")
root.geometry("700x650")
root.configure(bg="#0f172a")

# Load images (placeholder GIFs - you can replace with actual images)
try:
    idle_gif = tk.PhotoImage(file="")  # Add path to idle image
    wave_gif = tk.PhotoImage(file="")  # Add path to wave animation
except:
    # Create placeholder images
    idle_gif = tk.PhotoImage(width=100, height=100)
    wave_gif = tk.PhotoImage(width=100, height=100)

# Header Frame
header_frame = tk.Frame(root, bg="#0f172a")
header_frame.pack(fill=tk.X, pady=(15, 5))

# Assistant Avatar and Name
avatar_frame = tk.Frame(header_frame, bg="#0f172a")
avatar_frame.pack(side=tk.LEFT, padx=20)

tk.Label(avatar_frame, text="🤖", font=("Segoe UI", 48),
         bg="#0f172a", fg="#38bdf8").pack()

tk.Label(avatar_frame, text=ASSISTANT_NAME, font=("Segoe UI", 24, "bold"),
         bg="#0f172a", fg="#ffffff").pack()

# Version and Status
info_frame = tk.Frame(header_frame, bg="#0f172a")
info_frame.pack(side=tk.RIGHT, padx=20)

tk.Label(info_frame, text=f"v{VERSION}", font=("Segoe UI", 10),
         bg="#0f172a", fg="#64748b").pack(anchor="e")

status_label = tk.Label(info_frame, text="● Idle", font=("Segoe UI", 12),
                        bg="#0f172a", fg="#64748b")
status_label.pack(anchor="e", pady=(10, 0))

# Animation Display
animation_label = tk.Label(root, image=idle_gif, bg="#0f172a")
animation_label.pack(pady=10)

# Output Log
output_frame = tk.Frame(root, bg="#0f172a")
output_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

tk.Label(output_frame, text="Conversation Log", font=("Segoe UI", 12, "bold"),
         bg="#0f172a", fg="#94a3b8").pack(anchor="w")

output = ScrolledText(output_frame, state="disabled", height=15,
                     bg="#020617", fg="#e5e7eb", insertbackground="white",
                     font=("Consolas", 10), relief="flat", bd=0)
output.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

# Control Buttons
button_frame = tk.Frame(root, bg="#0f172a")
button_frame.pack(pady=15)

voice_enabled = True
voice_btn = tk.Button(button_frame, text="🔊 Voice ON", font=("Segoe UI", 10),
                     bg="#10b981", fg="white", padx=15, pady=5,
                     relief="flat", command=toggle_voice)
voice_btn.grid(row=0, column=0, padx=5)

start_btn = tk.Button(button_frame, text="🎤 Start Listening", 
                     font=("Segoe UI", 12, "bold"), bg="#3b82f6", fg="white",
                     padx=20, pady=10, relief="flat", command=start_assistant)
start_btn.grid(row=0, column=1, padx=10)

help_btn = tk.Button(button_frame, text="❓ Help", font=("Segoe UI", 10),
                    bg="#8b5cf6", fg="white", padx=15, pady=5,
                    relief="flat", command=show_help)
help_btn.grid(row=0, column=2, padx=5)

clear_btn = tk.Button(button_frame, text="🗑️ Clear", font=("Segoe UI", 10),
                     bg="#64748b", fg="white", padx=15, pady=5,
                     relief="flat", command=lambda: output.delete(1.0, tk.END))
clear_btn.grid(row=0, column=3, padx=5)

# Footer
footer_frame = tk.Frame(root, bg="#0f172a")
footer_frame.pack(fill=tk.X, pady=(10, 5))

tk.Label(footer_frame, text="💡 Tip: Say 'help' to see all commands", 
         font=("Segoe UI", 9), bg="#0f172a", fg="#94a3b8").pack()

# Initial greeting
root.after(500, lambda: log(f"{ASSISTANT_NAME} initialized. Click 'Start Listening' or say 'Hello {ASSISTANT_NAME}'", "system"))

root.mainloop()