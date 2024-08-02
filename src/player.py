from save_data_manager import Data, SaveDataManager


class Player:
    """Stores the player's balance and bet. Automatically calls the save data manager as needed."""

    _BASE_BALANCE = 1000
    _balance: int
    _bet = 100
    _save_data_manager: SaveDataManager
    _choice = ""

    def __init__(self):
        self._save_data_manager = SaveDataManager()
        self._balance = self._save_data_manager.load(
            Data.balance, self._BASE_BALANCE)
        self._hand = []


    @property
    def balance(self) -> int:
        """Gets the player's balance."""
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        """Sets the player's balance."""
        self._balance = value
        self._save_data_manager.save(Data.balance, self._balance)

    @property
    def bet(self) -> int:
        """Gets the player's bet."""
        return self._bet

    @property
    def hand(self):
        return self._hand

    @bet.setter
    def bet(self, value: int) -> None:
        """Sets the player's bet."""
        self._bet = value

    def reset_balance(self) -> None:
        """Reset the player's balance to a predefined, default value."""
        self.balance = self._BASE_BALANCE

    @property
    def choice(self) -> str:
        return self._choice
    
    @choice.setter
    def choice(self, selection: str) -> None:
        self._choice = selection

class Dealer(Player):
    def __init__(self):
        super().__init__()
