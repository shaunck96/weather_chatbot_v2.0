import json
import config

# API keys
config_data = {
    "OPENAI_API_KEY": "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",
    "SERPAPI_API_KEY": "a52405e62b1522253260891971ed21903bebe6ba7879bca152f87a0de5bef4b1"
}

# Writing to config.json
with open(r"C:\Users\307164\Desktop\Weather Chat Bot\config.json", "w") as config_file:
    json.dump(config_data, config_file, indent=4)
