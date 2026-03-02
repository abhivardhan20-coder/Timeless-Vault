from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import AccessRequest, VaultItem, Nominee, User
from deps import get_current_user

router = APIRouter()

# Step 1: Nominee requests access
@router.post("/access/request/{vault_id}")
def request_access(vault_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    request = AccessRequest(
        vault_item_id=vault_id,
        requester_email=current_user.email
    )

    db.add(request)
    db.commit()

    return {"message": "Access request created"}


# Step 2: Approve request
@router.post("/access/approve/{request_id}")
def approve_access(request_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    request = db.query(AccessRequest).filter(
        AccessRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.approval_count += 1

    if request.approval_count >= 2:
        request.is_approved = True

    db.commit()

    return {
        "approval_count": request.approval_count,
        "is_approved": request.is_approved
    }


# Step 3: List access requests for current user's vault items
@router.get("/access/requests")
def list_access_requests(db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    # Get all vault items belonging to the current user
    vault_item_ids = [
        v.id for v in db.query(VaultItem).filter(
            VaultItem.user_id == current_user.id
        ).all()
    ]

    if not vault_item_ids:
        return []

    requests = db.query(AccessRequest).filter(
        AccessRequest.vault_item_id.in_(vault_item_ids)
    ).all()

    return requests