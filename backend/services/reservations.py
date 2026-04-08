import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from database_models import ReservationCourse, CourseUserCard, CreditCard
from models import ReservationCourseCreateORM


def get_reservation_or_404(db: Session, reservation_id: int) -> ReservationCourse:
    res = db.get(ReservationCourse, reservation_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found.")
    return res


def list_all_reservations(db: Session) -> list[ReservationCourse]:
    return db.query(ReservationCourse).all()


def list_reservations_by_user(db: Session, user_id: int) -> list[ReservationCourse]:
    return (
        db.query(ReservationCourse)
        .join(CourseUserCard, ReservationCourse.course_user_card_id == CourseUserCard.id)
        .join(CreditCard, CourseUserCard.card_id == CreditCard.id)
        .filter(CreditCard.user_id == user_id)
        .all()
    )


def create_reservation(db: Session, reservation_in: ReservationCourseCreateORM) -> ReservationCourse:
    # Valida che il CourseUserCard esista
    db_cuc = db.get(CourseUserCard, reservation_in.course_user_card_id)
    if not db_cuc:
        raise HTTPException(status_code=404, detail="CourseUserCard not found.")

    # Prevenire prenotazioni sovrapposte per lo stesso CourseUserCard nella stessa data/ora
    overlapping = db.query(ReservationCourse).filter(
        ReservationCourse.course_user_card_id == reservation_in.course_user_card_id,
        ReservationCourse.date == reservation_in.date,
        ReservationCourse.from_hour < reservation_in.to_hour,
        ReservationCourse.to_hour > reservation_in.from_hour,
    ).first()
    if overlapping:
        raise HTTPException(status_code=409, detail="Overlapping reservation exists.")

    db_res = ReservationCourse(**reservation_in.model_dump())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res


def delete_reservation(db: Session, reservation_id: int) -> ReservationCourse:
    db_res = get_reservation_or_404(db, reservation_id)
    db.delete(db_res)
    db.commit()
    return db_res


def delete_reservation_by_user(db: Session, reservation_id: int, user_id: int) -> ReservationCourse:
    db_res = get_reservation_or_404(db, reservation_id)

    db_cuc = db.get(CourseUserCard, db_res.course_user_card_id)
    db_card = db.get(CreditCard, db_cuc.card_id) if db_cuc else None
    if not db_card or db_card.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    db.delete(db_res)
    db.commit()
    return db_res


def count_participants_by_course(
    db: Session,
    course_id: int,
    start_date: datetime.date = None,
    end_date: datetime.date = None,
) -> int:
    query = (
        db.query(func.count(ReservationCourse.id))
        .join(CourseUserCard, ReservationCourse.course_user_card_id == CourseUserCard.id)
        .filter(CourseUserCard.course_id == course_id)
    )
    if start_date:
        query = query.filter(ReservationCourse.date >= start_date)
    if end_date:
        query = query.filter(ReservationCourse.date <= end_date)
    return int(query.scalar() or 0)