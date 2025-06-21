import pytest
import os
from actions import initialize_vault, load_vault, delete_credential

# --- Test 1: Can we create a vault? ---
def test_initialize_vault():
    """
    Tests if a vault can be initialized correctly.
    """
    result = initialize_vault("test_pass")
    assert result == {}
    assert os.path.exists("vault.salt")
    assert os.path.exists("vault.db")
    os.remove("vault.salt")
    os.remove("vault.db")

# --- Test 2: Can we open a vault? ---
def test_load_vault():
    """
    Tests if a vault can be loaded with correct and incorrect passwords.
    """
    initialize_vault("correct_password")
    assert load_vault("correct_password") == {}
    assert load_vault("wrong_password") is None
    os.remove("vault.salt")
    os.remove("vault.db")
    

# --- Test 3: Does delete work on an empty vault? ---
def test_delete_from_empty_vault(capsys):
    """
    Tests that the delete function handles an empty vault gracefully
    without crashing.
    """
    empty_dict = {}
    delete_credential(empty_dict, "any_password")
    
    # Check that the dictionary is still empty
    assert empty_dict == {}

    # `capsys` is a pytest fixture that captures printed output.
    # We can check that our "empty vault" message was printed.
    captured = capsys.readouterr()
    assert "Your vault is currently empty" in captured.out