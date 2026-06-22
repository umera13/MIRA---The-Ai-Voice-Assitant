import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import math
from PIL import Image, ImageTk
from config import Config
import pyjokes

# --------------------------------------------------------------------
# Enhanced emoji replacements for all features
# --------------------------------------------------------------------
class SimpleIcons:
    icons = {
        'robot': '🤖',
        'circle': '●',
        'wave-square': '🌊',
        'comments': '💬',
        'microphone-alt': '🎙️',
        'microphone': '🎤',
        'clock': '⏰',
        'cloud-sun': '🌤️',
        'calendar': '📅',
        'laugh': '😂',
        'search': '🔍',
        'calculator': '🧮',
        'info-circle': 'ℹ️',
        'user': '👤',
        'help': '❓',
        'email': '✉️',
        'whatsapp': '📱',
        'game': '🎮',
        'camera': '📷',
        'screenshot': '📸',
        'brightness': '💡',
        'speed': '🚀',
        'alarm': '⏰',
        'password': '🔒',
        'volume': '🔊',
        'keyboard': '⌨️',
        'browser': '🌐',
        'news': '📰',
        'wikipedia': '📚',
        'system': '💻',
        'shutdown': '⭕',
        'restart': '🔄',
        'sleep': '😴',
        'app': '📱',
        'website': '🌍',
        'weather': '🌡️',
        'schedule': '📋',
        'conversation': '💭',
        'close': '❌',
        'open': '📂',
        'folder': '📁',
        'process': '⚙️',
        'info': '📊',
        'close-all': '🚫',
        'type': '⌨️',
        'enter': '↩️'
    }

fa = SimpleIcons()
# --------------------------------------------------------------------


