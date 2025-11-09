import yaml
import os

def load_config():
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, "config.yaml")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)
