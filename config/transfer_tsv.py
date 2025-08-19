import sys

from pathlib import Path

# * Current solution
sys.path.append(str(Path(__file__).resolve().parent.parent))

import BitEngine as bit

def extract_tsv() -> bool:
    # ! ⚠️ Not Optimized yet.
    file = bit.BitFileManager(size_limit = 10000)
    return file.extract_source_file("./eng_sentences.tsv", "eng_sentences.txt")

if __name__ == "__main__":
      if extract_tsv():
           print("Extraction Done 🎉.")