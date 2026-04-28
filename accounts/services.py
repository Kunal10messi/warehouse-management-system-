from accounts.models import User
from django.core.exceptions import ValidationError
from allocations.models import Assignment
import logging
logger = logging.getLogger(__name__)

def create_employee(data):
    email = data.get('email')

    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError("Email already exists")

    user = User(
        username=data['username'],
        email=email,
        role=data.get('role', 'EMPLOYEE')
    )
    user.set_password(data['password'])
    user.save()
    logger.info(f"User created: {user.id} ({user.username})")
    return user

def update_user(user, data):
    if 'email' in data:
        if User.objects.filter(email__iexact=data['email']).exclude(id=user.id).exists():
            raise ValidationError("Email already exists")
        user.email = data['email']

    if 'username' in data:
        if User.objects.filter(username=data['username']).exclude(id=user.id).exists():
            raise ValidationError("Username already exists")
        user.username = data['username']

    if 'role' in data:
        user.role = data['role']

    # 🔥 FIX: handle password properly
    if 'password' in data:
        user.set_password(data['password'])

    user.save()
    logger.info(f"User updated: {user.id}")
    return user

def delete_user(user):
    active_assignment = Assignment.objects.filter(
        user=user,
        actual_return_date__isnull=True
    ).exists()

    if active_assignment:
        raise ValueError("Cannot delete user with active assignments")
    logger.info(f"User deleted: {user.id}")
    user.delete()