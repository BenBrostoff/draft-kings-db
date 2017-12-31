from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from draft_kings_db import models, db_data


class DraftKingsHistory(object):
    def __init__(self, db_url='sqlite:///:memory:', verbose=False):
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
        db_data.retrieve_data(self.session, self.verbose)

    def lookup_nba_performances(self, name, limit=5):
        return (
            self.session
                .query(models.NBAPerformance)
                .filter(models.NBAPerformance.name == name)
                .limit(limit)
                .all()
        )
