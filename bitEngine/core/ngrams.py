import os
from collections import Counter, defaultdict


class NGrams:
    def __init__(self, max_n=3):
        """
        max_n = highest order of n-grams to compute.
        Default = 3 (unigram, bigram, trigram).
        """
        self.max_n = max_n
        self.ngram_counts = {n: Counter() for n in range(1, max_n + 1)}
        self.total_counts = {n: 0 for n in range(1, max_n + 1)}

    def process(self, file_path="BitEngine/data/sentences/eng_sentences.txt"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                tokens = ["<s>"] + line.split() + ["<s/>"]

                # Generate n-grams up to max_n
                for n in range(1, self.max_n + 1):
                    for i in range(len(tokens) - n + 1):
                        ngram = tuple(tokens[i:i + n])
                        self.ngram_counts[n][ngram] += 1

        # Save totals
        for n in range(1, self.max_n + 1):
            self.total_counts[n] = sum(self.ngram_counts[n].values())

    def count_occurrences(self, phrase: str):
        """
        Count how many times the given phrase appears in the corpus.
        Works for any n <= max_n.
        """
        words = tuple(phrase.split())
        n = len(words)

        if n > self.max_n:
            raise ValueError(f"Only up to {self.max_n}-grams are supported.")

        return self.ngram_counts[n][words]

    def next_possible_words(self, phrase: str):
        """
        Suggest next words using automatic backoff:
        Start from highest n-gram available for context,
        and fallback until we find candidates.
        """
        words = phrase.split()
        candidates = []

        # Start from highest order (max_n)
        for n in range(self.max_n, 0, -1):
            if len(words) >= n - 1:
                context = tuple(words[-(n - 1):]) if n > 1 else ()

                # Collect candidates
                candidates = [
                    (ngram[-1], count)
                    for ngram, count in self.ngram_counts[n].items()
                    if ngram[:-1] == context
                ]

                if candidates:
                    break

        # If still nothing, return most common unigrams
        if not candidates:
            candidates = list(self.ngram_counts[1].items())

        # Sort by frequency
        candidates.sort(key=lambda x: x[1], reverse=True)

        # Compute probabilities
        total = sum(c for _, c in candidates)
        candidates_with_prob = [(word, count, count / total) for word, count in candidates]

        return candidates_with_prob, total


# === DEBUG MODE ===
if __name__ == "__main__":
    model = NGrams(max_n=3)
    try:
        model.process()
        query = input("Enter a word/phrase to analyze: ").strip()

        # Count
        count = model.count_occurrences(query)
        print(f"\n'{query}' appears {count} times in the corpus.")

        # Next word prediction
        next_words, total = model.next_possible_words(query)
        if next_words:
            print(f"\nNext possible words after '{query}' "
                  f"(showing top {len(next_words)} options, total {total} appearances):")
            for word, freq, prob in next_words:
                print(f"  {word:10} ({freq} times, {prob*100:.2f}%)")
        else:
            print("\nNo continuation found in corpus.")

    except FileNotFoundError as e:
        print(f"Error: {e}")



"""
TODO:
1. Spell Casing needs some improvements

2. Since trigrams is the max for now, can you try put 4 grams?, or any num of grams?, support for any type of grams? (OPTIONAL TASK)

3. Create backoff method
"""