import json
import config

# API keys
config_data = {
    "OPENAI_API_KEY": "",
    "SERPAPI_API_KEY": ""
}

# Writing to config.json
with open(r"C:\Users\307164\Desktop\Weather Chat Bot\config.json", "w") as config_file:
    json.dump(config_data, config_file, indent=4)
