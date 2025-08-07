import os
import json

from typing import List, Any, Dict

class BitFileManager:
    """ Manages Bit Engine's files """
    def __init__(self) -> None:
        self.__directory = r"j3mify/lexicon/"


    def load_file(self, file_name: str) -> List | Dict | Any:
        """ Loads data on the specified json file name. """
        with open(fr"{self.__directory}{file_name}", "r", encoding="utf-8") as file:
            return json.load(file)


    def load_txt_file(self, file_name: str) -> List[str]:
        """ Loads data on the specified txt file name. """
        with open(fr"{self.__directory}{file_name}", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]


    def save_file(self, file_name: str, data: Any) -> Any:
        """ Saves data on the specified json file name. """
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)


    def create_file(self, directory: str, file_name: str) -> bool:
        """ Creates a specified file with its file name and designated directrory """
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)

        if os.path.exists(file_path):
            return False

        with open(file_path, "w") as f:
            pass
        return True


    def create_folder(self, directory_name: str) -> bool:
        """ Creates a folder by its given name. """
        if not os.path.exists(directory_name):
            os.makedirs(directory_name, exist_ok=True)
            return True
        return False
    

    def extract_tsv_file(self) -> None:
        pass

if __name__ == "__main__":
    pass

    # * For different english sentences
    # * Source: https://tatoeba.org/en/downloads
