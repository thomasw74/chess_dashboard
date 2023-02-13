import requests, io
import chess.pgn as pgn
import pandas as pd


def load_games(username, filename):
    games = []
    try:
        with open(filename) as f:
            while (g := pgn.read_game(f)) is not None:
                games.append(g)
    except:
        r = requests.get(f"http://lichess.org/api/games/user/{username}")
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(r.text)
        with io.StringIO(r.text) as f:
            while (g := pgn.read_game(f)) is not None:
                games.append(g)
    return games


def create_dataframe(games, username):
    # create dataframe from games
    columns = ['Date', 'Site', 'White', 'Black', 'Result', 'Variant', 'TimeControl', 'WhiteElo', 'BlackElo']
    df = pd.DataFrame([[g.headers[k] for k in columns] for g in games], columns=columns)
    # column contains if the user had white
    df['GameWithWhite'] = df['White'] == username
    # opponent data
    df['Opponent'] = df.apply(lambda x: x['Black'] if x['GameWithWhite'] else x['White'], axis=1)
    df['OpponentElo'] = df.apply(lambda x: x['BlackElo'] if x['GameWithWhite'] else x['WhiteElo'], axis=1)
    df.loc[~df['OpponentElo'].str.isdecimal(), 'OpponentElo'] = '0'
    df['OpponentElo'] = df['OpponentElo'].astype('int')
    # result from user perspective
    result_values = {'1-0': 1.0, '1/2-1/2': 0.5, '0-1': 0.0}
    df['Result'] = df['Result'].map(result_values)
    df['Result'] = df.apply(lambda x: x['Result'] if x['GameWithWhite'] else 1.0 - x['Result'], axis=1)
    # change type to category where reasonable
    df['Variant'] = df['Variant'].astype('category')
    df['TimeControl'] = df['TimeControl'].astype('category')
    # drop columns that are no longer needed
    df.drop(['White', 'Black', 'WhiteElo', 'BlackElo'], axis=1, inplace=True)
    # use date as index
    df['Date'] = pd.to_datetime(df.Date)
    df = df.set_index('Date')
    return df


def load_games_dataframe(username):
    games = load_games(username, username + '.pgn')
    return create_dataframe(games, username)


def options(df, column):
    return [{'label': t, 'value': t} for t in df[column].unique()]


def last_games(df):
    return tuple(df.iloc[0:3].reset_index()[['Date', 'Opponent', 'Site']].values.reshape(-1))
