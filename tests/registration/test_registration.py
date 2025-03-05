#pylint: disable=missing-class-docstring,missing-module-docstring,line-too-long,missing-function-docstring,wildcard-import,redefined-outer-name
import io
import pytest
from src.dsti_mlops_labs.registration.registration import *


@pytest.fixture
def email_errors():
    possible_errors = {
        "@": 'Email should have exactly 1 "@" symbol',
        ".": 'Email should have at least 1 "." symbol',
        "space": 'Email should not have any spaces',
    }
    return possible_errors

@pytest.fixture
def username_errors():
    possible_errors = {
        "space": 'Username should not have any spaces',
        "empty": 'Username should not be empty',
    }
    return possible_errors

@pytest.fixture
def password_errors():
    possible_errors = {
        "length": 'Password must be at least 8 characters long',
        "number": 'Password must have at least 1 number',
        "letter": 'Password must have at least 1 letter',
        "special": 'Password must have at least 1 special character'
    }
    return possible_errors


class TestUserPrompt:
    @staticmethod
    def test_prompt_user(monkeypatch):
        # Arrange
        expected = 'test'
        monkeypatch.setattr("sys.stdin", io.StringIO(expected))

        # Act
        result = prompt_user("What is your name?")

        # Assert
        assert result == expected
        assert isinstance(result, str)

    @staticmethod
    def test_prompt_user_error_handling(monkeypatch):
        # Arrange
        expected = ''
        monkeypatch.setattr("sys.stdin", io.StringIO(''))

        # Act
        result = prompt_user("What is your name?")

        # Assert
        assert result == expected
        assert not result

class TestUserEmail:
    @staticmethod
    def test_validate_user_email_at_error_too_many(email_errors):
        # Arrange
        email = "test@@test.com"
        expected_error = email_errors["@"]

        # Act
        result = validate_user_email(email)
        print(result)

        # Assert
        assert result== expected_error

    @staticmethod
    def test_validate_user_email_at_error_missing(email_errors):
        # Arrange
        email = "testtest.com"
        expected_error = email_errors["@"]

        # Act
        result = validate_user_email(email)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_user_email_dot_error_missing(email_errors):
        # Arrange
        email = "test@testcom"
        expected_error = email_errors["."]

        # Act
        result = validate_user_email(email)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_user_email_has_space_error(email_errors):
        # Arrange
        email = "test @test.com"
        expected_error = email_errors["space"]

        # Act
        result = validate_user_email(email)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_user_email_valid():
        # Arrange
        email = "test@test.com"

        # Act
        result = validate_user_email(email)

        # Assert
        assert result == ""
        assert not result

    @staticmethod
    def test_capture_user_email_throws_error(monkeypatch):
        # Arrange
        monkeypatch.setattr("sys.stdin", io.StringIO("test @test.com"))

        # Act
        with pytest.raises(ValueError) as e:
            capture_user_email()

        # Assert
        assert e.type == ValueError

    @staticmethod
    def test_capture_user_email_returns_input(monkeypatch):
        # Arrange
        expected = "test@test.com"
        monkeypatch.setattr("sys.stdin", io.StringIO(expected))

        # Act
        result = capture_user_email()

        # Assert
        assert result == expected

class TestUsername:
    @staticmethod
    def test_validate_username_no_space(username_errors):
        # Arrange
        username = "test username"
        expected_error = username_errors["space"]

        # Act
        result = validate_username(username)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_username_not_empty(username_errors):
        # Arrange
        username = ""
        expected_error = username_errors["empty"]

        # Act
        result = validate_username(username)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_username_valid():
        # Arrange
        username = "test"

        # Act
        result = validate_username(username)

        # Assert
        assert result == ""
        assert not result

    @staticmethod
    def test_capture_username_throws_error(monkeypatch, username_errors):
        # Arrange
        monkeypatch.setattr("sys.stdin", io.StringIO(""))

        # Act
        with pytest.raises(ValueError) as e:
            capture_username()

        # Assert
        assert str(e.value) == username_errors["empty"]
        assert e.type == ValueError

    @staticmethod
    def test_capture_username_returns_input(monkeypatch):
        # Arrange
        expected = "test"
        monkeypatch.setattr("sys.stdin", io.StringIO(expected))

        # Act
        result = capture_username()

        # Assert
        assert result == expected