class VoiceAssistantUI:
    def __init__(self, root, assistant):
        self.root = root
        self.assistant = assistant
        self.config = Config()
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.root.title("MIRA The AI Voice Assistant - Complete Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.config.COLORS['dark'])
        
        # Make window semi-transparent
        self.root.attributes('-alpha', 0.97)
        
        # Center the window
        self.center_window()
        
        # Create main container
        self.create_main_container()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_main_container(self):
        """Create the main UI container"""
        self.create_header()
        self.create_visualization_area()
        self.create_conversation_area()
        self.create_controls_area()
        self.create_status_bar()
    
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg=self.config.COLORS['primary'], height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(header_frame, bg=self.config.COLORS['primary'])
        title_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        robot_icon = tk.Label(
            title_frame,
            text=fa.icons['robot'],
            font=('Arial', 24),
            fg=self.config.COLORS['light'],
            bg=self.config.COLORS['primary']
        )
        robot_icon.pack(side=tk.LEFT)
        
        title_label = tk.Label(
            title_frame,
            text="MIRA The AI Voice Assistant",
            font=('Arial', 16, 'bold'),
            fg=self.config.COLORS['light'],
            bg=self.config.COLORS['primary']
        )
        title_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Status indicator
        status_frame = tk.Frame(header_frame, bg=self.config.COLORS['primary'])
        status_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.status_icon = tk.Label(
            status_frame,
            text=fa.icons['circle'],
            font=('Arial', 12),
            fg=self.config.COLORS['success'],
            bg=self.config.COLORS['primary']
        )
        self.status_icon.pack(side=tk.LEFT)
        
        self.status_indicator = tk.Label(
            status_frame,
            text=" Ready",
            font=('Arial', 12, 'bold'),
            fg=self.config.COLORS['light'],
            bg=self.config.COLORS['primary']
        )
        self.status_indicator.pack(side=tk.LEFT)
    
    def create_visualization_area(self):
        """Create voice visualization area"""
        viz_frame = tk.Frame(self.root, bg=self.config.COLORS['dark'], height=120)
        viz_frame.pack(fill=tk.X, padx=10, pady=5)
        viz_frame.pack_propagate(False)
        
        wave_icon = tk.Label(
            viz_frame,
            text=fa.icons['wave-square'],
            font=('Arial', 24),
            fg=self.config.COLORS['primary'],
            bg=self.config.COLORS['dark']
        )
        wave_icon.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.viz_canvas = tk.Canvas(
            viz_frame,
            bg=self.config.COLORS['dark'],
            highlightthickness=0,
            height=80
        )
        self.viz_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.viz_bars = []
        bar_width = 6
        spacing = 2
        
        for i in range(self.config.VOICE_VISUALIZATION_BARS):
            x = i * (bar_width + spacing) + 20
            bar = self.viz_canvas.create_rectangle(
                x, 60, x + bar_width, 80,
                fill=self.config.COLORS['primary'],
                outline=""
            )
            self.viz_bars.append(bar)
    
    def create_conversation_area(self):
        """Create conversation display area"""
        conv_frame = tk.Frame(self.root, bg=self.config.COLORS['dark'])
        conv_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        header_frame = tk.Frame(conv_frame, bg=self.config.COLORS['dark'])
        header_frame.pack(fill=tk.X, padx=15, pady=(5, 0))
        
        comments_icon = tk.Label(
            header_frame,
            text=fa.icons['comments'],
            font=('Arial', 14),
            fg=self.config.COLORS['primary'],
            bg=self.config.COLORS['dark']
        )
        comments_icon.pack(side=tk.LEFT)
        
        header_label = tk.Label(
            header_frame,
            text=" Conversation & Command Results",
            font=('Arial', 12, 'bold'),
            fg=self.config.COLORS['light'],
            bg=self.config.COLORS['dark']
        )
        header_label.pack(side=tk.LEFT)
        
        self.conversation_text = scrolledtext.ScrolledText(
            conv_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg=self.config.COLORS['light'],
            fg=self.config.COLORS['dark'],
            state=tk.DISABLED,
            padx=15,
            pady=15
        )
        self.conversation_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.conversation_text.tag_config('user', foreground=self.config.COLORS['primary'], font=('Arial', 10, 'bold'))
        self.conversation_text.tag_config('assistant', foreground=self.config.COLORS['secondary'], font=('Arial', 10))
        self.conversation_text.tag_config('system', foreground=self.config.COLORS['accent'], font=('Arial', 9, 'italic'))
        self.conversation_text.tag_config('success', foreground='#2E7D32', font=('Arial', 9, 'bold'))
        self.conversation_text.tag_config('error', foreground='#C62828', font=('Arial', 9, 'bold'))
        self.conversation_text.tag_config('info', foreground='#1565C0', font=('Arial', 9, 'italic'))
    
    def create_controls_area(self):
        """Create control buttons area"""
        controls_frame = tk.Frame(self.root, bg=self.config.COLORS['dark'], height=120)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        controls_frame.pack_propagate(False)
        
        # Main controls frame
        main_controls_frame = tk.Frame(controls_frame, bg=self.config.COLORS['dark'])
        main_controls_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Left side - Primary controls
        left_frame = tk.Frame(main_controls_frame, bg=self.config.COLORS['dark'])
        left_frame.pack(side=tk.LEFT)
        
        self.listen_button = tk.Button(
            left_frame,
            text="🎤 Start Listening",
            font=('Arial', 12, 'bold'),
            bg=self.config.COLORS['accent'],
            fg=self.config.COLORS['light'],
            relief='flat',
            padx=25,
            pady=12,
            command=self.toggle_listening
        )
        self.listen_button.pack(side=tk.LEFT, padx=5)
        
        # Help button
        help_button = tk.Button(
            left_frame,
            text=f"{fa.icons['help']} Help & Commands",
            font=('Arial', 11, 'bold'),
            bg=self.config.COLORS['secondary'],
            fg=self.config.COLORS['light'],
            relief='flat',
            padx=20,
            pady=12,
            command=self.show_help_window
        )
        help_button.pack(side=tk.LEFT, padx=10)
        
        # Quick commands grid
        quick_commands_frame = tk.Frame(controls_frame, bg=self.config.COLORS['dark'])
        quick_commands_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Create 2 rows of quick commands
        quick_commands = [
            (fa.icons['clock'], "Time", self.ask_time),
            (fa.icons['weather'], "Weather", self.ask_weather),
            (fa.icons['calendar'], "Date", self.ask_date),
            (fa.icons['news'], "News", self.ask_news),
            (fa.icons['calculator'], "Calculator", self.ask_calculator),
            (fa.icons['search'], "Search", self.ask_search),
            (fa.icons['wikipedia'], "Wikipedia", self.ask_wikipedia),
            (fa.icons['game'], "Game", self.ask_game),
            (fa.icons['camera'], "Camera", self.ask_photo),
            (fa.icons['screenshot'], "Screenshot", self.ask_screenshot),
            (fa.icons['brightness'], "Brightness", self.ask_brightness),
            (fa.icons['speed'], "Speed", self.ask_speed),
            (fa.icons['open'], "Open", self.ask_open_app),
            (fa.icons['close'], "Close", self.ask_close_app),
            (fa.icons['folder'], "Files", self.ask_open_files),
            (fa.icons['volume'], "Volume", self.ask_volume),
            (fa.icons['process'], "Processes", self.ask_processes),
            (fa.icons['info'], "System Info", self.ask_system_info),
            (fa.icons['schedule'], "Schedule", self.ask_schedule),
            (fa.icons['alarm'], "Alarm", self.ask_alarm)
        ]
        
        # Create 2 rows of 10 buttons each
        for row in range(2):
            row_frame = tk.Frame(quick_commands_frame, bg=self.config.COLORS['dark'])
            row_frame.pack(pady=2)
            for col in range(10):
                index = row * 10 + col
                if index < len(quick_commands):
                    icon, text, command = quick_commands[index]
                    btn = tk.Button(
                        row_frame,
                        text=f"{icon} {text}",
                        font=('Arial', 8),
                        bg=self.config.COLORS['primary'],
                        fg=self.config.COLORS['light'],
                        relief='flat',
                        padx=8,
                        pady=4,
                        command=command,
                        width=12
                    )
                    btn.pack(side=tk.LEFT, padx=2)
    
    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.root, bg=self.config.COLORS['primary'])
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        info_icon = tk.Label(
            status_frame,
            text=fa.icons['info-circle'],
            font=('Arial', 10),
            bg=self.config.COLORS['primary'],
            fg=self.config.COLORS['light']
        )
        info_icon.pack(side=tk.LEFT, padx=(10, 5))
        
        self.status_bar = tk.Label(
            status_frame,
            text="Ready! Say 'help' for all commands or click Help button",
            font=('Arial', 9),
            bg=self.config.COLORS['primary'],
            fg=self.config.COLORS['light'],
            relief='sunken',
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, expand=True, padx=(0, 10), pady=2)
    
    def show_help_window(self):
        """Create comprehensive help window with ALL commands"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Voice Assistant - Complete Command Guide")
        help_window.geometry("1000x800")
        help_window.configure(bg=self.config.COLORS['dark'])
        help_window.resizable(True, True)
        
        # Center the help window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (help_window.winfo_screenheight() // 2) - (800 // 2)
        help_window.geometry(f'1000x800+{x}+{y}')
        
        # Create notebook for categorized commands
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Style the notebook
        style = ttk.Style()
        style.configure('TNotebook', background=self.config.COLORS['dark'])
        style.configure('TNotebook.Tab', background=self.config.COLORS['primary'], 
                       foreground=self.config.COLORS['light'], padding=[10, 5])
        
        # Define ALL commands in categories
        categories = {
            "📋 BASIC COMMANDS": [
                ("Hello / Hi", "Basic greeting"),
                ("How are you?", "Check assistant status"),
                ("Thank you", "Polite response"),
                ("Tell me a joke", "Get a random joke"),
                ("Stop listening", "Stop voice recognition"),
                ("Help", "Show this command list"),
                ("Good morning/afternoon/evening", "Time-based greeting")
            ],
            
            "🕐 TIME & DATE": [
                ("What time is it?", "Current time"),
                ("What's the date today?", "Current date"),
                ("Set alarm for 8 AM", "Set an alarm"),
                ("What day is it?", "Day of the week"),
                ("What's my schedule?", "Today's schedule")
            ],
            
            "💻 SYSTEM COMMANDS": [
                ("Shutdown computer", "Shutdown in 10 sec"),
                ("Restart computer", "Restart system"),
                ("Sleep mode", "Put to sleep"),
                ("Take screenshot", "Capture screen"),
                ("Click photo", "Take webcam photo"),
                ("Set brightness to 50%", "Adjust brightness"),
                ("List processes", "Show running processes"),
                ("System information", "Show system details")
            ],
            
            "🖥️ APPLICATION CONTROL - OPEN": [
                ("Open notepad", "Launch Notepad"),
                ("Open calculator", "Launch Calculator"),
                ("Open paint", "Launch Paint"),
                ("Open word", "Launch Microsoft Word"),
                ("Open excel", "Launch Microsoft Excel"),
                ("Open powerpoint", "Launch PowerPoint"),
                ("Open chrome", "Open Chrome browser"),
                ("Open firefox", "Open Firefox browser"),
                ("Open edge", "Open Edge browser"),
                ("Open command", "Open Command Prompt"),
                ("Open task manager", "Open Task Manager"),
                ("Open settings", "System settings"),
                ("Open file explorer", "Open File Explorer"),
                ("Open sticky notes", "Open Sticky Notes")
            ],
            
            "🖥️ APPLICATION CONTROL - CLOSE": [
                ("Close notepad", "Close Notepad"),
                ("Close calculator", "Close Calculator"),
                ("Close paint", "Close Paint"),
                ("Close word", "Close Microsoft Word"),
                ("Close excel", "Close Microsoft Excel"),
                ("Close powerpoint", "Close PowerPoint"),
                ("Close browser", "Close all browsers"),
                ("Close chrome", "Close Chrome"),
                ("Close firefox", "Close Firefox"),
                ("Close edge", "Close Edge"),
                ("Close command", "Close Command Prompt"),
                ("Close task manager", "Close Task Manager"),
                ("Close window", "Close current window"),
                ("Close everything", "Close all applications")
            ],
            
            "🧮 CALCULATOR": [
                ("Calculate 15 plus 27", "Addition"),
                ("Calculate 50 minus 15", "Subtraction"),
                ("Calculate 10 times 5", "Multiplication"),
                ("Calculate 100 divided by 4", "Division")
            ],
            
            "🎮 GAMES & ENTERTAINMENT": [
                ("Play game", "Start rock paper scissors"),
                ("Rock paper scissors", "Play RPS game")
            ],
            
            "📅 CALENDAR & REMINDERS": [
                ("Create event meeting tomorrow", "Add event"),
                ("Show my calendar", "View events")
            ],
            
            "⌨️ KEYBOARD CONTROL": [
                ("Volume up / Volume down", "Adjust volume"),
                ("Mute volume", "Mute sound"),
                ("Press enter", "Simulate key press"),
                ("Type hello", "Type text")
            ],
            
            "📁 FILE OPERATIONS": [
                ("Open documents", "Open Documents folder"),
                ("Open downloads", "Open Downloads folder"),
                ("Open desktop", "Open Desktop folder"),
                ("Open pictures", "Open Pictures folder"),
                ("Open music", "Open Music folder"),
                ("Open videos", "Open Videos folder")
            ],
            
            "🌐 INTERNET COMMANDS": [
                ("Open YouTube", "Launch YouTube"),
                ("Open Google", "Launch Google"),
                ("Search for cats", "Google search"),
                ("Search cats on YouTube", "YouTube search"),
                ("Weather today", "Weather info (requires internet)"),
                ("Check internet speed", "Speed test"),
                ("Give me the news", "News headlines"),
                ("Wikipedia artificial intelligence", "Wikipedia search")
            ],
            
            "🔧 LOCAL FEATURES (NO INTERNET)": [
                ("Tell me a joke", "Local joke database"),
                ("Local weather", "Random weather description"),
                ("Local news", "Random local news"),
                ("What time is it?", "Local time"),
                ("What's the date?", "Local date"),
                ("Open applications", "Local apps - no internet needed"),
                ("Close applications", "Close local apps"),
                ("Take screenshot", "Local screenshot"),
                ("Take photo", "Local webcam photo"),
                ("Set brightness", "Local brightness control"),
                ("Volume control", "Local volume control"),
                ("Calculate", "Local calculator"),
                ("File operations", "Local file/folder access")
            ],
            
            "📧 EMAIL & MESSAGING": [
                ("Send email", "Send email (requires SMTP setup)"),
                ("Send WhatsApp", "Send WhatsApp message")
            ]
        }
        
        # Create tabs for each category
        for category_name, commands in categories.items():
            # Create frame for each tab
            tab_frame = tk.Frame(notebook, bg=self.config.COLORS['light'])
            notebook.add(tab_frame, text=category_name)
            
            # Create scrollable text area
            text_frame = tk.Frame(tab_frame, bg=self.config.COLORS['light'])
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create canvas with scrollbar
            canvas = tk.Canvas(text_frame, bg=self.config.COLORS['light'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.config.COLORS['light'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add commands to the frame
            for i, (command, description) in enumerate(commands):
                cmd_frame = tk.Frame(scrollable_frame, bg=self.config.COLORS['light'])
                cmd_frame.pack(fill=tk.X, padx=5, pady=3)
                
                # Command label
                cmd_label = tk.Label(
                    cmd_frame,
                    text=f"• {command}",
                    font=('Arial', 10, 'bold'),
                    bg=self.config.COLORS['light'],
                    fg=self.config.COLORS['primary'],
                    anchor='w',
                    wraplength=850
                )
                cmd_label.pack(fill=tk.X, pady=(2, 0))
                
                # Description label
                desc_label = tk.Label(
                    cmd_frame,
                    text=f"  → {description}",
                    font=('Arial', 9),
                    bg=self.config.COLORS['light'],
                    fg=self.config.COLORS['dark'],
                    anchor='w',
                    wraplength=850
                )
                desc_label.pack(fill=tk.X, pady=(0, 2))
                
                # Separator
                if i < len(commands) - 1:
                    separator = tk.Frame(cmd_frame, height=1, bg=self.config.COLORS['secondary'])
                    separator.pack(fill=tk.X, pady=3)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        # Quick Reference Frame
        quick_ref_frame = tk.Frame(help_window, bg=self.config.COLORS['dark'])
        quick_ref_frame.pack(fill=tk.X, padx=10, pady=10)
        
        quick_ref_text = """
