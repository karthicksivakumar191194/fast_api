from app.seeder.base_seeder import BaseSeeder
from app.models.user import User, UserStatusEnum
from app.utils.helpers import hash_password

class UserSeeder(BaseSeeder):
    def create_data(self):
        users = [
            User(
                name="Test User 1",
                email="test.user1@example.com",
                phone_number="1234567890",
                password=hash_password("password"),
                status=UserStatusEnum.ACTIVE,
            ),
            User(
                name="Test User 2",
                email="test.user2@example.com",
                phone_number="9876543210",
                password=hash_password("password"),
                status=UserStatusEnum.NOT_VERIFIED,
            )
        ]

        # Add users to the session
        self.db.add_all(users)

    def run(self):
        """Override to run the seeder directly from this file."""
        super().run()

if __name__ == "__main__":
    # If the file is executed directly, run the seeder
    user_seeder = UserSeeder()
    user_seeder.run()
