import os

class NGrams:
    def __init__(self, n=2):
        self.n = n

    def process(self, file_path="bitEngine/data/sentences/eng_sentences.txt"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")

        bigrams = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                tokens = ["<s>"] + line.split() + ["<s/>"]
                for i in range(len(tokens) - self.n + 1):
                    ngram = tuple(tokens[i:i+self.n])
                    bigrams.append(ngram)

        return bigrams


# === DEBUG MODE ===
if __name__ == "__main__":
    model = NGrams(n=2)

    try:
        bigrams = model.process()

        print("=== BIGRAMS FROM sentences.txt ===")
        for b in bigrams:
            print(b)

    except FileNotFoundError as e:
        print(f"Error: {e}")


