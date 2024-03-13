from assets.emails.templates import *


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
    
    These are your login credentials to your personal portal on FarmCI. Keep them save and secure.
    
    """
)

USERNAME_REQUEST_MESSAGE = ACTIVITY_EMAIL_TEMPLATE.format(
    name="{full_name}",
    message="""
    We receive a request for your . Below are your username and email\n\n"
                    
    Your username: {username}
    
    """
)

PASSWORD_RESET_MESSAGE = ACTIVITY_EMAIL_TEMPLATE.format(
    name="{full_name}",
    message="""
    We received your request to reset your password. 
    Complete action with the below OTP. Expires within {expiry}.
    
    {otp}

    """
)


