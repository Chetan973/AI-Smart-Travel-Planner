from sqlalchemy.orm import Session

from app.models import User


class UserRepository:

    @staticmethod
    def find_by_email(
        db: Session,
        email: str
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def save(
        db: Session,
        user: User
    ) -> User:

        db.add(user)

        db.commit()

        db.refresh(user)

        return user
    
    @staticmethod
    def update(
        db: Session,
        user: User
    ) -> User:

        db.commit()

        db.refresh(user)

        return user