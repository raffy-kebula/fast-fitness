from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from database import get_db
from models import (
    SubscriptionOutORM, SubscriptionCreateORM,
    SubscriptionUserCardCreateORM, SubscriptionUserCardOutORM,
    CurrentUser, UserRole,
)
from routers.auth import get_current_user
from services import subscriptions as sub_service
from services.subscriptions import get_profit_by_week, get_profit_by_year, get_profit_by_month

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


# -------------------------------------------------------------------------
# ADMIN OPERATIONS
# -------------------------------------------------------------------------

@router.post("/", response_model=SubscriptionOutORM, status_code=status.HTTP_201_CREATED)
def create_subscription(
    subscription_in: SubscriptionCreateORM,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Admin privileges required.")
    return sub_service.create_subscription(db, subscription_in)


@router.put("/{subscription_id}", response_model=SubscriptionOutORM, status_code=status.HTTP_200_OK)
def update_subscription(
    subscription_id: int,
    subscription_in: SubscriptionCreateORM,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Admin privileges required.")
    return sub_service.update_subscription(db, subscription_id, subscription_in)


@router.delete("/{subscription_id}", response_model=SubscriptionOutORM)
def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Admin privileges required.")
    return sub_service.delete_subscription(db, subscription_id)


@router.get("/profit/week")
def profit_week(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Admin privileges required.")
    return {"profit_week": get_profit_by_week(db)}


@router.get("/profit/month")
def profit_month(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Admin privileges required.")
    return {"profit_month": get_profit_by_week(db)}


@router.get("/profit/year")
def profit_year(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Admin privileges required.")
    return {"profit_year": get_profit_by_year(db)}


# -------------------------------------------------------------------------
# USER OPERATIONS
# -------------------------------------------------------------------------

@router.get("/list/{user_id}", response_model=list[SubscriptionUserCardOutORM])
def list_subscriptions_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    # Users can only see their own subscriptions; admins can see any
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized.")
    # single JOIN query
    return sub_service.list_subscriptions_by_user(db, user_id)


@router.post("/create_by_user", response_model=SubscriptionUserCardOutORM, status_code=status.HTTP_201_CREATED)
def create_subscription_by_user(
    subscription_user_card_in: SubscriptionUserCardCreateORM,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if subscription_user_card_in.user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized.")
    return sub_service.create_subscription_by_user(db, subscription_user_card_in)


@router.get("/list", response_model=list[SubscriptionOutORM])
def list_subscriptions(
    cost_sup: float,
    db: Session = Depends(get_db),
):
    return sub_service.list_subscriptions(db, cost_sup)


@router.delete("/{subscription_user_card_id}", response_model=SubscriptionUserCardOutORM)
def delete_subscription_by_user(
    subscription_user_card_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if user_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized.")
    return sub_service.delete_subscription_by_user(db, subscription_user_card_id, user_id)

@router.get("/{subscription_id}", response_model=SubscriptionOutORM)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    return sub_service.get_subscription_or_404(db, subscription_id)