import os
import json

import csv
from pathlib import Path
from rich.progress import Progress
from typing import List, Any, Dict

class BitFileManager:
    """ Manages Bit Engine's files """
    def __init__(self, size_limit: int = 5_000) -> None:
        self.__engine_directory = Path.cwd() / "bitEngine"
        self.__size_limit = size_limit


    def load_file(self, file_name: str) -> List | Dict | Any:
        """ Loads data on the specified json file name. """
        with open(fr"{self.__engine_directory}{file_name}", "r", encoding="utf-8") as file:
            return json.load(file)


    def load_txt_file(self, file_name: str) -> List[str]:
        """ Loads data on the specified txt file name. """
        with open(fr"{self.__engine_directory}{file_name}", "r", encoding="utf-8") as f:
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
    

    def extract_source_file(self, file_source: str, file_transfer: str = None) -> bool:
        """ Extracting tab seperated values sentences data within specified path """
        directory: str = self.__engine_directory/ 'data' / 'sentences'
        file_source = directory / file_source
        file_transfer = directory / file_transfer

        num_data_extracted: int = 0

        file_source_length: int = self._get_file_length(file_source)
        target_indices: List[str] = self._get_spread_indices(file_source_length)

        with file_source.open("r", encoding="utf-8") as source, file_transfer.open("w", encoding="utf-8") as transfer, Progress() as progress:
            reader = csv.reader(source, delimiter = "\t")

            task = progress.add_task(f"Starting Extracting sentences ...", total = self.__size_limit, bar_style = "red")

            for i, row in enumerate(reader):
                if i not in target_indices:
                    continue

                if len(row) >= 3:
                    transfer.write(row[2] + "\n")
                    num_data_extracted += 1

                    if num_data_extracted < self.__size_limit // 2:
                        progress.update(task, advance=1, bar_style="yellow", description = f"[yellow][{num_data_extracted}] Extracting sentences")
                    elif num_data_extracted > self.__size_limit // 2:
                        progress.update(task, advance=1, bar_style="green", description = f"[green][{num_data_extracted}] Extracting sentences")
                   
                if num_data_extracted >= self.__size_limit:
                    break
        
        return True


    def _get_spread_indices(self, total_lines: int) -> List[int]:
        """ To get the equal size_limit even iterating through the whole file_source_length size """
        step: int = (total_lines - 1) / (self.__size_limit - 1) if self.__size_limit > 1 else 0
        return [round(i * step) for i in range(self.__size_limit)]
    

    def _get_file_length(self, file_name: str) -> int:
        """ specific data length size inside of the file """
        directory: str = self.__engine_directory / 'data' / 'sentences'
        file_name = directory / file_name

        with file_name.open("r", encoding="utf-8") as file:
            return sum(1 for _ in file)


if __name__ == "__main__":
    file = BitFileManager(size_limit = 1_000)
    extracted_data = file.extract_source_file(
        file_source = "eng_sentences.tsv",
        file_transfer = "eng_sentences.txt"
    )

    """
    * For different english sentences
    # * Source: https://tatoeba.org/en/downloads

    """