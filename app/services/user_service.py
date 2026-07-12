from sqlalchemy.orm import Session

from app.models import User
from app.repository.user_repository import UserRepository


class UserService:

    @staticmethod
    def get_or_create_user(
        db: Session, 
        request
    ) -> User:

        existing_user = UserRepository.find_by_email(
            db,
            request.email
        )

        if existing_user:
            return existing_user

        user = User(
            full_name=request.full_name,
            email=request.email,
            mobile_no=request.mobile_no
        )

        return UserRepository.save(
            db,
            user
        )