from .templates import *


WELCOME_MESSAGE = EMAIL_MESSAGE_TEMPLATE.format(
    message="""
    Dear {username},

    Welcome to FarmCI, your go-to resource for discovering the best farms in your area! 
    We’re thrilled to have you join our community of farm enthusiasts and food lovers.
        
    """
)


CREDENTIAL_MESSAGE = EMAIL_MESSAGE_TEMPLATE.format(
    message="""
    We have generated a unique Id for you.
    Here are your credentials. Please keep this save
    
    User Id: {user_id}
    Username: {email}
    Password: {password}
    
    These are your login credentials to your person portal on FarmCI. Keep them save and secure.
    
    """
)

PASSWORD_RESET_MESSAGE = ACTIVITY_EMAIL_TEMPLATE.format(
    name="{full_name}",
    message="""
    We receive a request for your username. Below are your username and email\n\n"
                    
    Your username: {username}
    
    """
)


