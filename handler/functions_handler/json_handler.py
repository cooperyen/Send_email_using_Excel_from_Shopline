

import json


class JASON_HANDLER:

    def __init__(self):
        self.saveJsonFileName = 'setting.json'

    def writeJsonFile(self, data):
        with open(self.saveJsonFileName, 'w') as json_file:
            json.dump(data, json_file)

        json_file.close()

    def loadJasonFile(self):
        with open(self.saveJsonFileName, 'r') as json_file:
            return json.load(json_file)
