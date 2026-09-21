from datetime import date, timedelta
from typing import Any, Dict, List, Optional
import logging

from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.gamification import Badge, UserBadge, Submission

logger = logging.getLogger("app.services.gamification")


XP_PER_LEVEL = 100
FIRST_SOLVE_XP = 50
FIRST_ATTEMPT_BONUS = 10


def add_xp(db: Session, student_id: int, xp_amount: int) -> Optional[Student]:
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            current_xp = getattr(student, "xp", 0) or 0
            student.xp = current_xp + xp_amount
            student.level = (student.xp // XP_PER_LEVEL) + 1
            db.commit()
            db.refresh(student)
        return student
    except Exception as e:
        logger.error(f"Error adding XP for student {student_id}: {e}")
        db.rollback()
        return None


def _level_for_xp(xp: int) -> int:
    return (max(0, xp) // XP_PER_LEVEL) + 1


def _update_streak(student: Student) -> None:
    today = date.today()
    last = student.last_active_date
    if last == today:
        return
    if last == today - timedelta(days=1):
        student.streak_days = (student.streak_days or 0) + 1
    else:
        student.streak_days = 1
    student.last_active_date = today


def _unlock_badge(db: Session, student_id: int, badge: Badge) -> Optional[Dict[str, Any]]:
    existing = (
        db.query(UserBadge)
        .filter(UserBadge.student_id == student_id, UserBadge.badge_id == badge.id)
        .first()
    )
    if existing:
        return None
    db.add(UserBadge(student_id=student_id, badge_id=badge.id))
    return {
        "id": badge.id,
        "code": badge.code,
        "title": badge.title,
        "description": badge.description,
        "icon_name": badge.icon_name,
        "xp_reward": badge.xp_reward or 0,
    }


def record_submission_and_award_xp(
    db: Session,
    student_id: int,
    assignment_id: int,
    code: str,
    passed: bool,
    execution_time_ms: float = 0.0,
) -> Dict[str, Any]:
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Studentul cu ID-ul {student_id} nu a fost găsit.")

        previous_passes = (
            db.query(Submission)
            .filter(
                Submission.student_id == student_id,
                Submission.assignment_id == assignment_id,
                Submission.passed.is_(True),
            )
            .count()
        )
        previous_attempts = (
            db.query(Submission)
            .filter(
                Submission.student_id == student_id,
                Submission.assignment_id == assignment_id,
            )
            .count()
        )

        db.add(
            Submission(
                student_id=student_id,
                assignment_id=assignment_id,
                code=code,
                passed=bool(passed),
                execution_time_ms=execution_time_ms or 0.0,
            )
        )

        old_level = _level_for_xp(student.xp or 0)
        xp_awarded = 0
        newly_unlocked: List[Dict[str, Any]] = []

        _update_streak(student)

        if passed and previous_passes == 0:
            xp_awarded += FIRST_SOLVE_XP
            if previous_attempts == 0:
                xp_awarded += FIRST_ATTEMPT_BONUS

            badges = {b.code: b for b in db.query(Badge).all()}

            first_blood = badges.get("FIRST_BLOOD")
            if first_blood:
                unlocked = _unlock_badge(db, student_id, first_blood)
                if unlocked:
                    newly_unlocked.append(unlocked)
                    xp_awarded += first_blood.xp_reward or 0

            if previous_attempts == 0:
                perfect = badges.get("PERFECT_ATTEMPT")
                if perfect:
                    unlocked = _unlock_badge(db, student_id, perfect)
                    if unlocked:
                        newly_unlocked.append(unlocked)
                        xp_awarded += perfect.xp_reward or 0

            if execution_time_ms and execution_time_ms < 300:
                speed = badges.get("SPEED_DEMON")
                if speed:
                    unlocked = _unlock_badge(db, student_id, speed)
                    if unlocked:
                        newly_unlocked.append(unlocked)
                        xp_awarded += speed.xp_reward or 0

            if (student.streak_days or 0) >= 3:
                streak = badges.get("STREAK_3")
                if streak:
                    unlocked = _unlock_badge(db, student_id, streak)
                    if unlocked:
                        newly_unlocked.append(unlocked)
                        xp_awarded += streak.xp_reward or 0

        student.xp = (student.xp or 0) + xp_awarded
        student.level = _level_for_xp(student.xp)

        python_pro = db.query(Badge).filter(Badge.code == "PYTHON_PRO").first()
        if python_pro and (student.xp or 0) >= 300:
            unlocked = _unlock_badge(db, student_id, python_pro)
            if unlocked:
                newly_unlocked.append(unlocked)
                student.xp = (student.xp or 0) + (python_pro.xp_reward or 0)
                xp_awarded += python_pro.xp_reward or 0
                student.level = _level_for_xp(student.xp)

        db.commit()
        db.refresh(student)

        new_level = student.level or 1
        return {
            "xp_awarded": xp_awarded,
            "total_xp": student.xp or 0,
            "level": new_level,
            "level_up": new_level > old_level,
            "new_level": new_level,
            "newly_unlocked_badges": newly_unlocked,
            "streak_days": student.streak_days or 0,
        }
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error in record_submission_and_award_xp: {e}")
        db.rollback()
        raise ValueError(f"Eroare la înregistrarea trimiterii: {str(e)}")


def get_leaderboard(db: Session, limit: int = 50) -> List[Dict[str, Any]]:
    students = (
        db.query(Student)
        .filter(Student.role == "student", Student.is_active.is_(True))
        .order_by(Student.xp.desc(), Student.full_name.asc())
        .limit(limit)
        .all()
    )
    entries = []
    for rank, student in enumerate(students, start=1):
        badges_count = db.query(UserBadge).filter(UserBadge.student_id == student.id).count()
        entries.append(
            {
                "rank": rank,
                "user_id": student.id,
                "student_code": student.student_code,
                "full_name": student.full_name,
                "xp": student.xp or 0,
                "level": student.level or 1,
                "streak_days": student.streak_days or 0,
                "badges_count": badges_count,
            }
        )
    return entries


def get_student_profile(db: Session, user_id: int) -> Dict[str, Any]:
    student = db.query(Student).filter(Student.id == user_id).first()
    if not student:
        raise ValueError(f"Utilizatorul cu ID-ul {user_id} nu a fost găsit.")

    xp = student.xp or 0
    level = student.level or _level_for_xp(xp)
    xp_in_level = xp % XP_PER_LEVEL
    all_badges = db.query(Badge).order_by(Badge.id).all()
    unlocked = {
        ub.badge_id: ub
        for ub in db.query(UserBadge).filter(UserBadge.student_id == user_id).all()
    }

    badges = []
    for badge in all_badges:
        ub = unlocked.get(badge.id)
        badges.append(
            {
                "id": badge.id,
                "code": badge.code,
                "title": badge.title,
                "description": badge.description,
                "icon_name": badge.icon_name,
                "xp_reward": badge.xp_reward or 0,
                "is_unlocked": ub is not None,
                "unlocked_at": ub.unlocked_at.isoformat() if ub and ub.unlocked_at else None,
            }
        )

    return {
        "user_id": student.id,
        "student_code": student.student_code,
        "full_name": student.full_name,
        "xp": xp,
        "level": level,
        "streak_days": student.streak_days or 0,
        "last_active_date": student.last_active_date.isoformat() if student.last_active_date else None,
        "progress": {
            "xp_in_level": xp_in_level,
            "xp_per_level": XP_PER_LEVEL,
            "percent": min(100, int((xp_in_level / XP_PER_LEVEL) * 100)),
        },
        "badges": badges,
        "unlocked_badges_count": len(unlocked),
        "total_badges_count": len(all_badges),
    }
