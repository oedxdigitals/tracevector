PLUGIN_TYPE = "phone"
PLUGIN_NAME = "Basic Phone Metadata"

def run(target):
    return {
        "plugin": PLUGIN_NAME,
        "data": {
            "input": target,
            "status": "plugin_loaded_successfully"
        }
    }
