import configparser
import os

def load_theme_settings():
    config = configparser.ConfigParser()
    
    appearance_mode = "light"
    color_theme = "blue"
    
    try:
        if os.path.exists("main.opt"):
            config.read("main.opt")
            if 'THEME' in config:
                appearance_mode = config['THEME'].get('appearance_mode', appearance_mode)
                color_theme = config['THEME'].get('color_theme', color_theme)
        else:
            create_default_config()
    except Exception as e:
        print(f"Error loading theme settings: {e}")
    
    return appearance_mode, color_theme

def create_default_config():
    config = configparser.ConfigParser()
    config['THEME'] = {
        'appearance_mode': 'light',
        'color_theme': 'blue'
    }
    
    with open('main.opt', 'w') as configfile:
        config.write(configfile)

def save_theme_settings(appearance_mode, color_theme):
    config = configparser.ConfigParser()
    config['THEME'] = {
        'appearance_mode': appearance_mode,
        'color_theme': color_theme
    }
    
    with open('main.opt', 'w') as configfile:
        config.write(configfile)