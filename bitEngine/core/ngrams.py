# ngrams.py
import json
from collections import Counter, defaultdict

class PatternNGrams:
    def __init__(self, corpus_file="pattern.json"):
        self.corpus_file = corpus_file
        self.col_model = defaultdict(Counter)  # (prev_piece, cur_piece) -> Counter(col)
        self.last_piece_seen = None
        self._load()

    def _load(self):
        try:
            with open(self.corpus_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

        prev = None
        for entry in data:
            cur = entry.get("piece")
            coords = entry.get("landed_coordinates", [])
            if not coords or cur is None:
                prev = cur
                continue

            # Use the leftmost x of the landed placement as the "column"
            xs = [x for x, _ in coords]
            col = min(xs)

            if prev is not None:
                self.col_model[(prev, cur)][col] += 1

            prev = cur

        self.last_piece_seen = prev

    # --- piece templates (default orientation) ---
    SHAPES = {
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
        "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
        "J": [(1, 0), (1, 1), (1, 2), (0, 2)],
        "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
        "Z": [(0, 0), (1, 0), (1, 1), (2, 1)]
    }

    def _drop(self, board, base_coords, columns, rows):
        """Simulate vertical drop of a piece starting from y=0 until it collides."""
        # clamp if exceeds columns
        max_x = max(x for x, _ in base_coords)
        if max_x >= columns:
            shift = columns - 1 - max_x
            base_coords = [(x + shift, y) for x, y in base_coords]

        y_offset = 0
        while True:
            # test next step
            next_coords = [(x, y + y_offset + 1) for x, y in base_coords]
            # check collision with bottom or filled cells
            blocked = False
            for x, y in next_coords:
                if y >= rows or (y >= 0 and board[y][x] != 0):
                    blocked = True
                    break
            if blocked:
                # settle at current y_offset
                final = [(x, y + y_offset) for x, y in base_coords]
                return final
            y_offset += 1

    def predict(self, board, current_piece, columns, rows, prev_piece=None):
        """
        Suggest placement for current_piece.
        Priority:
        1. If possible, place piece to complete a line.
        2. Otherwise, fall back to n-gram or heuristic.
        """
        if current_piece not in self.SHAPES:
            return None

        # --- 1. Try all rotations + columns to clear a line ---
        for rotation in range(4):  # 0°, 90°, 180°, 270°
            shape = self._rotate_shape(self.SHAPES[current_piece], rotation)
            for col in range(columns):
                base_coords = [(x + col, y) for x, y in shape]
                placement = self._drop(board, base_coords, columns, rows)
                if placement is None:
                    continue
                # Does this placement complete a line?
                if self._completes_line(board, placement, rows, columns):
                    return {
                        "placement": placement,
                        "rotation": rotation,
                        "column": col,
                        "reason": "line_clear"
                    }

        # --- 2. Fallback to n-gram model ---
        key = None
        if prev_piece is not None:
            key = (prev_piece, current_piece)
        elif self.last_piece_seen is not None:
            key = (self.last_piece_seen, current_piece)

        if key and key in self.col_model and len(self.col_model[key]):
            chosen_col = self.col_model[key].most_common(1)[0][0]
        else:
            chosen_col = 0  # fallback heuristic

        # base coords
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

    # --- Helper: rotate shape ---
    def _rotate_shape(self, coords, times=0):
        rotated = coords
        for _ in range(times):
            rotated = [(-y, x) for (x, y) in rotated]  # 90° CCW
            # normalize so no negative offsets
            min_x = min(x for x, _ in rotated)
            min_y = min(y for _, y in rotated)
            rotated = [(x - min_x, y - min_y) for x, y in rotated]
        return rotated

    # --- Helper: check line clear ---
    def _completes_line(self, board, placement, rows, cols):
        sim = [row[:] for row in board]
        for x, y in placement:
            if 0 <= x < cols and 0 <= y < rows:
                sim[y][x] = 1
        for y in range(rows):
            if all(sim[y][x] != 0 for x in range(cols)):
                return True
        return False
