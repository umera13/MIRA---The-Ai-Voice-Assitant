import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import pyautogui
import requests
import json
import pyjokes
import wikipedia
import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pywhatkit as kit
import threading
import speedtest
import screen_brightness_control as sbc
import subprocess
import calendar
import random
import sys


class VoiceAssistant:
    def __init__(self, ui_callback=None):
        self.ui_callback = ui_callback
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None
        self.is_listening = False
        self.current_command = ""
        self.alarms = []
        self.calendar_events = []
        self.brightness_level = 50
        self.local_jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? It got mugged!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What's orange and sounds like a parrot? A carrot!",
            "Why did the tomato turn red? Because it saw the salad dressing!"
        ]
        self.local_weather_options = [
            "It's a beautiful sunny day with clear skies. Perfect for outdoor activities!",
            "Partly cloudy with a gentle breeze. A pleasant day overall.",
            "Overcast but no rain expected. Good day for indoor activities.",
            "Light showers expected. Don't forget your umbrella!",
            "Cool and crisp weather. Great for a refreshing walk.",
            "Warm and humid today. Stay hydrated if you're going outside.",
            "A bit chilly outside. You might want a light jacket.",
            "Perfect weather - not too hot, not too cold. Goldilocks would approve!"
        ]
        self.local_news_headlines = [
            "Local community celebrates annual festival with great enthusiasm.",
            "City council announces new park development project.",
            "Local sports team wins championship after thrilling final match.",
            "New library opening scheduled for next month in downtown area.",
            "Annual charity drive exceeds fundraising goals for local hospital.",
            "Public transportation system to receive upgrades starting next quarter.",
            "Local farmers market expands with new organic produce vendors.",
            "City announces plans for new bicycle lanes across major routes."
        ]

        # Initialize systems safely
        self.setup_voice()
        self.setup_speech_recognition()

    # -------------------------------
    # VOICE SETUP
    # -------------------------------
    def setup_voice(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty("voices")
            if len(voices) > 1:
                self.tts_engine.setProperty("voice", voices[1].id)  # Female voice
            self.tts_engine.setProperty("rate", 150)
            self.tts_engine.setProperty("volume", 0.9)
            print("Voice system initialized successfully.")
        except Exception as e:
            print(f"[ERROR] TTS Setup Error: {e}")

    # -------------------------------
    # SPEECH SETUP
    # -------------------------------
    def setup_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            print("[INFO] Microphone initialized.")
        except Exception as e:
            print(f"[ERROR] Speech Recognition Setup Error: {e}")
            self.microphone = None

    # -------------------------------
    # CORE FUNCTIONS - ENHANCED SPEAK
    # -------------------------------
    def speak(self, text):
        """Speak text and update UI"""
        if not text:
            return
        
        text = str(text).strip()
        if not text:
            return
        
        # Only filter out specific technical patterns, not general responses
        technical_patterns = [
            "[info]",
            "[error]",
            "[processing]:",
            "user - online",
            "user - offline",
            "result:",
            "screenshot saved:",
            "photo saved:",
            "brightness set to",
            "volume increased",
            "volume decreased",
            "volume muted",
            "enter pressed",
            "typed:",
            "speed test failed",
            "email requires setup",
            "alarm feature coming soon",
            "successfully opened",
            "successfully closed",
            "closed all applications",
            "current window closed",
            "failed to open",
            "failed to close",
            "application not found",
            "no application specified",
            "folder opened successfully",
            "failed to open",
            "no folder specified",
            "schedule retrieval failed",
            "event creation failed",
            "calculation error",
            "invalid expression",
            "keyboard control failed",
            "camera access failed",
            "photo failed",
            "screenshot failed",
            "system info retrieval failed",
            "alarm setting failed",
            "email failed",
            "process list failed",
            "failed to terminate",
            "no process specified",
            "command not recognized",
            "no command detected",
            "internet required",
            "internet command failed:",
            "listening stopped",
            "listening started"
        ]
        
        # Check if text starts with or contains any technical pattern
        text_lower = text.lower()
        for pattern in technical_patterns:
            if pattern in text_lower and len(text) < 100:  # Only filter short technical messages
                print(f"[TECHNICAL - NOT SPOKEN]: {text}")
                return
        
        # Send to UI for display
        if self.ui_callback:
            self.ui_callback("assistant_speak", text)
        
        print(f"🤖 Assistant: {text}")
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"[ERROR] Speech Output Failed: {e}")

    def listen(self):
        """Listen to user's voice"""
        if self.microphone is None:
            self.speak("Microphone not found. Please check your audio input device.")
            return ""

        try:
            with sr.Microphone() as source:
                if self.ui_callback:
                    self.ui_callback("listening_start", None)
                print("[LISTENING...]")
                
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
                if self.ui_callback:
                    self.ui_callback("listening_stop", None)

            # Try offline recognition first
            try:
                command = self.recognizer.recognize_sphinx(audio).lower()
                print(f"🗣️ User (offline): {command}")
                if self.ui_callback:
                    self.ui_callback("user_speech", command)
                return command
            except:
                # Fallback to Google
                command = self.recognizer.recognize_google(audio).lower()
                print(f"🗣️ User (online): {command}")
                if self.ui_callback:
                    self.ui_callback("user_speech", command)
                return command

        except sr.WaitTimeoutError:
            print("[INFO] Listening timeout - no speech detected")
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that. Please speak clearly.")
            return ""
        except sr.RequestError:
            self.speak("Speech recognition service is unavailable. Please check your internet connection.")
            return ""
        except Exception as e:
            print(f"[ERROR] Listening Error: {e}")
            self.speak("There was an error with the microphone. Please try again.")
            return ""

    # -------------------------------
    # HELP COMMAND SYSTEM
    # -------------------------------
    def show_help(self):
        """Display all available commands"""
        help_text = """
🤖 VOICE ASSISTANT COMMAND GUIDE 🤖

📋 LOCAL COMMANDS (NO INTERNET):
• "Hello" / "Hi" - Greeting
• "How are you?" - Check status
• "Thank you" - Polite response
• "Tell me a joke" - Get a random joke
• "Stop listening" - Stop voice recognition
• "Help" - Show this command list

🕐 TIME & DATE:
• "What time is it?" - Current time
• "What's the date today?" - Current date
• "Set alarm for 8 AM" - Set an alarm
• "What day is it?" - Day of the week
• "What's my schedule?" - Today's schedule

💻 SYSTEM COMMANDS:
• "Shutdown computer" - Shutdown in 10 sec
• "Restart computer" - Restart system
• "Sleep mode" - Put to sleep
• "Take screenshot" - Capture screen
• "Click photo" - Take webcam photo
• "Set brightness to 50%" - Adjust brightness

🖥️ APPLICATION CONTROL - OPEN:
• "Open notepad" - Launch Notepad
• "Open calculator" - Launch Calculator
• "Open paint" - Launch Paint
• "Open word" - Launch Microsoft Word
• "Open excel" - Launch Microsoft Excel
• "Open powerpoint" - Launch PowerPoint
• "Open chrome" - Open Chrome browser
• "Open firefox" - Open Firefox browser
• "Open edge" - Open Edge browser
• "Open command" - Open Command Prompt
• "Open task manager" - Open Task Manager
• "Open settings" - System settings
• "Open file explorer" - Open File Explorer
• "Open sticky notes" - Open Sticky Notes

🖥️ APPLICATION CONTROL - CLOSE:
• "Close notepad" - Close Notepad
• "Close calculator" - Close Calculator
• "Close paint" - Close Paint
• "Close word" - Close Microsoft Word
• "Close excel" - Close Microsoft Excel
• "Close powerpoint" - Close PowerPoint
• "Close browser" - Close all browsers
• "Close chrome" - Close Chrome
• "Close firefox" - Close Firefox
• "Close edge" - Close Edge
• "Close command" - Close Command Prompt
• "Close task manager" - Close Task Manager
• "Close window" - Close current window
• "Close everything" - Close all applications

🧮 CALCULATOR:
• "Calculate 15 plus 27" - Addition
• "Calculate 50 minus 15" - Subtraction
• "Calculate 10 times 5" - Multiplication
• "Calculate 100 divided by 4" - Division

🎮 GAMES & ENTERTAINMENT:
• "Play game" - Start rock paper scissors
• "Rock paper scissors" - Play RPS game

📅 CALENDAR & REMINDERS:
• "Create event meeting tomorrow" - Add event
• "Show my calendar" - View events

⌨️ KEYBOARD CONTROL:
• "Volume up" / "Volume down" - Adjust volume
• "Mute volume" - Mute sound
• "Press enter" - Simulate key press
• "Type hello" - Type text

📧 LOCAL EMAIL:
• "Send email" - Send email (requires SMTP setup)

🔗 INTERNET COMMANDS:
• "Open YouTube" / "Open Google"
• "Search for cats" - Google search
• "Weather today" - Weather info
• "Check internet speed" - Speed test
• "Give me the news" - News headlines
• "Wikipedia artificial intelligence" - Wikipedia
        """
        
        self.speak("Here are all the commands you can use. I'll display them on your screen now.")
        self.speak("You can now see all available commands on your screen. I'm ready to help you with any of these tasks!")
        return help_text

    # -------------------------------
    # BASIC GREETINGS
    # -------------------------------
    def greet(self):
        """Greet the user based on the time"""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning! I'm your AI assistant. How can I help you today?"
        elif 12 <= hour < 18:
            greeting = "Good afternoon! I'm ready to assist you with your tasks."
        else:
            greeting = "Good evening! What can I do for you tonight?"
        self.speak(greeting)
        return greeting

    # -------------------------------
    # SYSTEM COMMANDS
    # -------------------------------
    def system_operations(self, command):
        """System operations with detailed voice feedback"""
        if "shutdown" in command:
            self.speak("I will now shut down your computer in 10 seconds. Please save your work immediately.")
            self.speak("Shutdown initiated. Goodbye!")
            os.system("shutdown /s /t 10")
            return "System shutdown initiated"
            
        elif "restart" in command:
            self.speak("I will now restart your system in 10 seconds. Please save all your work before it restarts.")
            self.speak("Restarting system now. I'll be back in a moment!")
            os.system("shutdown /r /t 10")
            return "System restart initiated"
            
        elif "sleep" in command or "hibernate" in command:
            self.speak("Putting your system to sleep mode now. Good night!")
            self.speak("Sleep mode activated. Wake me up when you need me!")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "System sleep initiated"
            
        else:
            self.speak("I didn't recognize that system command. Please say 'shutdown', 'restart', or 'sleep'.")
            return "Unknown system command"

    # -------------------------------
    # LOCAL JOKES
    # -------------------------------
    def tell_local_joke(self):
        """Tell a local joke"""
        joke = random.choice(self.local_jokes)
        self.speak("Here's a joke for you!")
        self.speak(joke)
        return joke

    # -------------------------------
    # APPLICATION LAUNCH & CLOSE
    # -------------------------------
    def open_application(self, command):
        """Open applications with detailed voice feedback"""
        app_mapping = {
            "notepad": ["notepad.exe", "Notepad", "Opening Notepad for you. It should appear on your screen shortly."],
            "calculator": ["calc.exe", "Calculator", "Opening Calculator. Ready for your calculations!"],
            "paint": ["mspaint.exe", "Microsoft Paint", "Launching Microsoft Paint. Get creative!"],
            "word": ["winword.exe", "Microsoft Word", "Opening Microsoft Word. Ready for document editing."],
            "excel": ["excel.exe", "Microsoft Excel", "Opening Microsoft Excel. Spreadsheets await!"],
            "powerpoint": ["powerpnt.exe", "Microsoft PowerPoint", "Launching Microsoft PowerPoint. Time for presentations!"],
            "settings": ["ms-settings:", "Settings", "Opening System Settings for you."],
            "command": ["cmd.exe", "Command Prompt", "Opening Command Prompt. Advanced commands ready!"],
            "task manager": ["taskmgr.exe", "Task Manager", "Opening Task Manager. Managing your processes now."],
            "control panel": ["control.exe", "Control Panel", "Opening Control Panel for system settings."],
            "file explorer": ["explorer.exe", "File Explorer", "Opening File Explorer. Browsing your files now."],
            "sticky notes": ["stikynot.exe", "Sticky Notes", "Opening Sticky Notes for quick reminders."],
            "chrome": ["chrome.exe", "Google Chrome", "Opening Google Chrome for you. Browsing the web now!"],
            "firefox": ["firefox.exe", "Mozilla Firefox", "Opening Mozilla Firefox. Happy browsing!"],
            "edge": ["msedge.exe", "Microsoft Edge", "Opening Microsoft Edge. Ready to explore!"],
            "browser": ["chrome.exe", "Web Browser", "Opening your default web browser."],
            "photos": ["ms-photos:", "Photos app", "Opening Photos app for your pictures."],
            "camera": ["microsoft.windows.camera:", "Camera app", "Opening Camera app. Say cheese!"],
            "calendar": ["outlookcal:", "Calendar", "Opening Calendar app. Managing your schedule."],
            "mail": ["outlookmail:", "Mail app", "Opening Mail app. Checking your emails."],
            "store": ["ms-windows-store:", "Microsoft Store", "Opening Microsoft Store. Browse apps!"],
            "terminal": ["wt.exe", "Windows Terminal", "Opening Windows Terminal."],
            "powershell": ["powershell.exe", "PowerShell", "Opening PowerShell for advanced tasks."],
            "regedit": ["regedit.exe", "Registry Editor", "Opening Registry Editor. Advanced system editing."],
            "services": ["services.msc", "Services", "Opening Services management console."],
            "disk cleanup": ["cleanmgr.exe", "Disk Cleanup", "Opening Disk Cleanup tool."],
            "defragment": ["dfrgui.exe", "Disk Defragmenter", "Opening Disk Defragmenter."],
            "character map": ["charmap.exe", "Character Map", "Opening Character Map for special characters."],
            "magnifier": ["magnify.exe", "Magnifier", "Opening Magnifier for screen zoom."],
            "narrator": ["narrator.exe", "Narrator", "Opening Narrator for screen reading."],
            "on-screen keyboard": ["osk.exe", "On-Screen Keyboard", "Opening On-Screen Keyboard."],
            "sound recorder": ["soundrecorder.exe", "Sound Recorder", "Opening Sound Recorder."],
            "xbox": ["xboxapp.exe", "Xbox app", "Opening Xbox app. Game on!"]
        }
        
        for app_key, app_data in app_mapping.items():
            if app_key in command:
                try:
                    exe_name, display_name, opening_message = app_data
                    self.speak(opening_message)
                    
                    if ":" in exe_name:
                        os.system(f'start {exe_name}')
                    else:
                        subprocess.Popen(exe_name, shell=True)
                    
                    return f"Successfully opened {display_name}"
                    
                except Exception as e:
                    error_msg = f"Sorry, I couldn't open {display_name}. The application may not be installed on your system."
                    self.speak(error_msg)
                    print(f"[ERROR] App Open Failed: {e}")
                    return f"Failed to open {display_name}"
        
        self.speak("I couldn't find that application in my list. Please try saying the name clearly or check my help menu for available applications.")
        return "Application not found"

    def close_application(self, command):
        """Close applications with detailed voice feedback"""
        apps_to_close = {
            "browser": ["chrome.exe", "msedge.exe", "firefox.exe", "iexplore.exe", "opera.exe", "brave.exe", "All web browsers", "Closing all web browsers for you."],
            "chrome": ["chrome.exe", "Google Chrome", "Closing Google Chrome now."],
            "firefox": ["firefox.exe", "Mozilla Firefox", "Closing Mozilla Firefox for you."],
            "edge": ["msedge.exe", "Microsoft Edge", "Closing Microsoft Edge now."],
            "internet explorer": ["iexplore.exe", "Internet Explorer", "Closing Internet Explorer."],
            "opera": ["opera.exe", "Opera Browser", "Closing Opera browser."],
            "brave": ["brave.exe", "Brave Browser", "Closing Brave browser."],
            
            "word": ["winword.exe", "Microsoft Word", "Closing Microsoft Word. Saving your documents first."],
            "excel": ["excel.exe", "Microsoft Excel", "Closing Microsoft Excel. Saving your spreadsheets."],
            "powerpoint": ["powerpnt.exe", "Microsoft PowerPoint", "Closing Microsoft PowerPoint."],
            "outlook": ["outlook.exe", "Microsoft Outlook", "Closing Microsoft Outlook."],
            "access": ["msaccess.exe", "Microsoft Access", "Closing Microsoft Access."],
            "publisher": ["mspub.exe", "Microsoft Publisher", "Closing Microsoft Publisher."],
            
            "notepad": ["notepad.exe", "Notepad", "Closing Notepad for you."],
            "calculator": ["calculator.exe", "calc.exe", "Calculator", "Closing Calculator."],
            "paint": ["mspaint.exe", "Microsoft Paint", "Closing Microsoft Paint."],
            "command": ["cmd.exe", "conhost.exe", "Command Prompt", "Closing Command Prompt."],
            "powershell": ["powershell.exe", "PowerShell", "Closing PowerShell."],
            "terminal": ["WindowsTerminal.exe", "cmd.exe", "Terminal", "Closing Windows Terminal."],
            "task manager": ["taskmgr.exe", "Task Manager", "Closing Task Manager."],
            "control panel": ["control.exe", "Control Panel", "Closing Control Panel."],
            "file explorer": ["explorer.exe", "File Explorer", "Closing File Explorer."],
            "sticky notes": ["stikynot.exe", "Sticky Notes", "Closing Sticky Notes."],
            
            "media player": ["wmplayer.exe", "Windows Media Player", "Closing Windows Media Player."],
            "photos": ["Microsoft.Photos.exe", "Photos app", "Closing Photos app."],
            "camera": ["WindowsCamera.exe", "Camera app", "Closing Camera app."],
            "movie": ["MoviesAndTV.exe", "Movies & TV app", "Closing Movies & TV app."],
            "music": ["GrooveMusic.exe", "Groove Music", "Closing Groove Music."],
            
            "adobe": ["acrobat.exe", "photoshop.exe", "illustrator.exe", "Adobe applications", "Closing Adobe applications."],
            "vscode": ["code.exe", "Visual Studio Code", "Closing Visual Studio Code."],
            "visual studio": ["devenv.exe", "Visual Studio", "Closing Visual Studio."],
            "python": ["python.exe", "pythonw.exe", "Python", "Closing Python applications."],
            "java": ["java.exe", "javaw.exe", "Java", "Closing Java applications."],
            "spotify": ["spotify.exe", "Spotify", "Closing Spotify."],
            "zoom": ["zoom.exe", "Zoom", "Closing Zoom."],
            "teams": ["teams.exe", "Microsoft Teams", "Closing Microsoft Teams."],
            "skype": ["skype.exe", "Skype", "Closing Skype."],
            "discord": ["discord.exe", "Discord", "Closing Discord."],
            "steam": ["steam.exe", "Steam", "Closing Steam."],
            "epic games": ["EpicGamesLauncher.exe", "Epic Games Launcher", "Closing Epic Games Launcher."],
            
            "settings": ["SystemSettings.exe", "Settings app", "Closing Settings app."],
            "registry": ["regedit.exe", "Registry Editor", "Closing Registry Editor."],
            "services": ["services.msc", "Services", "Closing Services console."],
            "event viewer": ["eventvwr.exe", "Event Viewer", "Closing Event Viewer."],
            "device manager": ["devmgmt.msc", "Device Manager", "Closing Device Manager."]
        }
        
        # Check for "close everything" command
        if "close everything" in command or "close all" in command:
            try:
                self.speak("Closing all applications now. This may take a moment...")
                self.speak("Terminating all running processes. Please wait...")
                
                closed_count = 0
                for app_name, data in apps_to_close.items():
                    for process in data[:-2]:  # Exclude display name and closing message
                        try:
                            os.system(f"taskkill /f /im {process} >nul 2>&1")
                            closed_count += 1
                        except:
                            continue
                
                self.speak(f"Successfully closed all applications. I terminated {closed_count} processes.")
                return f"Closed all applications - {closed_count} processes terminated"
                
            except Exception as e:
                self.speak("I couldn't close all applications. Some applications may require manual closing or administrator permissions.")
                return "Failed to close all applications"
        
        # Check for "close window" command
        if ("close window" in command or "close this" in command or 
            "close current" in command or "close it" in command):
            try:
                self.speak("Closing the current active window for you now.")
                pyautogui.hotkey('alt', 'f4')
                time.sleep(0.3)
                self.speak("Current window closed successfully.")
                return "Current window closed"
            except Exception as e:
                self.speak("I couldn't close the current window. Please try manually or check if there's an unsaved document.")
                return "Failed to close window"
        
        # Check for specific applications
        for app_key, data in apps_to_close.items():
            if app_key in command:
                try:
                    display_name = data[-2]
                    closing_message = data[-1]
                    self.speak(closing_message)
                    
                    closed_count = 0
                    for process in data[:-2]:
                        try:
                            os.system(f"taskkill /f /im {process} >nul 2>&1")
                            closed_count += 1
                        except:
                            continue
                    
                    if closed_count > 0:
                        self.speak(f"Successfully closed {display_name}. Terminated {closed_count} related processes.")
                        return f"Closed {display_name} - {closed_count} processes"
                    else:
                        self.speak(f"I couldn't close {display_name}. It may not be running right now.")
                        return f"{display_name} not running"
                        
                except Exception as e:
                    self.speak(f"Sorry, I couldn't close {display_name}. It may be a system application that requires different permissions.")
                    return f"Failed to close {display_name}"
        
        # Generic close command
        if "close" in command:
            self.speak("Please specify what application you want to close. You can say something like 'close chrome' or 'close notepad'.")
            return "No application specified"
        
        return None

    # -------------------------------
    # SCHEDULE & CALENDAR
    # -------------------------------
    def get_schedule(self):
        """Get today's schedule"""
        try:
            day_name = datetime.datetime.now().strftime("%A")
            month = datetime.datetime.now().strftime("%B")
            day = datetime.datetime.now().strftime("%d")
            year = datetime.datetime.now().strftime("%Y")
            
            self.speak(f"Let me check your schedule for today, {day_name}, {month} {day}, {year}.")
            
            if self.calendar_events:
                self.speak(f"You have {len(self.calendar_events)} events scheduled for today.")
                for i, event in enumerate(self.calendar_events[-3:], 1):
                    self.speak(f"Event {i}: {event['name']} at {event['time'].strftime('%I:%M %p')}.")
                self.speak("That's all your scheduled events for today.")
            else:
                self.speak("You have no events scheduled for today. It's a free day! You can relax or add some tasks if you'd like.")
            
            schedule_text = f"Today is {day_name}, {month} {day}, {year}. "
            if self.calendar_events:
                schedule_text += f"You have {len(self.calendar_events)} events scheduled."
            else:
                schedule_text += "No events scheduled."
            return schedule_text
                
        except Exception as e:
            self.speak("I couldn't retrieve your schedule at this moment. Please try again in a moment.")
            return "Schedule retrieval failed"

    # -------------------------------
    # GAME - ROCK PAPER SCISSORS
    # -------------------------------
    def play_game(self, command):
        """Play rock paper scissors"""
        self.speak("Let's play rock paper scissors!")
        
        choices = ["rock", "paper", "scissors"]
        
        # Extract user choice
        user_choice = ""
        if "rock" in command:
            user_choice = "rock"
            self.speak("You chose rock!")
        elif "paper" in command:
            user_choice = "paper"
            self.speak("You chose paper!")
        elif "scissors" in command:
            user_choice = "scissors"
            self.speak("You chose scissors!")
        else:
            self.speak("Please choose rock, paper, or scissors. Say your choice clearly.")
            return "Awaiting user choice"
        
        self.speak("Now it's my turn...")
        time.sleep(1)
        
        computer_choice = random.choice(choices)
        self.speak(f"I choose... {computer_choice}!")
        time.sleep(1)
        
        if user_choice == computer_choice:
            self.speak("It's a tie! We both chose the same. Let's play again if you want!")
            result = "Tie game!"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            self.speak("You win! Congratulations! Well played!")
            result = "You win!"
        else:
            self.speak("I win this round! Better luck next time!")
            result = "Computer wins!"
        
        return f"You: {user_choice}, Computer: {computer_choice} - {result}"

    # -------------------------------
    # SCREENSHOT
    # -------------------------------
    def take_screenshot(self):
        """Take screenshot"""
        try:
            self.speak("Taking a screenshot now. Please hold still for a moment.")
            self.speak("Capturing your screen...")
            
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_path = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
            os.makedirs(screenshot_path, exist_ok=True)
            full_path = os.path.join(screenshot_path, filename)
            screenshot.save(full_path)
            
            self.speak("Screenshot taken successfully!")
            self.speak(f"I've saved it as {filename} in your Pictures folder under Screenshots.")
            return f"Screenshot saved: {filename}"
            
        except Exception as e:
            self.speak("Failed to take screenshot. Please check if you have proper permissions to save files.")
            return "Screenshot failed"

    # -------------------------------
    # WEBCAM PHOTO
    # -------------------------------
    def take_photo(self):
        """Take photo using webcam"""
        try:
            self.speak("Accessing your camera to take a photo now.")
            self.speak("Please look at the camera and smile!")
            
            cap = cv2.VideoCapture(0)
            time.sleep(1)  # Give camera time to adjust
            ret, frame = cap.read()
            
            if ret:
                self.speak("Smile! Taking photo now...")
                photos_path = os.path.join(os.path.expanduser("~"), "Pictures", "Camera Photos")
                os.makedirs(photos_path, exist_ok=True)
                filename = f"photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                full_path = os.path.join(photos_path, filename)
                cv2.imwrite(full_path, frame)
                
                self.speak("Photo taken successfully!")
                self.speak(f"I've saved it as {filename} in your Pictures folder under Camera Photos.")
                self.speak("You look great!")
                result = f"Photo saved: {filename}"
            else:
                self.speak("I couldn't access your camera. Please check if it's connected and permissions are granted.")
                result = "Camera access failed"
            
            cap.release()
            return result
            
        except Exception as e:
            self.speak("Failed to take photo. Please check your camera connection and try again.")
            return "Photo failed"

    # -------------------------------
    # BASIC CONVERSATION
    # -------------------------------
    def handle_conversation(self, command):
        """Handle conversation"""
        responses = {
            "how are you": "I'm doing great! Thanks for asking. I'm always ready to help you. How are you doing today?",
            "your name": "I'm your AI voice assistant, created to make your life easier. You can call me your personal assistant!",
            "who made you": "I was created by developers who wanted to build a helpful assistant that can make your day more productive and enjoyable.",
            "thank you": "You're very welcome! I'm always happy to help you with anything you need.",
            "thanks": "You're welcome! Glad I could help.",
            "good morning": "Good morning! I hope you have a wonderful day ahead. How can I assist you today?",
            "good afternoon": "Good afternoon! Hope you're having a productive day. What can I help you with?",
            "good evening": "Good evening! How can I assist you tonight? Is there something specific you need help with?",
            "good night": "Good night! Sleep well and have sweet dreams. See you tomorrow!",
            "hello": "Hello! It's great to hear from you. What can I do for you today?",
            "hi": "Hi there! I'm here and ready to help you with whatever you need.",
            "hey": "Hey! What can I do for you today?",
            "how old are you": "As an AI assistant, I don't have an age in the traditional sense. I was recently created and I'm learning new things every day!",
            "what can you do": "I can help you with many things! I can open applications, take screenshots, tell jokes, check the time and date, control your computer settings, and much more. Just ask for help to see all my capabilities.",
            "who are you": "I'm your personal AI voice assistant. I'm here to help you with tasks on your computer, answer questions, and make your work easier.",
            "i love you": "That's very kind of you! I'm here to help and support you in any way I can.",
            "you are smart": "Thank you! I'm always learning and trying to be more helpful. Your feedback helps me improve.",
            "you are stupid": "I'm sorry if I made a mistake. I'm still learning and improving. Please let me know how I can better assist you.",
            "sorry": "No problem at all! We all make mistakes. How can I help you now?",
            "bye": "Goodbye! It was nice talking to you. Have a great day!",
            "see you later": "See you later! Don't hesitate to call me if you need anything.",
            "nice to meet you": "Nice to meet you too! I'm looking forward to helping you with your tasks.",
            "what's up": "Not much, just waiting to help you! What can I do for you today?",
            "how's it going": "Everything is going well on my end! How about you? How can I assist you today?"
        }
        
        for key, value in responses.items():
            if key in command:
                self.speak(value)
                return value

        if "joke" in command:
            return self.tell_local_joke()
            
        return None

    # -------------------------------
    # KEYBOARD CONTROL
    # -------------------------------
    def keyboard_control(self, command):
        """Control keyboard functions"""
        try:
            if "volume up" in command:
                self.speak("Increasing volume for you now.")
                for _ in range(5):
                    pyautogui.press('volumeup')
                self.speak("Volume increased successfully.")
                return "Volume increased"
                
            elif "volume down" in command:
                self.speak("Decreasing volume for you now.")
                for _ in range(5):
                    pyautogui.press('volumedown')
                self.speak("Volume decreased successfully.")
                return "Volume decreased"
                
            elif "mute" in command:
                self.speak("Muting the volume now.")
                pyautogui.press('volumemute')
                self.speak("Volume muted successfully.")
                return "Volume muted"
                
            elif "press enter" in command:
                self.speak("Pressing the Enter key for you now.")
                pyautogui.press('enter')
                self.speak("Enter key pressed successfully.")
                return "Enter pressed"
                
            elif "type" in command:
                text = command.replace("type", "").strip()
                if text:
                    self.speak(f"Typing the text for you now: {text}")
                    pyautogui.write(text, interval=0.1)
                    self.speak("Text typed successfully.")
                    return f"Typed: {text}"
                else:
                    self.speak("Please tell me what you want me to type. For example, say 'type Hello World'.")
                    return "No text specified"
                    
        except Exception as e:
            self.speak("Keyboard control failed. Please try again or check your keyboard settings.")
            return "Keyboard control failed"

    # -------------------------------
    # LOCAL WEATHER
    # -------------------------------
    def get_local_weather(self):
        """Get local weather info"""
        self.speak("Checking local weather conditions for you now.")
        weather = random.choice(self.local_weather_options)
        self.speak(weather)
        return weather

    # -------------------------------
    # LOCAL NEWS
    # -------------------------------
    def get_local_news(self):
        """Get local news"""
        self.speak("Getting the latest local news updates for you now.")
        time.sleep(0.5)
        
        num_news = random.randint(3, 5)
        selected_news = random.sample(self.local_news_headlines, num_news)
        
        self.speak(f"Here are {num_news} local news headlines for today:")
        time.sleep(0.5)
        
        for i, news_item in enumerate(selected_news, 1):
            self.speak(f"Headline {i}: {news_item}")
            time.sleep(0.5)
        
        self.speak("That's all for the local news updates today.")
        return "\n".join(selected_news)

    # -------------------------------
    # TIME & DATE
    # -------------------------------
    def get_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {now}")
        return now

    def get_date(self):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {today}")
        return today

    def get_day(self):
        day = datetime.datetime.now().strftime("%A")
        self.speak(f"Today is {day}")
        return day

    # -------------------------------
    # CALENDAR EVENTS
    # -------------------------------
    def create_calendar_event(self, command):
        """Create calendar event"""
        try:
            event_name = "Meeting"
            if "event" in command:
                event_name = command.split("event")[1].strip()
            elif "reminder" in command:
                event_name = command.split("reminder")[1].strip()
            
            if not event_name or event_name == "":
                event_name = "New Event"
            
            self.calendar_events.append({
                "name": event_name,
                "time": datetime.datetime.now(),
                "created": datetime.datetime.now()
            })
            
            self.speak(f"I've created a new event for you.")
            self.speak(f"Event name: {event_name}")
            self.speak(f"You now have {len(self.calendar_events)} events scheduled in your calendar.")
            return f"Event '{event_name}' added"
            
        except Exception as e:
            self.speak("Failed to create calendar event. Please try again with a clear event name, like 'create event team meeting'.")
            return "Event creation failed"

    # -------------------------------
    # BRIGHTNESS CONTROL
    # -------------------------------
    def adjust_brightness(self, command):
        """Adjust screen brightness"""
        try:
            if "brightness" in command:
                if "100" in command or "maximum" in command or "full" in command:
                    level = 100
                    self.speak("Setting screen brightness to maximum level.")
                elif "50" in command or "half" in command:
                    level = 50
                    self.speak("Setting screen brightness to 50 percent.")
                elif "25" in command or "quarter" in command:
                    level = 25
                    self.speak("Setting screen brightness to 25 percent.")
                elif "0" in command or "minimum" in command or "lowest" in command:
                    level = 0
                    self.speak("Setting screen brightness to minimum level.")
                else:
                    import re
                    numbers = re.findall(r'\d+', command)
                    level = int(numbers[0]) if numbers else 50
                    level = min(100, max(0, level))
                    self.speak(f"Setting screen brightness to {level} percent.")
                
                sbc.set_brightness(level)
                self.speak(f"Screen brightness adjusted to {level} percent successfully.")
                return f"Brightness set to {level}%"
                
        except Exception as e:
            self.speak("Failed to adjust brightness. Please try a value between 0 and 100, like 'set brightness to 75 percent'.")
            return "Brightness adjustment failed"

    # -------------------------------
    # CALCULATOR
    # -------------------------------
    def calculate(self, expression):
        """Calculator"""
        try:
            # Clean the expression
            original_expr = expression
            expression = (expression.replace("plus", "+")
                          .replace("minus", "-")
                          .replace("times", "*")
                          .replace("multiplied by", "*")
                          .replace("divided by", "/")
                          .replace("x", "*"))
            
            # Remove non-math words
            math_words = ["calculate", "what is", "how much is", "compute"]
            for word in math_words:
                expression = expression.replace(word, "")
            
            expression = expression.strip()
            
            # Safety check
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                self.speak(f"Calculating {original_expr} for you now.")
                result = eval(expression)
                self.speak(f"The result is {result}")
                return result
            else:
                self.speak("Sorry, I can only do basic math calculations with numbers and basic operators like plus, minus, times, and divided by.")
                return "Invalid expression"
                
        except Exception as e:
            self.speak("Sorry, I couldn't calculate that. Please check your calculation and try again. For example, say 'calculate 15 plus 27'.")
            return "Calculation error"

    # -------------------------------
    # FILE OPERATIONS
    # -------------------------------
    def open_file(self, command):
        """Open files"""
        common_folders = {
            "documents": ["Documents", "Opening your Documents folder for you now. It should appear shortly."],
            "downloads": ["Downloads", "Opening your Downloads folder now. Your downloaded files await."],
            "desktop": ["Desktop", "Opening your Desktop now. Accessing your desktop items."],
            "pictures": ["Pictures", "Opening your Pictures folder for you. Your photos and images are here."],
            "music": ["Music", "Opening your Music folder now. Ready to play some tunes?"],
            "videos": ["Videos", "Opening your Videos folder. Your movie collection awaits."]
        }
        
        for folder_name, folder_data in common_folders.items():
            if folder_name in command:
                try:
                    folder_path = os.path.join(os.path.expanduser("~"), folder_data[0])
                    self.speak(folder_data[1])
                    os.startfile(folder_path)
                    self.speak("Folder opened successfully.")
                    return f"Opened {folder_name}"
                except Exception as e:
                    self.speak(f"Sorry, I couldn't open your {folder_name} folder. Please check if it exists.")
                    return f"Failed to open {folder_name}"
        
        self.speak("Please specify which folder to open. You can say documents, downloads, desktop, pictures, music, or videos.")
        return "No folder specified"

    # -------------------------------
    # PROCESS MANAGEMENT
    # -------------------------------
    def manage_processes(self, command):
        """Manage running processes"""
        if "list processes" in command or "running processes" in command or "show tasks" in command:
            try:
                self.speak("Showing all running processes for you now. Please check your screen for the complete list.")
                result = subprocess.run(['tasklist'], capture_output=True, text=True, shell=True)
                processes = result.stdout.split('\n')[:15]
                process_list = "\n".join(processes)
                self.speak("Process list displayed on screen.")
                return f"Running processes:\n{process_list}"
            except Exception as e:
                self.speak("Could not list running processes. Please try again.")
                return "Process list failed"
        
        elif "kill process" in command or "stop process" in command or "end process" in command:
            if "named" in command:
                process_name = command.split("named")[1].strip()
            else:
                process_name = command.split("process")[1].strip()
            
            if not process_name:
                self.speak("Please specify which process to stop. For example, say 'kill process notepad'.")
                return "No process specified"
            
            if not process_name.endswith(".exe"):
                process_name += ".exe"
            
            try:
                self.speak(f"Attempting to stop {process_name} now.")
                self.speak("Terminating process...")
                os.system(f"taskkill /f /im {process_name} >nul 2>&1")
                self.speak(f"Successfully terminated {process_name}")
                return f"Terminated {process_name}"
            except Exception as e:
                self.speak(f"Could not terminate process {process_name}. It may not be running or may require administrator permissions.")
                return f"Failed to terminate {process_name}"
        
        return None

    # -------------------------------
    # SYSTEM INFORMATION
    # -------------------------------
    def get_system_info(self):
        """Get system information"""
        try:
            import platform
            
            self.speak("Getting system information for you now.")
            self.speak("Please check your screen for detailed system information.")
            
            info = f"""
System Information:
• Operating System: {platform.system()} {platform.release()}
• Processor: {platform.processor()}
• Machine Type: {platform.machine()}
• Architecture: {platform.architecture()[0]}
• Python Version: {platform.python_version()}
            """.strip()
            
            self.speak("System information displayed on screen.")
            return info
            
        except Exception as e:
            self.speak("Could not retrieve system information at this time.")
            return "System info retrieval failed"

    # -------------------------------
    # ALARM FUNCTIONALITY
    # -------------------------------
    def set_alarm(self, command):
        """Set an alarm"""
        try:
            self.speak("Alarm feature is currently under development.")
            self.speak("For now, I can help you create calendar events and reminders instead.")
            return "Alarm feature coming soon"
        except Exception as e:
            self.speak("Sorry, I couldn't set an alarm at this time.")
            return "Alarm setting failed"

    # -------------------------------
    # INTERNET SPEED TEST
    # -------------------------------
    def check_internet_speed(self):
        """Check internet speed"""
        try:
            self.speak("Checking your internet speed now.")
            self.speak("This may take a few moments, please wait...")
            
            st = speedtest.Speedtest()
            st.get_best_server()
            
            self.speak("Testing download speed now...")
            download_speed = st.download() / 1_000_000
            
            self.speak("Testing upload speed now...")
            upload_speed = st.upload() / 1_000_000
            
            self.speak("Speed test completed successfully!")
            self.speak(f"Your download speed is {download_speed:.1f} megabits per second.")
            self.speak(f"Your upload speed is {upload_speed:.1f} megabits per second.")
            
            if download_speed > 50:
                self.speak("You have excellent internet speed!")
            elif download_speed > 20:
                self.speak("Your internet speed is good for most activities.")
            else:
                self.speak("Your internet speed might be slow for some activities.")
                
            return f"Download: {download_speed:.1f} Mbps, Upload: {upload_speed:.1f} Mbps"
        except Exception as e:
            self.speak("Could not check internet speed. Please check your connection and try again.")
            return "Speed test failed"

    # -------------------------------
    # EMAIL FUNCTIONALITY
    # -------------------------------
    def send_email(self, command):
        """Send email"""
        try:
            self.speak("Email functionality requires configuration. Please set up your email credentials first.")
            self.speak("You can configure email settings in the application settings menu.")
            return "Email requires setup"
        except Exception as e:
            self.speak("Email sending failed. Please check your email configuration.")
            return "Email failed"

    # -------------------------------
    # INTERNET COMMANDS HANDLER
    # -------------------------------
    def handle_internet_commands(self, command):
        """Handle commands that require internet"""
        try:
            # Web operations
            if "open youtube" in command:
                self.speak("Opening YouTube for you now.")
                self.speak("Enjoy your videos!")
                webbrowser.open("https://youtube.com")
                return "YouTube opened"
                
            elif "open google" in command:
                self.speak("Opening Google for you now.")
                self.speak("What would you like to search for?")
                webbrowser.open("https://google.com")
                return "Google opened"
                
            elif "search" in command:
                query = command.replace("search", "").replace("for", "").strip()
                if "on youtube" in query:
                    query = query.replace("on youtube", "").strip()
                    self.speak(f"Playing {query} on YouTube for you now.")
                    kit.playonyt(query)
                    return f"Searching YouTube for {query}"
                else:
                    self.speak(f"Searching for {query} on Google now.")
                    self.speak("Here are the results.")
                    webbrowser.open(f"https://google.com/search?q={query}")
                    return f"Google search for {query}"
                    
            # Wikipedia
            elif "wikipedia" in command:
                query = command.replace("wikipedia", "").replace("search", "").strip()
                if query:
                    self.speak(f"Searching Wikipedia for {query} now.")
                    summary = wikipedia.summary(query, sentences=2)
                    self.speak(f"According to Wikipedia: {summary}")
                    return summary
                else:
                    self.speak("Please specify what you want to search on Wikipedia. For example, 'Wikipedia artificial intelligence'.")
                    return "No Wikipedia query specified"
                    
            # Internet speed test
            elif "internet speed" in command or "speed test" in command:
                return self.check_internet_speed()
                
            else:
                self.speak("This command requires internet connection. Please check your connection and try again.")
                return "Internet required"
                
        except Exception as e:
            self.speak("This command requires an internet connection. Please check your connection and try again.")
            return f"Internet command failed: {str(e)}"

    # -------------------------------
    # ENHANCED COMMAND PROCESSOR
    # -------------------------------
    def process_command(self, command):
        """Main command processor with detailed voice feedback"""
        if not command:
            self.speak("I didn't hear anything. Please speak clearly and try again.")
            return "No command detected"

        self.current_command = command
        print(f"[PROCESSING]: {command}")

        try:
            # LOCAL COMMANDS (NO INTERNET REQUIRED)
            
            # Help command
            if any(word in command for word in ["help", "commands", "what can you do", "show options"]):
                return self.show_help()

            # Greetings
            elif any(word in command for word in ["hello", "hi", "hey", "greetings"]):
                return self.greet()

            # System operations
            elif any(x in command for x in ["shutdown", "restart", "sleep", "hibernate"]):
                return self.system_operations(command)

            # Applications - OPEN
            elif "open" in command and not any(x in command for x in ["youtube", "google", "website"]):
                return self.open_application(command)

            # Applications - CLOSE
            elif "close" in command:
                result = self.close_application(command)
                if result:
                    return result
                self.speak("Please specify what you want to close. For example, 'close chrome' or 'close notepad'.")
                return "No application specified"

            # File operations
            elif any(x in command for x in ["open folder", "open documents", "open downloads", "open desktop"]):
                return self.open_file(command)

            # Local utilities
            elif "screenshot" in command or "screen shot" in command:
                return self.take_screenshot()
                
            elif any(x in command for x in ["photo", "picture", "camera", "take photo"]):
                return self.take_photo()
                
            elif "brightness" in command:
                return self.adjust_brightness(command)
                
            elif "system info" in command or "system information" in command:
                return self.get_system_info()

            # Process management
            elif any(x in command for x in ["process", "task", "kill", "end task"]):
                return self.manage_processes(command)

            # Games
            elif any(x in command for x in ["game", "rock", "paper", "scissors", "play game"]):
                return self.play_game(command)

            # Keyboard control
            elif any(x in command for x in ["volume", "mute", "type", "press", "keyboard"]):
                return self.keyboard_control(command)

            # Alarm functionality
            elif "alarm" in command:
                return self.set_alarm(command)

            # Local information
            elif "weather" in command or "temperature" in command:
                return self.get_local_weather()
                
            elif "news" in command:
                return self.get_local_news()
                
            elif "time" in command:
                return self.get_time()
                
            elif "date" in command:
                return self.get_date()
                
            elif "day" in command:
                return self.get_day()
                
            elif any(x in command for x in ["schedule", "calendar"]):
                if "event" in command or "reminder" in command or "create" in command:
                    return self.create_calendar_event(command)
                else:
                    return self.get_schedule()

            # Calculator
            elif any(x in command for x in ["calculate", "plus", "minus", "times", "divided", "multiplied", "math", "add", "subtract"]):
                return self.calculate(command)

            # Conversation
            elif response := self.handle_conversation(command):
                return response

            # INTERNET-DEPENDENT COMMANDS
            elif any(x in command for x in ["search", "youtube", "google", "wikipedia", "internet speed", "speed test", "browse"]):
                return self.handle_internet_commands(command)

            # Email
            elif "email" in command or "send mail" in command:
                return self.send_email(command)

            # Stop listening
            elif "stop listening" in command or "stop assistant" in command:
                self.speak("Stopping voice recognition now.")
                self.speak("You can start again by saying 'start listening' or clicking the start button.")
                self.stop_listening()
                return "Listening stopped"

            # Start listening
            elif "start listening" in command or "wake up" in command or "hey assistant" in command:
                self.speak("I'm listening now. How can I help you?")
                self.start_listening_loop()
                return "Listening started"

            else:
                self.speak("I'm not sure how to help with that. You can say 'help' to see all the things I can do for you.")
                return "Command not recognized"

        except Exception as e:
            error_msg = f"An error occurred while processing your command: {str(e)}"
            self.speak("Sorry, I encountered an error while processing your request. Please try again.")
            print(f"[ERROR] Command processing failed: {e}")
            return error_msg

    # -------------------------------
    # LISTENING LOOP
    # -------------------------------
    def start_listening_loop(self):
        """Continuous listening"""
        def loop():
            self.is_listening = True
            self.speak("Voice assistant activated. I'm ready to help you!")
            while self.is_listening:
                cmd = self.listen()
                if cmd:
                    result = self.process_command(cmd)
                    if self.ui_callback:
                        self.ui_callback("command_result", result)
                time.sleep(0.5)

        listen_thread = threading.Thread(target=loop, daemon=True)
        listen_thread.start()

    def stop_listening(self):
        """Stop the listening loop"""
        self.is_listening = False
        self.speak("Voice recognition stopped.")


