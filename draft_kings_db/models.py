from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Numeric


Base = declarative_base()


class NBAPerformance(Base):
    __tablename__ = 'performance'
    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    position = Column(String(255))
    team = Column(String(255))
    matchup = Column(String(255))
    date = Column(Date)
    salary = Column(Numeric(asdecimal=False))

    draft_kings_points = Column(Numeric(asdecimal=False))
    rebounds = Column(Numeric(asdecimal=False))
    assists = Column(Numeric(asdecimal=False))
    points = Column(Numeric(asdecimal=False))
    minutes = Column(Numeric(asdecimal=False))
    steals = Column(Numeric(asdecimal=False))
    turnovers = Column(Numeric(asdecimal=False))
    three_pointers = Column(Numeric(asdecimal=False))
    blocks = Column(Numeric(asdecimal=False))
