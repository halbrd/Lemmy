import json
import os

class NoConfigRootDirectoryException(Exception):
    def __repr__(self):
        return "No root config directory"

class NoConfigDirectoryException(Exception):
    def __init__(self, server):
        self.server = server

    def __repr__(self):
        return "No config directory for " + server

class NoConfigFileException(Exception):
    def __init__(self, server, topic):
        self.server, self.topic = server, topic

    def __repr__(self):
        return "No config file for " + server + "/" + topic

class NoConfigAttributeException(Exception):
    def __init__(self, server, topic, attribute):
        self.server, self.topic, self.attribute = server, topic, attribute

    def __repr__(self):
        return "No config attribute for " + server + "/" + topic + "/" + attribute

def _makePath(*directories):
    formattedDirectories = [directory.strip("/\\") for directory in directories]
    return os.path.join(*formattedDirectories if len(formattedDirectories) > 0 else "")

def _checkFile(*steps):
    return os.path.isfile(_makePath(steps))

def _checkDirectory(*steps):
    return os.path.isdir(_makePath(steps))

class ConfigAccessor:
    configRoot = "data/config/"

    """def _checkExistence(server, topic, *attributes):
        if not os.path.isdir(self.configRoot):
            raise NoConfigRootDirectoryException()

        if server:
            if not os.path.isdir(makePath(self.configRoot, server)):
                raise NoConfigDirectoryException()

            if topic:
                if not os.path.isfile(self.configRoot + server + )



    def _getConfig(self, server, topic):

    def _getConfigAttributes(self, server, topic, *attributes):


    def _getGlobalConfig(self, topic):


    def _getGlobalConfigAttributes(self, topic, *attributes):
"""
