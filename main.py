import dash
from dash import dcc, html, Input, Output
import utils, plots


df = utils.load_games_dataframe('t_wille')
app = dash.Dash()
app.layout = html.Div([
    dcc.Dropdown(id='variant_dd', options=utils.options(df, 'Variant')),
    dcc.Dropdown(id='timecontrol_dd', options=utils.options(df, 'TimeControl')),
    dcc.Graph(
        id='graph',
        figure=plots.game_count_heatmap(df, 'Standard', '300+3')),
    html.Div(id='last_games', children=[
        'Test'
    ])])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Output(component_id='last_games', component_property='children'),
    Input(component_id='variant_dd', component_property='value'),
    Input(component_id='timecontrol_dd', component_property='value')
)
def update_plot(variant, timecontrol):
    return plots.game_count_heatmap(df, variant, timecontrol), plots.last_games_list(df, variant, timecontrol, 5)


if __name__ == '__main__':
    app.run_server(debug=False)
