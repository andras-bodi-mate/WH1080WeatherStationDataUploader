from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine, select
from weatherReading import WeatherReading
from datetime import timedelta, datetime

class DatabaseManager:
    def __init__(self, databasePath: Path):
        self.databasePath = databasePath
        self.databasePath.parent.mkdir(parents = True, exist_ok = True)
        self.databaseEngine = create_engine(f"sqlite:///{self.databasePath.as_posix()}", echo = False)
        SQLModel.metadata.create_all(self.databaseEngine)

    def getSession(self) -> Session:
        return Session(self.databaseEngine, expire_on_commit=False)

    def getRainDuringTimeDelta(self, timeDelta: timedelta) -> float:
        currentDatetime = datetime.now()
        cutoffDatetime = currentDatetime - timeDelta

        with self.getSession() as session:
            statement = select(WeatherReading).where(WeatherReading.measuredAt >= cutoffDatetime)
            reports = session.exec(statement).all()
            hourlyRainSum = sum((report.rainSinceLastUpdate for report in reports))

        return hourlyRainSum
    
    def getRainInLastHour(self) -> float:
        """Returns the amount of rain that fell in the last hour in millimeters"""
        return self.getRainDuringTimeDelta(timedelta(hours = 1))

    def getRainInLast24Hours(self) -> float:
        """Returns the amount of rain that fell in the last 24 hours in millimeters"""
        return self.getRainDuringTimeDelta(timedelta(hours = 24))

    def save(self, weatherReading: WeatherReading):
        with self.getSession() as session:
            session.add(weatherReading)
            session.commit()