import dash
from dash import dcc
import pandas as pd
import plotly.express as px
import requests
import chess.pgn as pgn

def load_games(filename):
    games = []
    with open(filename) as f:
        while (g := pgn.read_game(f)) is not None:
            games.append(g)
    return games


def get_games(url, filename):
    r = requests.get(url)
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(r.text)


try:
    games = load_games('games.png')
except:
    get_games('http://lichess.org/api/games/user/t_wille', 'games.png')
    games = load_games('games.png')

columns = ['Date', 'White', 'Black', 'Result', 'Event', 'Variant']
df = pd.DataFrame([[g.headers[k] for k in columns] for g in games], columns=columns)
df['Date'] = pd.to_datetime(df.Date)
df = df.set_index('Date')
games_per_month = df.Event.resample('M').count()
games_per_month_fig = px.line(x=games_per_month.index, y=games_per_month)

games_per_day = df.Event.resample('D').count().reset_index()
games_per_day['weekday'] = games_per_day.Date.dt.day_of_week
games_per_day['first_day_of_week'] = games_per_day.Date.dt.to_period('W').dt.to_timestamp()
games_per_day = games_per_day.drop('Date', axis=1)
games_per_day_fig = px.density_heatmap(games_per_day, x='first_day_of_week', y='weekday', z='Event', nbinsx=50, nbinsy=7)

app = dash.Dash()
app.layout = dcc.Graph(
    id='graph',
    figure=games_per_day_fig)

games_per_day = df.Event.resample('D').count().reset_index()
games_per_day['weekday'] = games_per_day.Date.dt.day_of_week
games_per_day['first_day_of_week'] = games_per_day.Date.dt.to_period('W').dt.to_timestamp()
games_per_day = games_per_day.drop('Date', axis=1)
games_per_day_fig = px.density_heatmap(games_per_day, x='first_day_of_week', y='weekday', z='Event', nbinsx=50, nbinsy=7)

if __name__ == '__main__':
    app.run_server(debug=True)
