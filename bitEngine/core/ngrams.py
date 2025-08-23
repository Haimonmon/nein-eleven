# ngrams.py
import json
import os
import pickle
from collections import Counter, defaultdict
from datetime import datetime


class PatternNGrams:
    def __init__(self, corpus_file="data/training_data/pattern.json", pickle_file="data/pickles/pattern.pkl"):
        self.corpus_file = corpus_file
        self.pickle_file = pickle_file
        self.col_model = defaultdict(Counter)  # (prev_piece, cur_piece) -> Counter(col)
        self.last_piece_seen = None
        self.patterns = []  # stores raw pattern entries

        # Ensure directories exist
        os.makedirs(os.path.dirname(corpus_file), exist_ok=True)
        os.makedirs(os.path.dirname(pickle_file), exist_ok=True)

        # Load dataset
        self._load()

    # --- Load / Save ---
    def _load(self):
        """Load from pickle if available, otherwise from JSON."""
        if os.path.exists(self.pickle_file):
            with open(self.pickle_file, "rb") as f:
                self.patterns = pickle.load(f)
        elif os.path.exists(self.corpus_file):
            with open(self.corpus_file, "r", encoding="utf-8") as f:
                self.patterns = json.load(f)
        else:
            self.patterns = []

        self._build_model(self.patterns)

    def _save(self):
        """Save JSON + Pickle."""
        with open(self.corpus_file, "w", encoding="utf-8") as f:
            json.dump(self.patterns, f, indent=2)

        with open(self.pickle_file, "wb") as f:
            pickle.dump(self.patterns, f)

    def _build_model(self, patterns):
        """Rebuild n-gram model from patterns."""
        self.col_model.clear()
        prev = None
        for entry in patterns:
            cur = entry.get("piece")
            coords = entry.get("landed_coordinates", [])
            if not coords or cur is None:
                prev = cur
                continue

            xs = [x for x, _ in coords]
            col = min(xs)

            if prev is not None:
                self.col_model[(prev, cur)][col] += 1
            prev = cur
        self.last_piece_seen = prev

    # --- Write Pattern ---
    def write_pattern(self, piece, landed_coords, rotation=0, lines_cleared=0,
                      next_queue=None, reason="manual"):
        """Write new pattern if not duplicate."""
        if next_queue is None:
            next_queue = []

        # Prevent duplicates
        for p in self.patterns:
            if p["piece"] == piece and p["landed_coordinates"] == landed_coords and p["rotation"] == rotation:
                return False

        entry = {
            "piece": piece,
            "landed_coordinates": landed_coords,
            "rotation": rotation,
            "lines_cleared": lines_cleared,
            "next_pieces_queue": next_queue,
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }
        self.patterns.append(entry)
        self._save()
        self._build_model(self.patterns)
        return True

    # --- Board Formatter (for saving states) ---
    def format_board(self, board):
        return ["".join(str(cell) for cell in row) for row in board]

    # --- Piece templates ---
    SHAPES = {
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
        "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
        "J": [(1, 0), (1, 1), (1, 2), (0, 2)],
        "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
        "Z": [(0, 0), (1, 0), (1, 1), (2, 1)]
    }

    # --- Prediction ---
    def predict(self, board, current_piece, columns, rows, prev_piece=None, next_queue=None):
        """Suggest placement for current_piece."""
        if current_piece not in self.SHAPES:
            return None

        # 1. Try all rotations to clear line
        for rotation in range(4):
            shape = self._rotate_shape(self.SHAPES[current_piece], rotation)
            for col in range(columns):
                base_coords = [(x + col, y) for x, y in shape]
                placement = self._drop(board, base_coords, columns, rows)
                if placement and self._completes_line(board, placement, rows, columns):
                    return {
                        "placement": placement,
                        "rotation": rotation,
                        "column": col,
                        "reason": "line_clear"
                    }

        # 2. Fallback to n-gram
        key = None
        if prev_piece is not None:
            key = (prev_piece, current_piece)
        elif self.last_piece_seen is not None:
            key = (self.last_piece_seen, current_piece)

        if key and key in self.col_model:
            chosen_col = self.col_model[key].most_common(1)[0][0]
        else:
            chosen_col = 0

        shape = self.SHAPES[current_piece]
        base_coords = [(x + chosen_col, y) for x, y in shape]
        placement = self._drop(board, base_coords, columns, rows)

        self.last_piece_seen = current_piece
        return {
            "placement": placement,
            "rotation": 0,
            "column": chosen_col,
            "reason": "ngram_fallback"
        }

    # --- Drop Simulation ---
    def _drop(self, board, base_coords, columns, rows):
        max_x = max(x for x, _ in base_coords)
        if max_x >= columns:
            shift = columns - 1 - max_x
            base_coords = [(x + shift, y) for x, y in base_coords]

        y_offset = 0
        while True:
            next_coords = [(x, y + y_offset + 1) for x, y in base_coords]
            if any(y >= rows or (y >= 0 and board[y][x] != 0) for x, y in next_coords):
                return [(x, y + y_offset) for x, y in base_coords]
            y_offset += 1

    # --- Helpers ---
    def _rotate_shape(self, coords, times=0):
        rotated = coords
        for _ in range(times):
            rotated = [(-y, x) for (x, y) in rotated]
            min_x = min(x for x, _ in rotated)
            min_y = min(y for _, y in rotated)
            rotated = [(x - min_x, y - min_y) for x, y in rotated]
        return rotated

    def _completes_line(self, board, placement, rows, cols):
        sim = [row[:] for row in board]
        for x, y in placement:
            if 0 <= x < cols and 0 <= y < rows:
                sim[y][x] = 1
        return any(all(sim[y][x] != 0 for x in range(cols)) for y in range(rows))

    # --- Debug Testing API ---
    def simulate(self, board, piece, columns, rows):
        """Test hint suggestion with custom board state."""
        return self.predict(board, piece, columns, rows)


"""
    TODO:
    1. the functions like write_pattern(), format_board() should be in this class, for readability

    2. fix format of the landed_coordinates on pattern.json

    3. apply pickle, this is very helpful for large datasets like our pattern base

    4. possible pattern can be overwritten, make a conditional where if a pattern already existed, it will stop to save on pattern.json

    5. Single player hint or suggestion

    6. For file usage you can use utils, if its not enough, create a class for it, commonly in utils are file handlings

    7. pattern json files should be save on data\training_data, pickle files should be save on data\pickles

    8. DATA FIELD ADDITION: on the chosen_position, the second value should store, default if no rotation happen, if so, store the designated rotation, "clock_wise" or
       "counter_clock_wise", this can be seen on core_controller.py

    9. DATA FIELD ADDITION: lines_clear, this will store how many lines it cleared on that pattern

    10. DATA FIELD ADDITION: next_pieces_queue , the pattern should know the pieces in queue, this can be seen on
        core_next_piece_view.py

    11. For debug or testing purposes, make a function that can recieve a board_state (Can be pass with your own board state),
        then insert_piece params will recieve a piece name or shape, example: "T", "L",
        then ai will decide to where to put the insert_piece bace on the given board_state

    12. DATA FIELD ADDITION: steps, basically just a timestamp for your moves.

    
    NOTE:
    1. hint or suggestion should prioritize first
"""