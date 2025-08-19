import os
from collections import Counter


class NGrams:
    def __init__(self):
        self.unigram_counts = Counter()
        self.bigram_counts = Counter()
        self.trigram_counts = Counter()
        self.total_unigrams = 0

    def process(self, file_path="BitEngine/data/sentences/eng_sentences.txt"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                tokens = ["<s>"] + line.split() + ["<s/>"]

                # Unigrams
                self.unigram_counts.update(tokens)

                # Bigrams
                bigrams = zip(tokens[:-1], tokens[1:])
                self.bigram_counts.update(bigrams)

                # Trigrams
                trigrams = zip(tokens[:-2], tokens[1:-1], tokens[2:])
                self.trigram_counts.update(trigrams)

        self.total_unigrams = sum(self.unigram_counts.values())

    def count_occurrences(self, phrase: str):
        """
        Count how many times the given phrase appears in the corpus.
        Works for unigram, bigram, and trigram.
        """
        words = phrase.split()

        if len(words) == 1:
            return self.unigram_counts[words[0]]

        elif len(words) == 2:
            return self.bigram_counts[tuple(words)]

        elif len(words) == 3:
            return self.trigram_counts[tuple(words)]

        else:
            raise ValueError("Only unigram, bigram, and trigram counts are supported.")

    def next_possible_words(self, phrase: str):
        """
        Suggest ALL possible next words based on the corpus.
        """
        words = phrase.split()

        if len(words) == 1:
            w1 = words[0]
            # Look for bigrams (w1, next)
            candidates = [(w2, c) for (x, w2), c in self.bigram_counts.items() if x == w1]

        elif len(words) == 2:
            w1, w2 = words
            # Look for trigrams (w1, w2, next)
            candidates = [(w3, c) for (x, y, w3), c in self.trigram_counts.items() if x == w1 and y == w2]

        elif len(words) == 3:
            # Use the last two words as context
            w2, w3 = words[-2], words[-1]
            candidates = [(w4, c) for (x, y, w4), c in self.trigram_counts.items() if x == w2 and y == w3]

        else:
            raise ValueError("Only unigram, bigram, and trigram contexts are supported.")

        # Sort candidates by frequency (highest first)
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates


# === DEBUG MODE ===
if __name__ == "__main__":
    model = NGrams()
    try:
        model.process()
        query = input("Enter a word/phrase to analyze: ").strip()

        # Count
        count = model.count_occurrences(query)
        print(f"\n'{query}' appears {count} times in the corpus.")

        # Next word prediction
        next_words = model.next_possible_words(query)
        if next_words:
            total = sum(freq for _, freq in next_words)
            print(f"\nNext possible words after '{query}' ")
            for word, freq in next_words:
                print(f"  {word:10} ({freq} times)")
        else:
            print("\nNo continuation found in corpus.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
