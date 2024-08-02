from unittest.mock import ANY, patch

from player import Player
from save_data_manager import Data


@patch("player.SaveDataManager.save")
def test_call_save_value(mock_save):
    """Setting the player's balance to 300 results in a call to SaveData with a value of 300."""
    """Note that player.balance is a setter property."""
    player = Player()
    player.balance = 300
    mock_save.assert_called_once_with(ANY, 300)


@patch("player.SaveDataManager.save")
def test_call_save_attribute(mock_save):
    """Setting the player's balance uses only the Data.balance property of SaveData, ensuring unrelated data is not accidentally overwritten."""
    player = Player()
    player.balance = 300
    mock_save.assert_called_once_with(Data.balance, ANY)


@patch("player.SaveDataManager.load")
def test_call_load_attribute(mock_load):
    """When a new Player is instantiated, its balance is automatically loaded from SaveData."""
    _ = Player()
    mock_load.assert_called_once_with(Data.balance, ANY)


@patch("player.SaveDataManager.load")
def test_initial_load(mock_load):
    """The return value from SaveData.load() is stored, unaltered, in Player."""
    test_value = 8688
    mock_load.return_value = test_value
    player = Player()
    assert player.balance == test_value


def test_reset_balance():
    """The Player's balance is set to the appropriate value when reset."""
    base_balance = Player._BASE_BALANCE
    player = Player()
    player.balance = -10000
    player.reset_balance()
    assert player.balance == base_balance
