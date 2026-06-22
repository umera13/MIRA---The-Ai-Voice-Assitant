class Config:
    # App paths
    APP_PATHS = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "chrome": "chrome.exe",
        "settings": "ms-settings:",
        "file explorer": "explorer.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe"
    }
    
    # Email configuration
    EMAIL_CONFIG = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your_email@gmail.com",
        "password": "your_app_password"
    }
    
    # Colors
    COLORS = {
        'primary': '#2E86AB',
        'secondary': '#A23B72',
        'accent': '#F18F01',
        'dark': '#1A1A2E',
        'light': '#FFFFFF',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#F44336'
    }
    
    # Voice visualization
    VOICE_VISUALIZATION_BARS = 20
    
    # Weather API
    WEATHER_API_KEY = "your_openweather_api_key"
    
    # News API
    NEWS_API_KEY = "your_newsapi_key"