class TestPassword:
    @staticmethod
    def test_validate_password_length(password_errors):
        # Arrange
        password = "test"
        expected_error = password_errors["length"]

        # Act
        result = validate_password(password)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_password_number(password_errors):
        # Arrange
        password = "testtest"
        expected_error = password_errors["number"]

        # Act
        result = validate_password(password)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_password_letter(password_errors):
        # Arrange
        password = "12345678"
        expected_error = password_errors["letter"]

        # Act
        result = validate_password(password)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_password_special(password_errors):
        # Arrange
        password = "test1234"
        expected_error = password_errors["special"]

        # Act
        result = validate_password(password)

        # Assert
        assert result == expected_error

    @staticmethod
    def test_validate_password_valid():
        # Arrange
        password = "test1234!"

        # Act
        result = validate_password(password)

        # Assert
        assert result == ""
        assert not result

    @staticmethod
    def test_capture_password_throws_error(monkeypatch, password_errors):
        # Arrange
        monkeypatch.setattr("sys.stdin", io.StringIO("test"))

        # Act
        with pytest.raises(ValueError) as e:
            capture_password()

        # Assert
        assert str(e.value) == password_errors["length"]
        assert e.type == ValueError

    @staticmethod
    def test_capture_password_returns_input(monkeypatch):
        # Arrange
        expected = "test1234!"
        monkeypatch.setattr("sys.stdin", io.StringIO(expected))

        # Act
        result = capture_password()

        # Assert
        assert result == expected
    
class TestUserRegistration:
    @staticmethod
    def test_register_user_successful(monkeypatch):
        # Arrange
        expected_username = "test"
        expected_email = "test@test.com"
        expected_password = "test1234!"
        expected_user_input = iter([expected_username, expected_email, expected_password])
        monkeypatch.setattr("builtins.input", lambda _: next(expected_user_input))

        # Act
        result = register_user()

        # Assert
        assert isinstance(result, dict)
        assert result["username"] == expected_username
        assert result["email"] == expected_email
        assert result["password"] == expected_password

    @staticmethod
    def test_register_user_throws_error_username(monkeypatch, username_errors):
        # Arrange
        expected_username = "test username"
        expected_error = username_errors["space"]
        monkeypatch.setattr("sys.stdin", io.StringIO(expected_username))

        # Act
        with pytest.raises(ValueError) as e:
            register_user()

        # Assert
        assert str(e.value) == expected_error
        assert e.type == ValueError

    @staticmethod
    def test_register_user_throws_error_email(monkeypatch, email_errors):
        # Arrange
        expected_username = "test"
        expected_email = "test @test.com"
        expected_inputs = iter([expected_username, expected_email])
        expected_error = email_errors["space"]
        monkeypatch.setattr("builtins.input", lambda _: next(expected_inputs))

        # Act
        with pytest.raises(ValueError) as e:
            register_user()

        # Assert
        assert str(e.value) == expected_error
        assert e.type == ValueError

    @staticmethod
    def test_register_user_throws_error_password(monkeypatch, password_errors):
        # Arrange
        expected_username = "test"
        expected_email = "test@test.com"
        expected_password = "testpw"
        expected_inputs = iter([expected_username, expected_email, expected_password])
        expected_error = password_errors["length"]
        monkeypatch.setattr("builtins.input", lambda _: next(expected_inputs))

        # Act
        with pytest.raises(ValueError) as e:
            register_user()

        # Assert
        assert str(e.value) == expected_error
        assert e.type == ValueError
