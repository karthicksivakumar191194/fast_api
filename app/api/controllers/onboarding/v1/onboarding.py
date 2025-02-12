from fastapi import APIRouter, HTTPException, Depends, Form, status
from sqlalchemy.orm import Session

from app.settings import settings
from app.db.database import get_db
from app.models import Tenant
from app.dependencies.tenant import get_not_verified_tenant
from app.exceptions import NotFound, BadRequest
from app.schemas.onboarding import (
    OnboardRequest,
    OnboardResponse,
    ValidateTenantOTPRequest,
    ValidateTenantOTPResponse,
    ResendOnboardOTPRequest,
    ResendOnboardOTPResponse,
    CompleteTenantSetupRequest,
    CompleteTenantSetupResponse,
    OnboardOfflineRequest,
    OnboardOfflineResponse
)
from app.services.otp_service import generate_tenant_verification_otp, validate_tenant_verification_otp
from app.services.email_service import send_account_verification_otp
from app.services.gsheet_service import add_tenant_details_to_admin_gsheet
from app.services.tenant_service import create_tenant, update_tenant
from app.services.workspace_service import create_default_workspace
from app.services.location_service import create_default_location
from app.services.team_service import create_default_team
from app.services.user_service import create_owner_user
from app.services.role_service import create_default_roles
from app.validators.onboarding import validate_onboard_request

router = APIRouter()

# @router.post("/validate/email", response_model=ValidateTenantOwnerEmailResponse, status_code=status.HTTP_200_OK)
# def validate_tenant_owner_email(
#     request: ValidateTenantOwnerEmailRequest,
#     db: Session = Depends(get_db),
# ) -> ValidateTenantOwnerEmailResponse:
#     """
#     Endpoint to validate tenant owner email already exists.
#     """
#     try:
#         is_tenant_owner_email_exists(request.owner_email)
#
#
#         return ValidateTenantOwnerEmailResponse(
#             status="success",
#             message="Valid OTP."
#         )
#     except BadRequest as e:
#         raise HTTPException(status_code=e.STATUS_CODE, detail=e.detail)
#     except Exception as e:
#         # Catch any unforeseen errors
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="An unexpected error occurred: " + str(e))

@router.post("/", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
def onboard_tenant(
    request: OnboardRequest,
    db: Session = Depends(get_db)
) -> OnboardResponse:
    """
    Endpoint to onboard a new tenant, along with creating an owner account.
    Tenant will be in status "Not Verified" once onboarded.
    The owner will receive an OTP in email for verification after the onboarding is complete.
    """
    try:
        # Validate the request before proceeding to the business logic
        validate_onboard_request(request, db)

        # Create Tenant
        tenant = create_tenant(
            db,
            False,
            request.company_name,
        )

        # Create Owner User
        create_owner_user(db, tenant, request.owner_name, request.owner_email)

        # Generate Tenant Verification OTP
        otp = generate_tenant_verification_otp(db, tenant)

        # Send Account Verification OTP
        send_account_verification_otp(otp, request.owner_email)

        # Sync Tenant Details to Google Sheets
        add_tenant_details_to_admin_gsheet(settings.environment)

        return OnboardResponse(
            status="success",
            message="Account has been created successfully. Use the OTP from the email to proceed."
        )
    except NotFound as e:
        raise HTTPException(status_code=e.STATUS_CODE, detail=e.detail)
    except Exception as e:
        # Catch any unforeseen errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred: " + str(e))


@router.post("/validate/otp", response_model=ValidateTenantOTPResponse, status_code=status.HTTP_200_OK)
def validate_tenant_onboard_otp(
    request: ValidateTenantOTPRequest,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_not_verified_tenant)
) -> ValidateTenantOTPResponse:
    """
    Endpoint to validate the tenant verification OTP.
    """
    try:
        otp = request.otp

        # Validate Tenant Verification OTP
        validate_tenant_verification_otp(tenant, otp)

        # If validation passes, return success response
        return ValidateTenantOTPResponse(
            status="success",
            message="Valid OTP."
        )
    except BadRequest as e:
        raise HTTPException(status_code=e.STATUS_CODE, detail=e.detail)
    except NotFound as e:
        raise HTTPException(status_code=e.STATUS_CODE, detail=e.detail)
    except Exception as e:
        # Catch any unforeseen errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred: " + str(e))


@router.post("/resend/otp", response_model=ResendOnboardOTPResponse, status_code=status.HTTP_200_OK)
def resend_tenant_onboard_otp(
    request: ResendOnboardOTPRequest,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_not_verified_tenant)
) -> ResendOnboardOTPResponse:
    """
    Endpoint to resend tenant verification OTP.
    """
    try:
        # Generate Tenant Verification OTP
        otp = generate_tenant_verification_otp(db, tenant)

        # Send Account Verification OTP
        send_account_verification_otp(otp, request.owner_email)

        return ResendOnboardOTPResponse(
            status="success",
            message="OTP resent successfully. Use the OTP from the email to proceed."
        )
    except NotFound as e:
        raise HTTPException(status_code=e.STATUS_CODE, detail=e.detail)
    except Exception as e:
        # Catch any unforeseen errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred: " + str(e))


@router.put("/complete-tenant-setup", response_model=CompleteTenantSetupResponse,
            status_code=status.HTTP_200_OK)
def complete_tenant_setup(
    request: CompleteTenantSetupRequest,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_not_verified_tenant)
) -> CompleteTenantSetupResponse:
    """
    Endpoint to complete the tenant setup, create a default workspace, default location, default team,
    and default roles.
    Tenant will be updated to status "Active".
    """
    try:
        # Create Default Workspace
        workspace = create_default_workspace(db, tenant)

        # Create Default Location under Default Workspace
        location = create_default_location(db, tenant, workspace)

        # Create Default Team under Default Workspace & Default Location
        create_default_team(db, tenant, workspace, location)

        # Create Default Roles(Admin, Manager, Operator, Sales, Technician)
        create_default_roles(db, tenant)

        # Update Tenant
        update_tenant(db, tenant, request.company_name)

        # Auto Login
        # auto_login(db)

        return CompleteTenantSetupResponse(
            status="success",
            message="Account setup completed successfully."
        )
    except NotFound as e:
        raise HTTPException(status_code=e.STATUS_CODE, detail=e.detail)
    except Exception as e:
        # Catch any unforeseen errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred: " + str(e))


@router.post("/offline", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
def onboard_account_offline(
    request: OnboardOfflineRequest,
    db: Session = Depends(get_db)
) -> OnboardOfflineResponse:
    """
    Endpoint to onboard a new tenant, create a default workspace, default location, default team,
    default roles, along with creating an owner account by an admin. This endpoint is used for
    offline onboarding of users, where the admin manually sets up a new tenant and owner account.
    """

    # Create Tenant
    tenant = create_tenant(
        db,
        True,
        request.company_name,
    )

    # Create Owner User
    create_owner_user(db, tenant, request.owner_name, request.owner_email)

    # Create Default Workspace
    workspace = create_default_workspace(db, tenant)

    # Create Default Location under Default Workspace
    location = create_default_location(db, tenant, workspace)

    # Create Default Team under Default Workspace & Default Location
    create_default_team(db, tenant, workspace, location)

    # Create Default Roles(Admin, Manager, Operator, Sales, Technician)
    create_default_roles(db, tenant)

    return OnboardResponse(
        status="success",
        message="Account has been created successfully."
    )
