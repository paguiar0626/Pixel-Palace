import json
from enum import Enum
from pathlib import Path
from typing import Any


class Data(Enum):
    """Maps a given save data attribute to its corresponding JSON object key."""

    balance = "balance"
    music_volume = "music_volume"
    sfx_volume = "sfx_volume"


class SaveDataManager:
    """Manages the player's save data, allowing it to persist between game instances.

    Available attributes to save to or load from are specified in the `Data` enum.
    """
    _FILEPATH = "save-data/data.json"
    _data: dict[str, Any]

    def __init__(self):
        self._data = {
            "balance": None,
            "music_volume": None,
            "sfx_volume": None,
        }

        parent_dir = self._FILEPATH.rsplit("/", 1)[0]
        Path(parent_dir).mkdir(parents=True, exist_ok=True)

        with Path(self._FILEPATH) as path:
            if not path.exists():
                path.touch()
                with open(self._FILEPATH, "w", encoding="utf-8") as file:
                    json.dump(self._data, file)

    def save(self, attribute: Data, new_data: Any) -> None:
        """Save data to disk.

        Args:
            attribute: a member of the Data enum
            new_data: the data to write to disk
        """
        self._data[attribute.value] = new_data
        with open(self._FILEPATH, "w", encoding="utf-8") as file:
            json.dump(self._data, file)

    def load(self, attribute: Data, fallback_value: Any) -> Any:
        """Load data from disk.

        Args:
            attribute: a member of the Data enum
            fallback_value: the value to return if no data is associated with the attribute

        Returns:
            The specified data, or `fallback_value` if no data has yet been saved to the attribute
        """
        with open(self._FILEPATH, "r", encoding="utf-8") as file:
            self._data = dict(json.load(file))
        return self._data[attribute.value] if self._data[attribute.value] is not None else fallback_value
