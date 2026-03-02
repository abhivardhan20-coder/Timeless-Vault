from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import VaultItem, User
from deps import get_current_user
from services.hash_service import generate_sha256
from services.encryption import encrypt_data
from services.openai_service import classify_document
from services.blockchain_service import store_hash_on_chain, verify_hash_on_chain
import pdfplumber
import io

router = APIRouter()

@router.get("/vault/verify/{vault_id}")
def verify_hash(vault_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    item = db.query(VaultItem).filter(
        VaultItem.id == vault_id,
        VaultItem.user_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Not found")

    is_valid = verify_hash_on_chain(item.file_hash)

    return {
        "hash": item.file_hash,
        "blockchain_verified": is_valid
    }

@router.post("/vault/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file_bytes = await file.read()

    # Generate SHA-256 hash
    file_hash = generate_sha256(file_bytes)

    # Extract text for AI
    extracted_text = ""
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""
    else:
        extracted_text = file_bytes.decode(errors="ignore")

    if not extracted_text.strip():
        extracted_text = "No readable text found."

    # AI classification
    category, summary = classify_document(extracted_text)

    # Encrypt original file
    encrypted_content = encrypt_data(file_bytes)

    vault_item = VaultItem(
        user_id=current_user.id,
        filename=file.filename,
        encrypted_data=encrypted_content,
        file_hash=file_hash,
        category=category,
        summary=summary
    )

    store_hash_on_chain(file_hash)

    db.add(vault_item)
    db.commit()
    db.refresh(vault_item)

    return {
        "message": "File uploaded successfully",
        "hash": file_hash,
        "category": category,
        "summary": summary
    }

@router.get("/vault/items")
def get_vault_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = db.query(VaultItem).filter(
        VaultItem.user_id == current_user.id
    ).all()
    return items