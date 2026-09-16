from fastapi import APIRouter
from app.api.v1.endpoints import (
    health, auth, students, courses, assignments, grades, exercises, notifications, achievements, sandbox, gamification
from app.api.v1.endpoints import health, auth, students, courses, assignments, grades, exercises, notifications, ai_hints

)

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
api_router.include_router(grades.router, prefix="/grades", tags=["Grades"])
api_router.include_router(ai_hints.router, prefix="/ai", tags=["AI Hints"])

api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
api_router.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
api_router.include_router(sandbox.router, prefix="/sandbox", tags=["Sandbox"])
api_router.include_router(gamification.router, prefix="/gamification", tags=["Gamification"])


