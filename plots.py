import plotly.express as px


def game_count_heatmap(df, variant, timecontrol):
    if variant is not None:
        df = df[df['Variant'] == variant]
    if timecontrol is not None:
        df = df[df['TimeControl'] == timecontrol]
    games_per_day = df.Result.resample('M').count().reset_index()
    return px.bar(games_per_day, x='Date', y='Result')