🚀 QUICK REFERENCE - Voice Commands:

1. BASIC: "hello", "how are you", "thank you", "help"
2. TIME/DATE: "time", "date", "set alarm 8 AM", "schedule"
3. APPS: "open notepad", "close chrome", "close everything"
4. SYSTEM: "screenshot", "camera", "brightness 50", "volume up"
5. CALCULATOR: "calculate 5 plus 3", "10 times 5"
6. FILES: "open documents", "open downloads"
7. INTERNET: "open youtube", "search cats", "weather"
8. GAMES: "play game", "rock paper scissors"
9. SYSTEM INFO: "system information", "list processes"

💡 TIPS:
• Speak clearly: "open notepad" not "can you open notepad please"
• Use simple phrases
• Click buttons for quick access
• Many features work WITHOUT internet!
        """
        
        quick_ref = tk.Label(
            quick_ref_frame,
            text=quick_ref_text,
            font=('Arial', 9, 'italic'),
            bg=self.config.COLORS['dark'],
            fg=self.config.COLORS['light'],
            justify=tk.LEFT
        )
        quick_ref.pack(pady=5)
        
        # Close button
        close_button = tk.Button(
            help_window,
            text="Close Help Window",
            font=('Arial', 11, 'bold'),
            bg=self.config.COLORS['accent'],
            fg=self.config.COLORS['light'],
            command=help_window.destroy,
            padx=20,
            pady=8
        )
        close_button.pack(pady=10)
    
    def setup_animations(self):
        self.is_listening = False
        self.pulse_animation_id = None
        self.viz_animation_id = None
    
    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        self.is_listening = True
        self.listen_button.config(
            text=f"{fa.icons['microphone-alt']} Stop Listening",
            bg=self.config.COLORS['error']
        )
        self.status_icon.config(fg=self.config.COLORS['warning'])
        self.status_indicator.config(text=" Listening")
        self.update_status("Listening... Speak your command now!")
        
        self.start_pulse_animation()
        self.start_voice_visualization()
        self.assistant.start_listening_loop()
    
    def stop_listening(self):
        self.is_listening = False
        self.listen_button.config(
            text="🎤 Start Listening",
            bg=self.config.COLORS['accent']
        )
        self.status_icon.config(fg=self.config.COLORS['success'])
        self.status_indicator.config(text=" Ready")
        self.update_status("Ready - All features available!")
        
        self.stop_animations()
        self.assistant.stop_listening()
    
    def start_pulse_animation(self):
        if self.is_listening:
            self.pulse_animation()
    
    def pulse_animation(self):
        current_bg = self.listen_button.cget('bg')
        new_bg = (self.config.COLORS['warning']
                  if current_bg == self.config.COLORS['error']
                  else self.config.COLORS['error'])
        self.listen_button.config(bg=new_bg)
        self.pulse_animation_id = self.root.after(500, self.pulse_animation)
    
    def start_voice_visualization(self):
        if self.is_listening:
            self.voice_visualization()
    
    def voice_visualization(self):
        for i, bar in enumerate(self.viz_bars):
            height = math.sin(time.time() * 5 + i * 0.3) * 15 + 20
            x1, y1, x2, y2 = self.viz_canvas.coords(bar)
            self.viz_canvas.coords(bar, x1, 80 - height, x2, 80)
            
            color_intensity = int(100 + abs(math.sin(time.time() * 3 + i * 0.2)) * 155)
            color = f'#{color_intensity:02x}{80:02x}{200:02x}'
            self.viz_canvas.itemconfig(bar, fill=color)
        
        self.viz_animation_id = self.root.after(50, self.voice_visualization)
    
    def stop_animations(self):
        if self.pulse_animation_id:
            self.root.after_cancel(self.pulse_animation_id)
        if self.viz_animation_id:
            self.root.after_cancel(self.viz_animation_id)
        
        for bar in self.viz_bars:
            x1, y1, x2, y2 = self.viz_canvas.coords(bar)
            self.viz_canvas.coords(bar, x1, 60, x2, 80)
            self.viz_canvas.itemconfig(bar, fill=self.config.COLORS['primary'])
    
    def update_status(self, message):
        self.status_bar.config(text=message)
    
    def add_message(self, sender, message, message_type='assistant'):
        self.conversation_text.config(state=tk.NORMAL)
        
        if sender:
            if sender == "You":
                icon = fa.icons['user']
                tag = 'user'
            elif sender == "Assistant":
                icon = fa.icons['robot']
                tag = 'assistant'
            elif sender == "System":
                icon = fa.icons['info-circle']
                tag = 'system'
            else:
                icon = ""
                tag = 'system'
            
            self.conversation_text.insert(tk.END, f"{icon} {sender}: ", tag)
        
        self.conversation_text.insert(tk.END, f"{message}\n\n", message_type)
        self.conversation_text.config(state=tk.DISABLED)
        self.conversation_text.see(tk.END)
    
    def ui_callback(self, event_type, data):
        """
        Handle callbacks from the voice assistant.
        IMPORTANT: This should ONLY display messages in the UI.
        The assistant.speak() method in assistant.py handles ALL speaking.
        """
        try:
            if event_type == "assistant_speak":
                # Assistant is speaking this - display in UI
                if data and data.strip():
                    self.add_message("Assistant", data.strip(), 'assistant')
                    
            elif event_type == "user_speech":
                # User said something - display in UI (don't speak)
                if data and data.strip():
                    self.add_message("You", data.strip(), 'user')
                    
            elif event_type == "listening_start":
                # Display listening indicator
                self.add_message("System", "🎤 Listening... Speak now", 'system')
                
            elif event_type == "listening_stop":
                # Display processing indicator
                self.add_message("System", "⚡ Processing...", 'system')
                
            elif event_type == "command_result":
                # This is a result from a command - ONLY display in UI, NEVER speak
                if data and data != "No command detected" and data != "None" and str(data).strip():
                    clean_data = str(data).strip()
                    
                    # Filter out messages that shouldn't be displayed
                    technical_messages = [
                        "opened notepad",
                        "closed notepad", 
                        "screenshot saved",
                        "photo saved",
                        "brightness set",
                        "volume increased",
                        "volume decreased",
                        "volume muted",
                        "enter pressed",
                        "typed:",
                        "weather",
                        "news",
                        "joke",
                        "time",
                        "date",
                        "day",
                        "schedule",
                        "event",
                        "alarm",
                        "speed test",
                        "wikipedia",
                        "youtube",
                        "google",
                        "search",
                        "game",
                        "system info",
                        "processes",
                        "files",
                        "calculation",
                        "result is"
                    ]
                    
                    # Don't display technical status messages
                    should_display = True
                    for tech_msg in technical_messages:
                        if tech_msg in clean_data.lower():
                            should_display = False
                            break
                    
                    if should_display:
                        # Check if it's an error message
                        if any(error_word in clean_data.lower() for error_word in [
                            "error", "failed", "cannot", "unable", "could not", "not found", 
                            "not installed", "no internet", "not recognized", "invalid", "sorry"
                        ]):
                            self.add_message("System", f"⚠️ {clean_data}", 'error')
                        else:
                            self.add_message("System", f"✅ {clean_data}", 'success')
                            
        except Exception as e:
            print(f"[UI ERROR] Callback error: {e}")
    
    # -----------------------------------------------------------------
    # ALL COMMAND METHODS - COMPLETE SET
    # -----------------------------------------------------------------
    
    def ask_time(self):
        self.assistant.get_time()
    
    def ask_weather(self):
        self.assistant.get_local_weather()
    
    def ask_date(self):
        self.assistant.get_date()
    
    def ask_news(self):
        self.assistant.get_local_news()
    
    def ask_joke(self):
        self.assistant.tell_local_joke()
    
    def ask_search(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Web Search")
        search_window.geometry("350x120")
        search_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(search_window, text="Enter search query:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        search_entry = tk.Entry(search_window, width=40, font=('Arial', 10))
        search_entry.pack(pady=5)
        
        def perform_search():
            query = search_entry.get()
            if query:
                self.assistant.handle_internet_commands(f"search {query}")
                search_window.destroy()
        
        tk.Button(search_window, text="🔍 Search Google", command=perform_search,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 10)).pack(pady=5)
        
        search_entry.focus()
        search_entry.bind('<Return>', lambda e: perform_search())
    
    def ask_calculator(self):
        calc_window = tk.Toplevel(self.root)
        calc_window.title("Calculator")
        calc_window.geometry("300x180")
        calc_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(calc_window, text="Enter calculation:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        calc_entry = tk.Entry(calc_window, width=30, font=('Arial', 12))
        calc_entry.pack(pady=5)
        
        # Example buttons
        examples_frame = tk.Frame(calc_window, bg=self.config.COLORS['dark'])
        examples_frame.pack(pady=5)
        
        examples = ["15 + 27", "50 - 15", "10 * 5", "100 / 4"]
        for example in examples:
            btn = tk.Button(examples_frame, text=example, font=('Arial', 8),
                           command=lambda e=example: calc_entry.insert(tk.END, e),
                           bg=self.config.COLORS['secondary'], fg=self.config.COLORS['light'])
            btn.pack(side=tk.LEFT, padx=2)
        
        def perform_calc():
            expression = calc_entry.get()
            if expression:
                self.assistant.calculate(expression)
                calc_window.destroy()
        
        tk.Button(calc_window, text="🧮 Calculate", command=perform_calc,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 10)).pack(pady=10)
        
        calc_entry.focus()
        calc_entry.bind('<Return>', lambda e: perform_calc())
    
    def ask_wikipedia(self):
        wiki_window = tk.Toplevel(self.root)
        wiki_window.title("Wikipedia Search")
        wiki_window.geometry("350x120")
        wiki_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(wiki_window, text="Search Wikipedia for:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        wiki_entry = tk.Entry(wiki_window, width=40, font=('Arial', 10))
        wiki_entry.pack(pady=5)
        
        def perform_wiki_search():
            query = wiki_entry.get()
            if query:
                self.assistant.handle_internet_commands(f"wikipedia {query}")
                wiki_window.destroy()
        
        tk.Button(wiki_window, text="📚 Search Wikipedia", command=perform_wiki_search,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 10)).pack(pady=5)
        
        wiki_entry.focus()
        wiki_entry.bind('<Return>', lambda e: perform_wiki_search())
    
    def ask_game(self):
        game_window = tk.Toplevel(self.root)
        game_window.title("Rock Paper Scissors")
        game_window.geometry("300x200")
        game_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(game_window, text="Choose your move:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light'],
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        def play_choice(choice):
            self.assistant.play_game(f"game {choice}")
            game_window.destroy()
        
        moves_frame = tk.Frame(game_window, bg=self.config.COLORS['dark'])
        moves_frame.pack(pady=10)
        
        tk.Button(moves_frame, text="🪨 Rock", font=('Arial', 11),
                 bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                 padx=15, pady=8, command=lambda: play_choice("rock")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(moves_frame, text="📄 Paper", font=('Arial', 11),
                 bg=self.config.COLORS['secondary'], fg=self.config.COLORS['light'],
                 padx=15, pady=8, command=lambda: play_choice("paper")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(moves_frame, text="✂️ Scissors", font=('Arial', 11),
                 bg=self.config.COLORS['accent'], fg=self.config.COLORS['light'],
                 padx=15, pady=8, command=lambda: play_choice("scissors")).pack(side=tk.LEFT, padx=5)
    
    def ask_screenshot(self):
        self.assistant.take_screenshot()
    
    def ask_photo(self):
        self.assistant.take_photo()
    
    def ask_speed(self):
        self.assistant.check_internet_speed()
    
    def ask_brightness(self):
        brightness_window = tk.Toplevel(self.root)
        brightness_window.title("Screen Brightness")
        brightness_window.geometry("300x150")
        brightness_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(brightness_window, text="Set brightness level (0-100%):", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        brightness_var = tk.IntVar(value=50)
        scale = tk.Scale(brightness_window, from_=0, to=100, orient=tk.HORIZONTAL,
                        variable=brightness_var, bg=self.config.COLORS['dark'],
                        fg=self.config.COLORS['light'], highlightbackground=self.config.COLORS['dark'])
        scale.pack(pady=10, fill=tk.X, padx=20)
        
        def set_brightness():
            level = brightness_var.get()
            self.assistant.adjust_brightness(f"brightness {level}")
            brightness_window.destroy()
        
        tk.Button(brightness_window, text="💡 Set Brightness", command=set_brightness,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 10)).pack(pady=10)
    
    def ask_alarm(self):
        alarm_window = tk.Toplevel(self.root)
        alarm_window.title("Set Alarm")
        alarm_window.geometry("300x150")
        alarm_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(alarm_window, text="Set alarm for (e.g., 8:30 AM):", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        alarm_entry = tk.Entry(alarm_window, width=20, font=('Arial', 12))
        alarm_entry.pack(pady=10)
        alarm_entry.insert(0, "8:00 AM")
        
        def set_alarm():
            time_str = alarm_entry.get()
            if time_str:
                self.assistant.set_alarm(f"set alarm for {time_str}")
                alarm_window.destroy()
        
        tk.Button(alarm_window, text="⏰ Set Alarm", command=set_alarm,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 10)).pack(pady=10)
        
        alarm_entry.focus()
        alarm_entry.bind('<Return>', lambda e: set_alarm())
    
    def ask_schedule(self):
        self.assistant.get_schedule()
    
    def ask_open_app(self):
        app_window = tk.Toplevel(self.root)
        app_window.title("Open Application")
        app_window.geometry("350x200")
        app_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(app_window, text="Enter application name:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        app_entry = tk.Entry(app_window, width=30, font=('Arial', 10))
        app_entry.pack(pady=5)
        
        tk.Label(app_window, text="Examples:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        examples_frame = tk.Frame(app_window, bg=self.config.COLORS['dark'])
        examples_frame.pack(pady=5)
        
        examples = ["notepad", "calculator", "paint", "chrome", "explorer"]
        for example in examples:
            btn = tk.Button(examples_frame, text=example, font=('Arial', 8),
                           command=lambda e=example: app_entry.insert(tk.END, e),
                           bg=self.config.COLORS['secondary'], fg=self.config.COLORS['light'])
            btn.pack(side=tk.LEFT, padx=2)
        
        def open_app():
            app = app_entry.get()
            if app:
                self.assistant.open_application(f"open {app}")
                app_window.destroy()
        
        tk.Button(app_window, text="📂 Open Application", command=open_app,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 10)).pack(pady=10)
        
        app_entry.focus()
        app_entry.bind('<Return>', lambda e: open_app())
    
    def ask_close_app(self):
        close_window = tk.Toplevel(self.root)
        close_window.title("Close Application")
        close_window.geometry("350x200")
        close_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(close_window, text="Enter application to close:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        app_entry = tk.Entry(close_window, width=30, font=('Arial', 10))
        app_entry.pack(pady=5)
        
        tk.Label(close_window, text="Quick close:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        
        quick_frame = tk.Frame(close_window, bg=self.config.COLORS['dark'])
        quick_frame.pack(pady=5)
        
        quick_buttons = [
            ("Close Everything", "close everything"),
            ("Close Window", "close window"),
            ("Close Browser", "close browser"),
            ("Close Notepad", "close notepad")
        ]
        
        for text, command in quick_buttons:
            btn = tk.Button(quick_frame, text=text, font=('Arial', 8),
                           command=lambda c=command: (self.assistant.close_application(c), close_window.destroy()),
                           bg=self.config.COLORS['secondary'], fg=self.config.COLORS['light'])
            btn.pack(side=tk.LEFT, padx=2)
        
        def close_app():
            app = app_entry.get()
            if app:
                self.assistant.close_application(f"close {app}")
                close_window.destroy()
        
        tk.Button(close_window, text="❌ Close Application", command=close_app,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 10)).pack(pady=10)
        
        app_entry.focus()
        app_entry.bind('<Return>', lambda e: close_app())
    
    def ask_open_files(self):
        file_window = tk.Toplevel(self.root)
        file_window.title("Open Files/Folders")
        file_window.geometry("350x200")
        file_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(file_window, text="Select folder to open:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=10)
        
        folders_frame = tk.Frame(file_window, bg=self.config.COLORS['dark'])
        folders_frame.pack(pady=10)
        
        folders = [
            ("📁 Documents", "documents"),
            ("📥 Downloads", "downloads"),
            ("🖥️ Desktop", "desktop"),
            ("🖼️ Pictures", "pictures"),
            ("🎵 Music", "music"),
            ("🎬 Videos", "videos")
        ]
        
        for i in range(0, len(folders), 2):
            row_frame = tk.Frame(folders_frame, bg=self.config.COLORS['dark'])
            row_frame.pack(pady=5)
            for j in range(2):
                if i + j < len(folders):
                    icon, folder = folders[i + j]
                    btn = tk.Button(row_frame, text=icon, font=('Arial', 10),
                                   command=lambda f=folder: (self.assistant.open_file(f"open {f}"), file_window.destroy()),
                                   bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                                   padx=15, pady=8)
                    btn.pack(side=tk.LEFT, padx=5)
    
    def ask_volume(self):
        volume_window = tk.Toplevel(self.root)
        volume_window.title("Volume Control")
        volume_window.geometry("300x150")
        volume_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(volume_window, text="Volume Control:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=10)
        
        buttons_frame = tk.Frame(volume_window, bg=self.config.COLORS['dark'])
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="🔊 Volume Up", font=('Arial', 10),
                 command=lambda: self.assistant.keyboard_control("volume up"),
                 bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                 padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🔉 Volume Down", font=('Arial', 10),
                 command=lambda: self.assistant.keyboard_control("volume down"),
                 bg=self.config.COLORS['secondary'], fg=self.config.COLORS['light'],
                 padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🔇 Mute", font=('Arial', 10),
                 command=lambda: self.assistant.keyboard_control("mute"),
                 bg=self.config.COLORS['accent'], fg=self.config.COLORS['light'],
                 padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    def ask_processes(self):
        self.assistant.manage_processes("list processes")
    
    def ask_system_info(self):
        self.assistant.get_system_info()
    
    def create_email_window(self):
        """Create email composition window"""
        email_window = tk.Toplevel(self.root)
        email_window.title("Send Email")
        email_window.geometry("450x350")
        email_window.configure(bg=self.config.COLORS['dark'])
        
        tk.Label(email_window, text="Recipient Email:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        recipient_entry = tk.Entry(email_window, width=40, font=('Arial', 10))
        recipient_entry.pack(pady=5)
        
        tk.Label(email_window, text="Subject:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        subject_entry = tk.Entry(email_window, width=40, font=('Arial', 10))
        subject_entry.pack(pady=5)
        subject_entry.insert(0, "Message From Meera")
        
        tk.Label(email_window, text="Message:", 
                 bg=self.config.COLORS['dark'], fg=self.config.COLORS['light']).pack(pady=5)
        message_text = scrolledtext.ScrolledText(email_window, width=50, height=8, font=('Arial', 10))
        message_text.pack(pady=5)
        
        def send_email():
            recipient = recipient_entry.get()
            subject = subject_entry.get()
            message = message_text.get("1.0", tk.END).strip()
            if recipient and message:
                self.assistant.send_email(f"send email to {recipient} subject {subject} message {message}")
                email_window.destroy()
        
        tk.Button(email_window, text="✉️ Send Email", command=send_email,
                  bg=self.config.COLORS['primary'], fg=self.config.COLORS['light'],
                  font=('Arial', 11)).pack(pady=10)
    
    def run(self):
        self.add_message("System", "🚀 MIRA The AI Voice Assistant Started!", 'system')
        self.add_message("System", "💡 Click 'Help & Commands' to see all available features", 'system')
        self.add_message("System", "🎤 Click 'Start Listening' or use the quick buttons", 'system')
        
        # Set UI callback for the assistant
        self.assistant.ui_callback = self.ui_callback
        
        # Greet the user (will be spoken by assistant)
        self.assistant.greet()