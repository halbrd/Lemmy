import json

class ConfigAccessor:
    configRoot = "data/config/"

    def getGlobalConfig(self, topic):
        with open(self.configRoot + topic + ".json", "r") as f:
            return json.load(f)
