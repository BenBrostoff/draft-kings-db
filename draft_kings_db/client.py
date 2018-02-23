from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from draft_kings_db import models, db_data


class DraftKingsHistory(object):
    def __init__(
        self,
        db_url='sqlite:///:memory:',
        verbose=False
    ):
        self.most_recent_data = None
        if verbose:
            self.verbose = True
        else:
            self.verbose = False

        engine = create_engine(db_url)
        models.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def initialize_nba(self):
        self.most_recent_data = db_data.retrieve_data(
            self.session,
            self.verbose
        )
        print('Retrieved data from {} to {}'.format(
            db_data.DB_START,
            self.most_recent_data,
        ))

    def lookup_nba_performances(self, name=None, date=None, limit=5):
        query = self.session.query(models.NBAPerformance)

        if name:
            query = query.filter(models.NBAPerformance.name == name)
        if date:
            query = query.filter(models.NBAPerformance.date == date)

        query = query.order_by(desc(models.NBAPerformance.date))
        return query.limit(limit) if limit else query.all()
