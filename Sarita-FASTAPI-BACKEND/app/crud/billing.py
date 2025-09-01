from sqlalchemy.orm import Session
from typing import List, Optional
from models.billing import Subscription, Payment
from app.schemas.billing import SubscriptionCreate, SubscriptionUpdate, PaymentCreate

# --- SubscriptionPlan ---
# This seems to be missing from the Spanish model, commenting out for now.
# def get_plan_by_name(db: Session, name: str) -> Optional[SubscriptionPlan]:
#     return db.query(SubscriptionPlan).filter(SubscriptionPlan.name == name).first()

# --- Subscription ---
def get_subscription_by_tenant(db: Session, inquilino_id: int) -> Optional[Subscription]:
    return db.query(Subscription).filter(Subscription.inquilino_id == inquilino_id).first()

def create_subscription(db: Session, *, obj_in: SubscriptionCreate) -> Subscription:
    db_obj = Subscription(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_subscription(db: Session, *, db_obj: Subscription, obj_in: SubscriptionUpdate) -> Subscription:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- Payment ---
def create_payment(db: Session, *, obj_in: PaymentCreate) -> Payment:
    db_obj = Payment(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_payment_by_gateway_transaction_id(db: Session, transaction_id: str) -> Optional[Payment]:
    return db.query(Payment).filter(Payment.gateway_transaction_id == transaction_id).first()

def update_payment_status(db: Session, *, db_obj: Payment, status: str) -> Payment:
    db_obj.status = status
    db.commit()
    db.refresh(db_obj)
    return db_obj
