from sqlalchemy.orm import Session

from app.models import User
from app.repository.user_repository import UserRepository


class UserService:
    """
    User Business Service
    """

    @staticmethod
    def get_or_create_user(
        db: Session,
        request
    ) -> User:
        """
        Get an existing user by email or create a new user.

        Business Rules:
        ----------------
        1. Email is the unique identifier.
        2. If the user already exists:
            - Update name if changed.
            - Update mobile number if changed.
            - Return the existing user.
        3. If the user does not exist:
            - Create a new user.
            - Return the newly created user.
        """

        existing_user = UserRepository.find_by_email(
            db=db,
            email=request.email
        )

        # Existing User
        if existing_user:

            updated = False

            if existing_user.full_name != request.full_name:
                existing_user.full_name = request.full_name
                updated = True

            if existing_user.mobile_no != request.mobile_no:
                existing_user.mobile_no = request.mobile_no
                updated = True

            if updated:
                existing_user = UserRepository.update(
                    db=db,
                    user=existing_user
                )

            return existing_user

        # New User
        user = User(
            full_name=request.full_name,
            email=request.email,
            mobile_no=request.mobile_no
        )

        return UserRepository.save(
            db=db,
            user=user
        )