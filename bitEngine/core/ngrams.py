import json
import os
from collections import Counter

class TetrisNGramAI:
    def __init__(self, corpus_file="bitEngine/data/training_data/pattern1.json", n=2):
        """
        n: size of N-gram (2 for bigram, 3 for trigram, etc.)
        """
        self.corpus_file = corpus_file
        self.n = n
        self.ngram_counts = Counter()
        self.history_sequence = []

    def load_corpus(self):
        if not os.path.exists(self.corpus_file):
            print("⚠️ No corpus file found.")
            return

        with open(self.corpus_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON in pattern.json")
                return

        # Extract sequence of current_piece only
        self.history_sequence = [entry["piece"] for entry in data]

        # Build n-grams from sequence
        for i in range(len(self.history_sequence) - self.n + 1):
            ngram = tuple(self.history_sequence[i:i+self.n])
            self.ngram_counts[ngram] += 1

    def predict_next_piece(self, last_pieces):
        """
        last_pieces: list of last (n-1) pieces
        Returns: list of next piece candidates sorted by frequency
        """
        if len(last_pieces) != self.n - 1:
            raise ValueError(f"Provide exactly {self.n - 1} last pieces")

        candidates = Counter()
        for ngram, count in self.ngram_counts.items():
            if ngram[:-1] == tuple(last_pieces):
                candidates[ngram[-1]] = count

        if not candidates:
            return []

        # Sort by frequency descending
        return [piece for piece, _ in candidates.most_common()]

    def show_ngrams(self, top=5):
        print(f"Top {top} {self.n}-grams:")
        for ngram, count in self.ngram_counts.most_common(top):
            print(f"  {ngram} -> {count} times")


if __name__ == "__main__":
    model = TetrisNGramAI(n=2)
    model.load_corpus()
    model.show_ngrams()

    # Example prediction using last piece
    if len(model.history_sequence) >= 1:
        last_piece = model.history_sequence[-1:]
        prediction = model.predict_next_piece(last_piece)
        print(f"\nPrediction after last piece {last_piece}: {prediction}")

    # Example prediction using last two pieces for trigram
    if len(model.history_sequence) >= 2:
        model_trigram = TetrisNGramAI(n=3)
        model_trigram.load_corpus()
        last_two = model_trigram.history_sequence[-2:]
        prediction_tri = model_trigram.predict_next_piece(last_two)
        print(f"\nPrediction after last two pieces {last_two}: {prediction_tri}")
