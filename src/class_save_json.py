import json
import os
from abc import ABC, abstractmethod

class JSONSaver(ABC):

    @abstractmethod
    def __init__(self, path):
        pass

    @abstractmethod
    def save_file(self, data):
        pass

    @abstractmethod
    def open_and_find_info(self, info):
        pass

    @abstractmethod
    def check_file(self):
        pass

class JSONSaver_Areas(JSONSaver):
    """
    This class for saving information about areas in JSON-file.
    """
    def __init__(self, path):
        self.path = path

    def save_file(self, data: dict):
        """
        Saving data in JSON-file
        :param data: dict
        :return: None
        """
        with open(self.path, "w", encoding='utf-8') as file:
            json.dump(data, file)


    def open_and_find_info(self, info: str):
        """
        Open file and find information in this file
        :param info: information which need ti find
        :return: information or False
        """
        with open(self.path, "r", encoding='utf-8') as file:
            data = json.load(file)
            if info in data:
                result = data[info]
            else:
                result = False
        return result

    def check_file(self):
        """
        Checking for file availability.
        :return: Thue or False
        """
        return os.path.isfile(self.path)
