import os
import random
from collections import Counter

class NGrams:
    def __init__(self):
        self.unigram_counts = Counter()
        self.bigram_counts = Counter()
        self.trigram_counts = Counter()
        self.total_unigrams = 0

    def process(self, file_path="bitEngine/data/sentences/eng_sentences.txt"):
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

    def unigram_prob(self, w):
        return self.unigram_counts[w] / self.total_unigrams

    def bigram_prob(self, w1, w2):
        count_w1 = self.unigram_counts[w1]
        if count_w1 == 0:
            return 0
        return self.bigram_counts[(w1, w2)] / count_w1

    def trigram_prob(self, w1, w2, w3):
        count_w1w2 = self.bigram_counts[(w1, w2)]
        if count_w1w2 == 0:
            return 0
        return self.trigram_counts[(w1, w2, w3)] / count_w1w2

    def interpolated_prob(self, w1, w2, w3, λ3=0.5, λ2=0.3, λ1=0.2):
        p_tri = self.trigram_prob(w1, w2, w3)
        p_bi = self.bigram_prob(w2, w3)
        p_uni = self.unigram_prob(w3)
        p_interp = λ3*p_tri + λ2*p_bi + λ1*p_uni
        return p_interp, p_tri, p_bi, p_uni

    def weighted_choice(self, choices):
        total = sum(w for _, w in choices)
        r = random.uniform(0, total)
        upto = 0
        for word, weight in choices:
            upto += weight
            if upto >= r:
                return word
        return choices[-1][0]

    def generate_sentence(self, start_words, max_length=20):
        words = start_words.split()

        if len(words) == 1:
            w1 = "<s>"
            w2 = words[0]
        else:
            w1, w2 = words[-2], words[-1]

        sentence = words[:]

        for _ in range(max_length):
            # Candidates from trigram context
            candidates = {w3 for (_, _, w3) in self.trigram_counts if _ == w1 and _ == w2}
            if not candidates:
                candidates = {w3 for (_, w3) in self.bigram_counts if _ == w2}
            if not candidates:
                candidates = set(self.unigram_counts.keys())

            # Calculate probabilities with repetition penalty
            details = []
            recent_words = set(sentence[-3:])
            for w3 in candidates:
                p_interp, p_tri, p_bi, p_uni = self.interpolated_prob(w1, w2, w3)
                if w3 in recent_words:
                    p_interp *= 0.3
                if w3 == "<s/>" and len(sentence) > 5:
                    p_interp *= 1.5 
                details.append((w3, p_interp, p_tri, p_bi, p_uni))

            # Keep only top 5 candidates
            details.sort(key=lambda x: x[1], reverse=True)
            top_candidates = details[:5]

            # Weighted random selection
            next_word = self.weighted_choice([(w, p) for w, p, *_ in top_candidates])

            # Debug output
            # print(f"\nContext: ({w1}, {w2})")
            # for w, p_int, p_tri, p_bi, p_uni in top_candidates:
            #     print(f"{w:15} interp={p_int:.4f} trigram={p_tri:.4f} bigram={p_bi:.4f} unigram={p_uni:.4f}")
            # print(f"Selected: {next_word}")

            if next_word == "<s/>":
                break

            sentence.append(next_word)
            w1, w2 = w2, next_word 

        return " ".join(w for w in sentence if w not in ("<s>", "<s/>"))


# === DEBUG MODE ===
if __name__ == "__main__":
    model = NGrams()
    try:
        model.process()
        start = input("Enter start words: ").strip()
        print("\n=== GENERATED SENTENCE ===")
        print(model.generate_sentence(start))
    except FileNotFoundError as e:
        print(f"Error: {e}")
