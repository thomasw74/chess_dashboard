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
        figure=plots.game_count_heatmap(df, 'Standard', '300+3'))])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='variant_dd', component_property='value'),
    Input(component_id='timecontrol_dd', component_property='value')
)
def update_plot(variant, timecontrol):
    return plots.game_count_heatmap(df, variant, timecontrol)


if __name__ == '__main__':
    app.run_server(debug=True)
