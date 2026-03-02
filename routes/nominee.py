from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Nominee, User
from deps import get_current_user

router = APIRouter()

@router.post("/nominee/add")
def add_nominee(email: str,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    nominee = Nominee(
        user_id=current_user.id,
        nominee_email=email
    )

    db.add(nominee)
    db.commit()

    return {"message": "Nominee added"}


@router.get("/nominee/list")
def list_nominees(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    nominees = db.query(Nominee).filter(
        Nominee.user_id == current_user.id
    ).all()
    return nominees