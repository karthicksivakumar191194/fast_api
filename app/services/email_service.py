import uuid
from app.settings import settings

def send_account_verification_email(owner_email: str) -> None:
    """
    Generate an account verification link and sends it to the account owner email address.
    """
    verification_token = str(uuid.uuid4())
    verification_link = f"{settings.frontend_url}/verify-email?token={verification_token}"

    print(f"Verification link: {verification_link} sent to {owner_email}")
