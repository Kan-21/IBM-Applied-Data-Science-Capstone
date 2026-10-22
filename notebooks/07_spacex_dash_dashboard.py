"""Historical Falcon 9 first-stage recovery dashboard.

Run from the project root after Notebook 02:
    python 07_spacex_dash_dashboard.py
Then open http://127.0.0.1:8050

Dependencies: dash, pandas, plotly
Data: data/processed/falcon9_labeled_historical.csv
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

ROOT = Path.cwd()
DATA_FILE = ROOT / 'data' / 'processed' / 'falcon9_labeled_historical.csv'
if not DATA_FILE.exists():
    raise FileNotFoundError(f'Run Notebook 02 first, then start Dash from the repository root: {DATA_FILE}')

df = pd.read_csv(DATA_FILE)
required = {'Date', 'LaunchSite', 'Orbit', 'PayloadMass', 'Class', 'BoosterVersion'}
if missing := required - set(df.columns):
    raise ValueError(f'Missing columns: {sorted(missing)}')
df['Date'] = pd.to_datetime(df['Date'], errors='raise')
df['PayloadMass'] = pd.to_numeric(df['PayloadMass'], errors='coerce')
df['Class'] = pd.to_numeric(df['Class'], errors='coerce')
if df['Class'].isna().any() or not df['Class'].isin([0, 1]).all():
    raise ValueError('Recovery Class must be binary (0/1)')
df['Year'] = df['Date'].dt.year
df['OutcomeLabel'] = df['Class'].map({0: 'Not recovered', 1: 'Recovered'})

sites = sorted(df['LaunchSite'].dropna().astype(str).unique())
orbits = sorted(df['Orbit'].dropna().astype(str).unique())
valid_mass = df['PayloadMass'].dropna()
if valid_mass.empty:
    raise ValueError('No numeric payload masses found')
mass_min = int(valid_mass.min() // 500 * 500)
mass_max = int(-(-valid_mass.max() // 500) * 500)
if mass_max <= mass_min:
    mass_max = mass_min + 500

app = Dash(__name__, title='Falcon 9 | Historical Recovery Analytics')
CARD = {'padding': '16px', 'background': '#16263a', 'borderRadius': '12px', 'flex': '1', 'minWidth': '160px'}
LABEL = {'color': '#9eb5cf', 'fontSize': '13px', 'marginBottom': '5px'}
CHART = {'background': '#132338', 'borderRadius': '12px', 'padding': '8px', 'flex': '1', 'minWidth': '320px'}


def kpi(label, value_id):
    return html.Div([html.Div(label, style=LABEL), html.H2(id=value_id, style={'margin': 0})], style=CARD)

app.layout = html.Div([
    html.Div([
        html.Div('FALCON 9  /  HISTORICAL ANALYTICS', style={'color': '#53b4f9', 'letterSpacing': '3px', 'fontSize': '13px'}),
        html.H1('First-stage recovery dashboard', style={'marginBottom': '5px'}),
        html.P('IBM capstone historical dataset (approximately 2010–2020) · Recovery ≠ mission success', style={'color': '#9eb5cf'}),
    ]),
    html.Div([
        html.Div([html.Label('Launch site', style=LABEL), dcc.Dropdown(['All sites'] + sites, 'All sites', id='site', clearable=False, style={'color': '#111827'})], style={'flex': 1, 'minWidth': '210px'}),
        html.Div([html.Label('Orbit', style=LABEL), dcc.Dropdown(['All orbits'] + orbits, 'All orbits', id='orbit', clearable=False, style={'color': '#111827'})], style={'flex': 1, 'minWidth': '210px'}),
        html.Div([html.Label('Payload mass (kg)', style=LABEL), dcc.RangeSlider(min=mass_min, max=mass_max, step=500, value=[mass_min, mass_max], id='payload', tooltip={'placement': 'bottom'})], style={'flex': 2, 'minWidth': '280px'}),
    ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap', 'padding': '20px', 'background': '#16263a', 'borderRadius': '12px'}),
    html.Div([kpi('Launch records', 'kpi-launches'), kpi('Recovered', 'kpi-recovered'), kpi('Recovery rate', 'kpi-rate'), kpi('Payload observations', 'kpi-payload')], style={'display': 'flex', 'gap': '14px', 'flexWrap': 'wrap', 'margin': '18px 0'}),
    html.Div([html.Div(dcc.Graph(id='site-chart'), style=CHART), html.Div(dcc.Graph(id='trend-chart'), style=CHART)], style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap'}),
    html.Div([html.Div(dcc.Graph(id='payload-chart'), style=CHART), html.Div(dcc.Graph(id='orbit-chart'), style=CHART)], style={'display': 'flex', 'gap': '16px', 'flexWrap': 'wrap', 'marginTop': '16px'}),
    html.P('Descriptive historical data only. Recovery rates reflect the course outcome mapping and do not control for mission mix or launch era.', style={'color': '#9eb5cf', 'marginTop': '20px', 'fontSize': '12px'}),
], style={'background': '#0a1728', 'color': '#f1f7ff', 'minHeight': '100vh', 'fontFamily': 'Arial, sans-serif', 'padding': '26px'})


def theme(fig):
    fig.update_layout(template='plotly_dark', paper_bgcolor='#132338', plot_bgcolor='#132338', font={'color': '#e6f1ff'}, margin=dict(l=35, r=25, t=60, b=40))
    return fig


def empty_chart(title):
    fig = px.scatter(title=title)
    fig.add_annotation(text='No records match these filters', x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False)
    return theme(fig)


@app.callback(
    Output('kpi-launches', 'children'), Output('kpi-recovered', 'children'),
    Output('kpi-rate', 'children'), Output('kpi-payload', 'children'),
    Output('site-chart', 'figure'), Output('trend-chart', 'figure'),
    Output('payload-chart', 'figure'), Output('orbit-chart', 'figure'),
    Input('site', 'value'), Input('orbit', 'value'), Input('payload', 'value')
)
def update(site, orbit, payload):
    view = df.copy()
    if site != 'All sites':
        view = view[view['LaunchSite'] == site]
    if orbit != 'All orbits':
        view = view[view['Orbit'] == orbit]
    lo, hi = payload
    view = view[view['PayloadMass'].between(lo, hi, inclusive='both')]
    n = len(view)
    recovered = int(view['Class'].sum())
    header = (f'{n:,}', f'{recovered:,}', f'{recovered/n:.1%}' if n else '—', f'{view["PayloadMass"].notna().sum():,}')
    if not n:
        return (*header, *(empty_chart(t) for t in ['Recovery by launch site', 'Recovery by year', 'Payload vs recovery', 'Recovery by orbit']))

    by_site = (view.groupby('LaunchSite')['Class'].agg(['sum', 'count', 'mean']).reset_index().sort_values('count', ascending=False))
    by_site['Rate %'] = by_site['mean'] * 100
    f1 = px.bar(by_site, x='LaunchSite', y='Rate %', hover_data=['count', 'sum'], title='Recovery rate by launch site (with sample size)', color='count', color_continuous_scale='Blues')
    f1.update_yaxes(range=[0, 100], title='Recovered (%)')
    f1.update_xaxes(title='Launch site')
    f1.update_layout(coloraxis_colorbar_title='Launches')

    by_year = view.groupby('Year')['Class'].agg(['mean', 'count']).reset_index()
    by_year['Rate %'] = by_year['mean'] * 100
    f2 = px.line(by_year, x='Year', y='Rate %', markers=True, hover_data=['count'], title='Historical recovery trend (hover for n)')
    f2.update_yaxes(range=[0, 100], title='Recovered (%)')

    f3 = px.strip(view, x='PayloadMass', y='OutcomeLabel', color='OutcomeLabel', hover_data=['LaunchSite', 'Orbit', 'Date'], title='Payload mass and first-stage recovery', color_discrete_map={'Recovered': '#2dd4bf', 'Not recovered': '#fb7185'})
    f3.update_xaxes(title='Payload mass (kg)')
    f3.update_yaxes(title='Recovery outcome')

    by_orbit = view.groupby('Orbit')['Class'].agg(['mean', 'count']).reset_index().sort_values('mean')
    by_orbit['Rate %'] = by_orbit['mean'] * 100
    f4 = px.bar(by_orbit, x='Rate %', y='Orbit', orientation='h', hover_data=['count'], title='Recovery rate by orbit (hover for n)', color='count', color_continuous_scale='Blues')
    f4.update_xaxes(range=[0, 100], title='Recovered (%)')
    f4.update_yaxes(title='Orbit')
    return (*header, *(theme(fig) for fig in (f1, f2, f3, f4)))


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8050)
