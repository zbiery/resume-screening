import os
import yaml

ENV = os.getenv("ENV", "dev")  # default to dev

def load_config():
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f)
    return config.get(ENV)

CONFIG = load_config()

# import os
# api_key = os.getenv(CONFIG["openai"]["api_key_env"])

