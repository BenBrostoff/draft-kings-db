from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from draft_kings_db import models, db_data


class DraftKingsHistory(object):
    def __init__(self, db_url='sqlite:///:memory:', verbose=False):
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
        self.most_recent_data = db_data.retrieve_data(self.session, self.verbose)
        print('Retrieved data from {} to {}'.format(
            db_data.DB_START,
            self.most_recent_data,
        ))

    def lookup_nba_performances(self, name, limit=5):
        if limit is None:
            return (
                self.session
                    .query(models.NBAPerformance)
                    .filter(models.NBAPerformance.name == name)
                    .order_by(desc(models.NBAPerformance.date))
                    .all()
            )
        return (
            self.session
                .query(models.NBAPerformance)
                .filter(models.NBAPerformance.name == name)
                .order_by(desc(models.NBAPerformance.date))
                .limit(limit)
                .all()
        )