# ==========================================
# SIMPLE TEST INTERFACE
# ==========================================
def test_interface():
    """Simple test interface for the voice assistant"""
    assistant = VoiceAssistant()
    
    print("=" * 50)
    print("VOICE ASSISTANT TEST MODE")
    print("=" * 50)
    print("\nAvailable test commands:")
    print("1. Type 'test notepad' to test opening Notepad")
    print("2. Type 'test close notepad' to test closing Notepad")
    print("3. Type 'test close everything' to close all apps")
    print("4. Type 'test close window' to close current window")
    print("5. Type 'test help' to see all commands")
    print("6. Type 'test listen' to start voice listening")
    print("7. Type 'test stop' to stop voice listening")
    print("8. Type 'test greeting' for a greeting")
    print("9. Type 'test joke' for a joke")
    print("10. Type 'test time' for current time")
    print("11. Type 'test calculator 15+27' for calculation")
    print("12. Type 'test screenshot' to take screenshot")
    print("13. Type 'test photo' to take webcam photo")
    print("14. Type 'test brightness 75' to set brightness")
    print("15. Type 'exit' to quit")
    print("\nYou can also speak directly to the assistant!")
    print("=" * 50)
    
    print("Voice assistant initialized. Test mode activated.")
    assistant.start_listening_loop()
    
    while True:
        user_input = input("\nTest Command: ").lower().strip()
        
        if user_input == 'exit':
            assistant.stop_listening()
            assistant.speak("Goodbye! Have a great day!")
            print("Goodbye!")
            break
        elif user_input == 'test notepad':
            print("Testing Notepad opening...")
            assistant.open_application("open notepad")
        elif user_input == 'test close notepad':
            print("Testing Notepad closing...")
            assistant.close_application("close notepad")
        elif user_input == 'test close everything':
            print("Testing close all applications...")
            assistant.close_application("close everything")
        elif user_input == 'test close window':
            print("Testing close current window...")
            assistant.close_application("close window")
        elif user_input == 'test listen':
            print("Starting listening...")
            assistant.start_listening_loop()
        elif user_input == 'test stop':
            print("Stopping listening...")
            assistant.stop_listening()
        elif user_input == 'test help':
            print(assistant.show_help())
        elif user_input == 'test greeting':
            print("Testing greeting...")
            assistant.greet()
        elif user_input == 'test joke':
            print("Testing joke...")
            assistant.tell_local_joke()
        elif user_input == 'test time':
            print("Testing time...")
            assistant.get_time()
        elif user_input == 'test screenshot':
            print("Testing screenshot...")
            assistant.take_screenshot()
        elif user_input == 'test photo':
            print("Testing webcam photo...")
            assistant.take_photo()
        elif user_input.startswith('test brightness'):
            level = user_input.replace('test brightness', '').strip()
            if level:
                print(f"Testing brightness to {level}...")
                assistant.adjust_brightness(f"brightness {level}")
            else:
                print("Please provide a brightness level. Example: 'test brightness 75'")
        elif user_input.startswith('test calculator'):
            expr = user_input.replace('test calculator', '').strip()
            if expr:
                print(f"Testing calculation: {expr}")
                assistant.calculate(expr)
            else:
                print("Please provide an expression. Example: 'test calculator 15+27'")
        elif user_input.startswith('test '):
            test_cmd = user_input.replace('test ', '')
            print(f"Processing: {test_cmd}")
            result = assistant.process_command(test_cmd)
            print(f"Result: {result}")
        else:
            print("Unknown test command. Type 'test help' for options.")


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.greet()

    while True:
        command = assistant.listen()

        if not command:
            continue

        if "exit" in command or "stop" in command:
            assistant.speak("Goodbye. Shutting down now.")
            break

        response = (
            assistant.handle_conversation(command)
            or assistant.system_operations(command)
            or assistant.open_application(command)
            or assistant.close_application(command)
            or assistant.calculate(command)
            or assistant.get_time()
        )

        if response:
            assistant.speak(response)
