from this import d
import project, pytest
from test_files.test_variables import test_populate_csv_result, \
    test_display_options_args, test_pagination_args, test_pagination_result_1, \
    test_pagination_result_2

"""
Run using the command `pytest test_project.py -s` or NOT
"""

def test_wait(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "")
    i = input("Enter ")
    assert i == ""


def test_populate_csv():
    assert project.populate_csv("./data/characters.json") == test_populate_csv_result
    pytest.raises(FileNotFoundError, project.populate_csv, "characters.json")
    

def test_display_header():
    assert project.display_header() == None


def test_display_options():
    assert project.display_options(*test_display_options_args) == None


def test_prompt(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 1)
    i = input("What do you want to do? ")
    assert i == 1


def test_pagination():
    assert project.pagination(test_pagination_args, 0) == test_pagination_result_1
    assert project.pagination(test_pagination_args, 1) == test_pagination_result_2


def test_to_table_wizards():
    assert project.to_table_wizards(test_populate_csv_result) == test_pagination_args
    

def test_view(monkeypatch):
    responses = iter([' ', ' ', ' ', ' '])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    assert project.view(test_populate_csv_result) == None


def test_find(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "0")
    assert project.find(test_pagination_args) == None


def test_search_wizard():
    assert project.search_wizard(test_pagination_args, 0, "harry") == [test_pagination_args[0]]
    assert project.search_wizard(test_pagination_args, 0, "cs50") == []


def test_get_wizards():
    assert project.get_wizards() == test_populate_csv_result


def test_about_program(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "")
    assert project.about_program() == None


def test_create_csv(monkeypatch):
    correct_args = ["test.csv", test_populate_csv_result]
    monkeypatch.setattr('builtins.input', lambda _: "")
    assert project.create_csv(*correct_args) == True


def test_reproduce(monkeypatch):
    responses = iter(['y', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    assert project.reproduce(test_populate_csv_result) == True
    

