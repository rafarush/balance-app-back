"""seed initial data

Revision ID: seed_data_initial
Revises: 7fe82b095a42
Create Date: 2026-04-25 10:00:00.000000

"""
from typing import Sequence, Union
import uuid
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'seed_data_initial'
down_revision: Union[str, Sequence[str], None] = '7fe82b095a42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Policy names for each model
POLICY_MODELS = ['user', 'role', 'policy', 'transaction']
POLICY_ACTIONS = ['create', 'read', 'update', 'delete']


def _generate_policy_id(model: str, action: str) -> uuid.UUID:
    """Generate deterministic UUID for policy based on model and action."""
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    name = f"{action}-{model}"
    return uuid.uuid5(namespace, name)


def _generate_role_id(role_name: str) -> uuid.UUID:
    """Generate deterministic UUID for role based on name."""
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    return uuid.uuid5(namespace, role_name)


def _generate_user_id(email: str) -> uuid.UUID:
    """Generate deterministic UUID for user based on email."""
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    return uuid.uuid5(namespace, email)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    import bcrypt
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def upgrade() -> None:
    """Seed initial data."""
    conn = op.get_bind()
    now = datetime.now(timezone.utc)

    # 1. Create all policies
    policy_ids = {}
    for model in POLICY_MODELS:
        for action in POLICY_ACTIONS:
            policy_name = f"{action}-{model}"
            policy_id = _generate_policy_id(model, action)
            policy_ids[policy_name] = policy_id

            conn.execute(
                sa.text("""
                    INSERT INTO policy (id, name, description, created_at, updated_at)
                    VALUES (:id, :name, :description, :created_at, :updated_at)
                """),
                {
                    "id": policy_id,
                    "name": policy_name,
                    "description": f"Permission to {action} {model}",
                    "created_at": now,
                    "updated_at": now,
                }
            )

    # 2. Create Admin role with all policies
    admin_role_id = _generate_role_id('Admin')
    conn.execute(
        sa.text("""
            INSERT INTO role (id, name, description, created_at, updated_at)
            VALUES (:id, :name, :description, :created_at, :updated_at)
        """),
        {
            "id": admin_role_id,
            "name": "Admin",
            "description": "Administrator with full access",
            "created_at": now,
            "updated_at": now,
        }
    )

    # 3. Create User role with only transaction policies
    user_role_id = _generate_role_id('User')
    conn.execute(
        sa.text("""
            INSERT INTO role (id, name, description, created_at, updated_at)
            VALUES (:id, :name, :description, :created_at, :updated_at)
        """),
        {
            "id": user_role_id,
            "name": "User",
            "description": "Regular user with transaction access",
            "created_at": now,
            "updated_at": now,
        }
    )

    # 4. Link Admin role to all policies
    for policy_name, policy_id in policy_ids.items():
        conn.execute(
            sa.text("""
                INSERT INTO role_policy (id, role_id, policy_id, created_at, updated_at)
                VALUES (:id, :role_id, :policy_id, :created_at, :updated_at)
            """),
            {
                "id": uuid.uuid4(),
                "role_id": admin_role_id,
                "policy_id": policy_id,
                "created_at": now,
                "updated_at": now,
            }
        )

    # 5. Link User role to only transaction policies
    for action in POLICY_ACTIONS:
        policy_name = f"{action}-transaction"
        policy_id = policy_ids[policy_name]
        conn.execute(
            sa.text("""
                INSERT INTO role_policy (id, role_id, policy_id, created_at, updated_at)
                VALUES (:id, :role_id, :policy_id, :created_at, :updated_at)
            """),
            {
                "id": uuid.uuid4(),
                "role_id": user_role_id,
                "policy_id": policy_id,
                "created_at": now,
                "updated_at": now,
            }
        )

    # 6. Create admin user
    admin_user_id = _generate_user_id('admin@gmail.com')
    conn.execute(
        sa.text("""
            INSERT INTO "user" (id, email, name, surname, hashed_password, is_active, role_id, created_at, updated_at)
            VALUES (:id, :email, :name, :surname, :hashed_password, :is_active, :role_id, :created_at, :updated_at)
        """),
        {
            "id": admin_user_id,
            "email": "admin@gmail.com",
            "name": "admin",
            "surname": "admin",
            "hashed_password": hash_password("admin"),
            "is_active": True,
            "role_id": admin_role_id,
            "created_at": now,
            "updated_at": now,
        }
    )

    # 7. Create regular user
    regular_user_id = _generate_user_id('user@gmail.com')
    conn.execute(
        sa.text("""
            INSERT INTO "user" (id, email, name, surname, hashed_password, is_active, role_id, created_at, updated_at)
            VALUES (:id, :email, :name, :surname, :hashed_password, :is_active, :role_id, :created_at, :updated_at)
        """),
        {
            "id": regular_user_id,
            "email": "user@gmail.com",
            "name": "user",
            "surname": "user",
            "hashed_password": hash_password("user"),
            "is_active": True,
            "role_id": user_role_id,
            "created_at": now,
            "updated_at": now,
        }
    )


def downgrade() -> None:
    """Remove seeded data."""
    conn = op.get_bind()

    # Delete users first (due to foreign key)
    conn.execute(sa.text('DELETE FROM "user" WHERE email IN (\'admin@gmail.com\', \'user@gmail.com\')'))

    # Delete role_policy associations
    conn.execute(sa.text('DELETE FROM role_policy'))

    # Delete roles
    conn.execute(sa.text('DELETE FROM role WHERE name IN (\'Admin\', \'User\')'))

    # Delete policies
    policy_names = [f"{action}-{model}" for model in POLICY_MODELS for action in POLICY_ACTIONS]
    for policy_name in policy_names:
        conn.execute(sa.text("DELETE FROM policy WHERE name = :name"), {"name": policy_name})