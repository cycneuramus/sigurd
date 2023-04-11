import json
import random
from json.decoder import JSONDecodeError
from pathlib import Path


def ensure_exists(file: str):
    p = Path(file)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch(exist_ok=True)


class Response:
    """
    Gets response from json-encoded <db> while
    preventing repetition by remembering <to_remember>
    amount of previous responses in <recents_file>.

    If not defined, or if set to 0, <to_remember> will
    be equal to len(possible).
    """

    def __init__(
        self,
        db: str,
        to_remember: int = 0,
    ):
        self.db = f"brain/responses/{db}"
        self.to_remember = to_remember
        self.recents_file = (
            f"brain/memory/{Path(db).stem}_recent"
        )

        self.possible = self._possible_responses()
        self.recents = self._recent_responses()

    def _possible_responses(self) -> str:
        with open(self.db) as f:
            try:
                return json.load(f)
            except JSONDecodeError:
                content = f.read()
                return json.dumps(content, ensure_ascii=False)

    def _recent_responses(self) -> list:
        ensure_exists(self.recents_file)
        with open(self.recents_file, "r") as f:
            try:
                return json.load(f)
            except JSONDecodeError:
                return []

    def get_fresh(self) -> str:
        response = ""
        for response in random.sample(
            self.possible, len(self.possible)
        ):
            if response in self.recents:
                continue
            else:
                break

        if response:
            self._remember_as_recent(response)

        return response

    def _remember_as_recent(self, response):
        self.recents.insert(0, response)

        if self.to_remember == 0:
            self.to_remember = len(self.possible) - 1
        del self.recents[self.to_remember :]

        ensure_exists(self.recents_file)
        with open(self.recents_file, "w") as f:
            json.dump(self.recents, f, ensure_ascii=False)
