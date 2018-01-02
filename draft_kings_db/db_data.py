import csv
from datetime import datetime, timedelta
import requests
from draft_kings_db.models import NBAPerformance

DB_START = datetime(2017, 12, 23)
S3_DATA_URL = 'https://s3.amazonaws.com/draftkings-fun/FULL_RESULTS_{}{}{}.csv'


def retrieve_data(session, verbose):
    today = datetime.today()
    row_holder = []
    date_counter = DB_START

    most_recent_data = None

    while date_counter < today:
        try:
            row_holder += _parse_rows_from_csv(date_counter)
            if verbose:
                print('Retrieved data for {}'.format(date_counter))
            most_recent_data = date_counter
        except Exception as e:
            # FIXME - inefficient and will let legitimate errors fall through.
            # Not all days have NBA games
            if verbose:
                print(e)
            pass

        date_counter += timedelta(days=1)

    for row in row_holder:
        found = session \
            .query(NBAPerformance) \
            .filter(
                NBAPerformance.name == row['Name'],
                NBAPerformance.date == row['GameDate']
            ).all()
        if len(found):
            if verbose:
                print('Data already committed for {} ({})'.format(
                    row['Name'],
                    row['GameDate'])
                )
            continue

        g = NBAPerformance(
            name=row['Name'],
            date=row['GameDate'],
            salary=float(row['Salary']),
            team=row['Team'],
            matchup=row['Matchup'],
            draft_kings_points=float(row['DraftKings Points']),
            rebounds=float(row['Rebounds']),
            assists=float(row['Assists']),
            points=float(row['Points']),
            minutes=float(row['Minutes']),
            steals=float(row['Steals']),
            turnovers=float(row['Turnovers']),
            blocks=float(row['Blocks']),
        )
        session.add(g)

    session.commit()
    return most_recent_data


def _parse_rows_from_csv(game_date):
    download = requests.get(S3_DATA_URL.format(
        game_date.year,
        '{}{}'.format('0' if game_date.month < 10 else '', game_date.month),
        '{}{}'.format('0' if game_date.day < 10 else '', game_date.day)
    ))
    if download.status_code != 200:
        raise Exception('No CSV data available for {}'.format(game_date))

    decoded_content = download.content.decode('utf-8')
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')

    rows = []
    for row in reader:
        row['GameDate'] = game_date
        rows.append(row)

    return rows
