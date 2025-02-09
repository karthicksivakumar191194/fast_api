from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.onboarding import OnboardRequest, OnboardResponse, OnboardResendEmailRequest, \
    OnboardResendEmailResponse
from app.validators.onboarding import validate_onboard_request
from app.services.tenant_service import create_tenant
from app.services.workspace_service import create_default_workspace
from app.services.location_service import create_default_location
from app.services.user_service import create_owner_account
from app.services.email_service import send_account_verification_email

router = APIRouter()


@router.post("/", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
def onboard_account(request: OnboardRequest, db: Session = Depends(get_db)) -> OnboardResponse:
    """
    Endpoint to onboard a new tenant, default workspace, and default location along with creating an owner account.
    The owner will also receive a verification email after the onboarding is complete.
    """

    # Validate the request before proceeding to the business logic
    validate_onboard_request(request, db)

    # Default values
    date_format = "YYYY-MM-DD"
    time_format = "HH:mm:ss"
    time_zone = "UTC"

    # Create Tenant
    tenant = create_tenant(
        db,
        request.company_name,
        request.company_website,
        request.company_size,
        request.company_location,
        request.industry_type,
        date_format,
        time_format,
        time_zone,
        False
    )

    # Create Default Workspace
    workspace = create_default_workspace(db, tenant.id)

    # Create Default Location
    create_default_location(db, tenant.id, workspace.id)

    # Create Default Roles(Admin, Manager, Operator, Sales, Technician)
    # create_default_role(db, tenant.id )

    # Create Owner Account(Admin)
    create_owner_account(db, request.owner_name, request.owner_email, request.owner_mobile_no)

    # Send Account Verification Email
    send_account_verification_email(request.owner_email)

    return OnboardResponse(
        status="success",
        message="Account has been created successfully, and a verification email has been sent to the owner's email."
    )

@router.post("/offline", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
def onboard_account_offline(request: OnboardRequest, db: Session = Depends(get_db)) -> OnboardResponse:
    """
    Endpoint to onboard a new tenant, create a default workspace, and a default location, along with
    creating an owner account by an admin. This endpoint is used for offline onboarding of users,
    where the admin manually sets up a new tenant and owner account.
    """

    # Default values
    date_format = "YYYY-MM-DD"
    time_format = "HH:mm:ss"
    time_zone = "UTC"

    # Create Tenant
    tenant = create_tenant(
        db,
        request.company_name,
        request.company_website,
        request.company_size,
        request.company_location,
        request.industry_type,
        date_format,
        time_format,
        time_zone,
        True
    )

    # Create Default Workspace
    workspace = create_default_workspace(db, tenant.id)

    # Create Default Location under Default Workspace
    create_default_location(db, tenant.id, workspace.id)

    # Create Default Roles(Admin, Manager, Operator, Sales, Technician)
    # create_default_role(db, tenant.id)

    # Create Owner Account(Admin)
    create_owner_account(db, request.owner_name, request.owner_email, request.owner_mobile_no)

    return OnboardResponse(
        status="success",
        message="Account has been created successfully."
    )


@router.post("/resend-verification-email", response_model=OnboardResendEmailResponse, status_code=status.HTTP_200_OK)
def resend_account_verification_email(request: OnboardResendEmailRequest, db: Session = Depends(get_db)) -> OnboardResendEmailResponse:
    """
    Endpoint to resend the account verification email to the owner.
    """
    owner_email = ""

    # Resend Account Verification Email
    send_account_verification_email(owner_email)

    return OnboardResendEmailResponse(
        status="success",
        message="A verification email has been resent successfully to the owner's email."
    )