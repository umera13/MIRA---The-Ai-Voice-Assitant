# main.py
import tkinter as tk
from tkinter import messagebox
import sys
import os
import threading
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant import VoiceAssistant
from ui import VoiceAssistantUI

def main():
    try:
        # Create main window
        root = tk.Tk()
        root.title("MIRA The AI Voice Assistant")
        root.geometry("800x600")
        
        # Initialize assistant FIRST (without UI callback)
        print("MIRA The AI Voice Assistant Initializing voice assistant...")
        assistant = VoiceAssistant()
        
        # Show loading message
        loading_label = tk.Label(root, text="MIRA The AI Voice Assistant Initializing Voice Assistant...", font=("Arial", 14))
        loading_label.pack(pady=50)
        root.deiconify()
        root.update()
        
        # Initialize UI with the assistant
        def init_ui():
            try:
                print("MIRA The AI Voice Assistant Initializing user interface...")
                app_ui = VoiceAssistantUI(root, assistant)
                
                # Connect UI callback to assistant
                assistant.ui_callback = app_ui.ui_callback
                
                # Remove loading label and show main UI
                loading_label.destroy()
                app_ui.run()
                
                # Handle window close
                def on_closing():
                    if messagebox.askokcancel("Quit", "Do you want to quit the Voice Assistant?"):
                        assistant.stop_listening()
                        root.destroy()
                
                root.protocol("WM_DELETE_WINDOW", on_closing)
                
                # Speak welcome message AFTER UI is ready
                time.sleep(1)
                assistant.speak("Voice Assistant is ready. How can I help you today?")
                
            except Exception as e:
                print(f"UI Initialization error: {e}")
                messagebox.showerror("Error", f"Failed to initialize UI: {e}")
                root.quit()
        
        # Start UI initialization
        init_ui()
        
        # Start the GUI loop
        root.mainloop()
        
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()