from dataclasses import dataclass

@dataclass
class WordTimestamp:
    word: str
    start: float
    end: float

    def __str__(self) -> str:
        return f"Word: {self.word}, start: {self.start}, end: {self.end}"

    def __repr__(self) -> str:
        return f"WordTimestamp(word={self.word}, start={self.start}, end={self.end})"

    def get_word_dict(self) -> dict:
        return {"word": self.word, "start": self.start, "end": self.end}
