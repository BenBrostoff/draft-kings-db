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

    def initialize_nba(self, to_date=None, from_date=None):
        self.most_recent_data = db_data.retrieve_data(
            self.session,
            self.verbose,
            to_date=to_date,
            from_date=from_date,
        )
        print('Retrieved data from {} to {}'.format(
            from_date or db_data.DB_START,
            to_date or self.most_recent_data,
        ))

    def lookup_nba_performances(self, name=None, date=None, limit=5):
        query = self.session.query(models.NBAPerformance)

        if name:
            query = query.filter(models.NBAPerformance.name == name)
        if date:
            query = query.filter(models.NBAPerformance.date == date)

        query = query.order_by(desc(models.NBAPerformance.date))
        return query.limit(limit) if limit else query.all()
