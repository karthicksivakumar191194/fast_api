from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from app.db.database import SessionLocal

class BaseSeeder(ABC):
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    @abstractmethod
    def create_data(self):
        """Abstract method for defining the specific data to be inserted."""
        pass

    def seed(self):
        """Method to seed the database."""
        self.create_data()  # Call the method that creates data
        self.db.commit()  # Commit the changes
        print(f"Seeding completed successfully!")

    def close(self):
        """Close the database session."""
        self.db.close()

    def run(self):
        """Run the seeder."""
        try:
            self.seed()
        finally:
            self.close()

