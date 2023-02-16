import plotly.express as px
from dash import html


def game_count_heatmap(df, variant, timecontrol):
    if variant is not None:
        df = df[df['Variant'] == variant]
    if timecontrol is not None:
        df = df[df['TimeControl'] == timecontrol]
    games_per_day = df.Result.resample('M').count().reset_index()
    return px.bar(games_per_day, x='Date', y='Result')


def last_games_list(df, variant, timecontrol, n):
    if variant is not None:
        df = df[df['Variant'] == variant]
    if timecontrol is not None:
        df = df[df['TimeControl'] == timecontrol]
    children = []
    for date, row in df.iloc[:n].iterrows():
        children.append(html.P([html.B(date), html.B(': '), html.A(row['Opponent'], href=row['Site'])]))
    return html.Div(children)
