"""
Module to capture terminal input registration data for users
"""
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

def prompt_user(question: str) -> str:
    """
    Prompt the user for input and return the response
    Handles for the annoying case where the user provides no input

    Args:
        question (str): The question to ask the user

    Returns:
        str: The user's response
    """
    try:
        response = input(question)
    except EOFError:
        response = ''

    return response

def validate_user_email(email: str) -> bool:
    """
    Validate the user's email address

    Args:
        email (str): The user's email address

    Returns:
        bool: True if the email address is valid, False otherwise
    """
    # Initialize the condition to an empty string
    cond = ''

    # Check if the email address is missing the "@" symbol or has too many
    if email.count('@') != 1:
        cond = 'Email should have exactly 1 "@" symbol'

    # Check if the email address is missing the "." symbol
    if email.count('.') < 1:
        cond = 'Email should have at least 1 "." symbol'

    # Check if the email address has any spaces in it
    if ' ' in email:
        cond = 'Email should not have any spaces'

    return cond

def capture_user_email() -> str:
    """
    Prompt the user for their email address
    Perform validation to ensure the email address is valid

    Returns:
        str: The user's email address
    """
    response = prompt_user("What is your email address? ")

    # Validate the user's email address
    validation = validate_user_email(response)
    if validation:
        raise ValueError(validation)
    
    return response

def validate_username(username: str) -> str:
    """
    Validates the given username based on specific conditions.
    Args:
        username (str): The username to be validated.
    Returns:
        str: An error message if the username is invalid, otherwise an empty string.
    """
    # Initialize
    cond = ''

    # No spaces
    if ' ' in username:
        cond = 'Username should not have any spaces'

    # Not empty 
    if not username:
        cond = 'Username should not be empty'
    
    return cond

def capture_username() -> str:
    """
    Captures the username from the user input.
    Prompts the user to enter their username and validates it. If the username
    is invalid, raises a ValueError with the validation message.
    Args:
        None
    Returns:
        str: The validated username entered by the user.
    Raises:
        ValueError: If the username is invalid.
    """
    # Prompt the user for their username
    response = prompt_user("What is your username? ")

    # Validate the user's username
    validation = validate_username(response)
    if validation:
        raise ValueError(validation)
    
    return response

def validate_password(password: str) -> str:
    """
    Validates the given password based on specific criteria.
    Args:
        password (str): The password to validate.
    Returns:
        str: An empty string if the password is valid, otherwise a string describing the validation error.
    """
    # At least 8 characters long
    if len(password) < 8:
        cond = 'Password must be at least 8 characters long'
    # At least 1 number
    elif not any(char.isdigit() for char in password):
        cond = 'Password must have at least 1 number'
    # At least 1 letter
    elif not any(char.isalpha() for char in password):
        cond = 'Password must have at least 1 letter'
    # At least 1 special character
    elif not any(not char.isalnum() for char in password):
        cond = 'Password must have at least 1 special character'
    # Default condition
    else:
        cond = ''

    return cond

def capture_password() -> str:
    """
    Captures the password from the user input.
    Prompts the user to enter their password and validates it. If the password
    is invalid, raises a ValueError with the validation message.
    Args:
        None
    Returns:
        str: The validated password entered by the user.
    Raises:
        ValueError: If the password is invalid.
    """
    # Prompt the user for their password
    response = prompt_user("What is your password? ")

    # Validate the user's password
    validation = validate_password(response)
    if validation:
        raise ValueError(validation)
    
    return response

def register_user() -> dict:
    """
    Register a user by capturing their username, email, and password.
    Returns a dictionary with the user's information.
    Args:
        None
    Returns:
        dict: A dictionary containing the user's information.
    """
    # Capture the user's username
    username = capture_username()

    # Capture the user's email address
    email = capture_user_email()

    # Capture the user's password
    password = capture_password()

    # Return the user's information
    return {
        'username': username,
        'email': email,
        'password': password
    }

# Execute the registration process if the script is directly run
if __name__ == "__main__":
    print("Registering the user")
    user_details = register_user()

    # Sink the user details to a file
    filename = f"user_details_{user_details.get('username')}.txt"
    current_path = os.getcwd()
    filepath = os.path.join(current_path, filename)

    # Debugging: Print the current working directory and file path
    print("Current working directory:", current_path)
    print("File will be written to:", filepath)

    with open(filepath, "w", encoding='UTF-8') as f:
        f.write(str(user_details))

    # Verify the file was created
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} was not created successfully.")

    # Copy out to blob with azcopy
    BLOB_SAS_TOKEN = os.getenv("BLOB_SAS_TOKEN")
    if not BLOB_SAS_TOKEN:
        raise ValueError("BLOB_SAS_TOKEN environment variable is not set")

    azcopy_command = [
        "azcopy", "copy", filepath,
        f"https://eddiejenkins.blob.core.windows.net/mlops-labs/registration/{filename}{BLOB_SAS_TOKEN}"
    ]

    # Debugging: Print the azcopy command
    print("Running azcopy command:", " ".join(azcopy_command))

    subprocess.run(azcopy_command, check=True)
    print("User details registered successfully")
