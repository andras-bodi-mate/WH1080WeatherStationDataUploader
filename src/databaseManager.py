from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from weatherReading import WeatherReading

class DatabaseManager:
    def __init__(self, databasePath: Path):
        self.databasePath = databasePath
        self.databasePath.parent.mkdir(parents = True, exist_ok = True)
        self.databaseEngine = create_engine(f"sqlite:///{self.databasePath.as_posix()}", echo = True)
        SQLModel.metadata.create_all(self.databaseEngine)

    def getSession(self):
        return Session(self.databaseEngine)

    def save(self, weatherReading: WeatherReading):
        with self.getSession() as session:
            session.add(weatherReading)
            session.commit()