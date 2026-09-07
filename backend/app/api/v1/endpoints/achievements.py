from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.student import Student
from app.models.achievement import Achievement, StudentAchievement


router = APIRouter()


def calculate_level_info(total_xp: int) -> Dict[str, Any]:
    """Calculates student level and rank title based on total XP."""
    level = 1 + (total_xp // 200)
    current_level_base = (level - 1) * 200
    next_level_xp = level * 200
    xp_in_level = total_xp - current_level_base

    rank_titles = {
        1: "Începător Python 🐣",
        2: "Explorator de Cod 🔍",
        3: "Algoritmist Junior ⚡",
        4: "Dezvoltator Software 💻",
        5: "Arhitect ArkiTech 🏆",
    }
    title = rank_titles.get(min(level, 5), "Arhitect ArkiTech 🏆")

    return {
        "level": level,
        "title": title,
        "total_xp": total_xp,
        "xp_in_level": xp_in_level,
        "next_level_xp": 200,  # XP needed per level
        "level_progress_percent": min(100, int((xp_in_level / 200) * 100))
    }


@router.get("/", summary="List all system achievements")
def get_all_achievements(db: Session = Depends(get_db)):
    achievements = db.query(Achievement).all()
    return achievements


@router.get("/my", summary="Get current student's unlocked achievements and XP stats")
def get_my_achievements(
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    all_achievements = db.query(Achievement).all()
    unlocked = db.query(StudentAchievement).filter(StudentAchievement.student_id == current_user.id).all()
    unlocked_map = {ua.achievement_id: ua.unlocked_at for ua in unlocked}

    total_xp = 0
    results = []
    for ach in all_achievements:
        is_unlocked = ach.id in unlocked_map
        if is_unlocked:
            total_xp += ach.xp_reward

        results.append({
            "id": ach.id,
            "code": ach.code,
            "title": ach.title,
            "description": ach.description,
            "icon": ach.icon,
            "xp_reward": ach.xp_reward,
            "category": ach.category,
            "unlocked": is_unlocked,
            "unlocked_at": unlocked_map.get(ach.id)
        })

    level_info = calculate_level_info(total_xp)

    return {
        "achievements": results,
        "unlocked_count": len(unlocked),
        "total_count": len(all_achievements),
        "stats": level_info
    }
