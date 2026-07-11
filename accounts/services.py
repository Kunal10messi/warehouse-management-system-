from accounts.models import User
from django.core.exceptions import ValidationError
from allocations.models import Assignment
import logging
logger = logging.getLogger(__name__)

def create_employee(data):
    email = data.get('email')

    if User.objects.filter(email__iexact=email).exists():
        logger.warning(
            "User creation failed | email=%s already exists",
            email,
        )
        raise ValidationError("Email already exists")

    user = User(
        username=data['username'],
        email=email,
        role=data.get('role', 'EMPLOYEE')
    )
    user.set_password(data['password'])
    user.save()
    logger.info(
        "User created | user_id=%s username=%s role=%s",
        user.id,
        user.username,
        user.role,
    )
    return user

def update_user(user, data):
    if 'email' in data:
        if User.objects.filter(email__iexact=data['email']).exclude(id=user.id).exists():
            logger.warning(
                "User update failed | user_id=%s duplicate_email=%s",
                user.id,
                data["email"],
            )
            raise ValidationError("Email already exists")
        user.email = data['email']

    if 'username' in data:
        if User.objects.filter(username=data['username']).exclude(id=user.id).exists():
            logger.warning(
                "User update failed | user_id=%s duplicate_username=%s",
                user.id,
                data["username"],
            )
            raise ValidationError("Username already exists")
        user.username = data['username']

    if 'role' in data:
        user.role = data['role']

    # 🔥 FIX: handle password properly
    if 'password' in data:
        user.set_password(data['password'])

    user.save()
    logger.info(
        "User updated | user_id=%s username=%s",
        user.id,
        user.username,
    )
    return user

def delete_user(user):
    active_assignment = Assignment.objects.filter(
        user=user,
        actual_return_date__isnull=True
    ).exists()

    if active_assignment:
        logger.warning(
            "User deletion denied | user_id=%s username=%s active_assignment_exists",
            user.id,
            user.username,
        )
        raise ValueError("Cannot delete user with active assignments")
    username = user.username
    user_id = user.id

    user.delete()

    logger.info(
        "User deleted | user_id=%s username=%s",
        user_id,
        username,
    )