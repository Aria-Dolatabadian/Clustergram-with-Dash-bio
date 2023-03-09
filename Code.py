import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bio as dashbio
app = Dash(__name__)

df = pd.read_csv('Cancer.csv').set_index('ID_REF')

columns = list(df.columns.values)
rows = list(df.index)

app.layout = html.Div([
    "Rows to display",
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': row, 'value': row} for row in list(df.index)
        ],
        value=rows[:10],
        multi=True
    ),

    html.Div(id='graph')
])

@app.callback(
    Output('graph', 'children'),
    Input('dropdown', 'value')
)
def update_clustergram(rows):
    if len(rows) < 2:
        return "Please select at least two rows to display."

    return dcc.Graph(figure=dashbio.Clustergram(
        data=df.loc[rows].values,
        column_labels=columns,
        row_labels=rows,
        color_threshold={
            'row': 250,
            'col': 700
        },
        hidden_labels='row',
        height=800,
        width=700,

    ))

if __name__ == '__main__':
    app.run_server(debug=True)
