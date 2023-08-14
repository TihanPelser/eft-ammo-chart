from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

eft_df = pd.read_csv('./data/Escape from Tarkov official and actual ammo table - 0.13.5 Patch.csv')
eft_df = eft_df.rename(columns={"0.13.5 Patch": "Calibre"})

eft_df = eft_df.dropna(subset='Calibre')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='EFT Ammo', style={'textAlign':'center'}),
    # dcc.Dropdown(eft_df.Calibre.unique(), '.45 ACP', id='calibre-selection'),
    dcc.Checklist(eft_df.Calibre.unique(), ['.45 ACP'], inline=True, id='calibre-selection'),
    dcc.Dropdown(eft_df.columns, 'Damage', id='x-selection'),
    dcc.Dropdown(eft_df.columns, 'Penetration', id='y-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('calibre-selection', 'value'),
    Input('x-selection', 'value'),
    Input('y-selection', 'value')
)
def update_graph(calibre, x, y):
    dff = eft_df[eft_df.Calibre.isin(calibre)]
    fig = px.scatter(dff, x=x, y=y, text="Ammo", color='Calibre')
    fig.update_traces(textposition='top center')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
