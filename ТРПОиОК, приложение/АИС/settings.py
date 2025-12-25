import configparser
from pathlib import Path



def load_config():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent / 'application.ini')
    return config

config = load_config()
DATABASE_URL = config['database']['url']
