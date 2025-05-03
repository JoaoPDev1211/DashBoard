import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import requests
import psycopg2

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('Dashboard de Gerenciamento Eletro Carneiro', style={'textAlign': 'center', 'color': '#333'}),

    html.Nav([
        html.A('Cadastro de Itens', href='/items', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),
        html.A('Cadastro de Valores', href='/values', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),
        html.A('Cadastro de Clientes', href='/clients', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),
        html.A('Relatórios', href='/reports', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),
        html.A('Entregas',href='https://www.mercadolivre.com.br/', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),   
    ], style={'padding': '10px', 'backgroundColor': '#f0f0f0'}),

    dcc.Tabs(id='tabs', value='dashboard', children=[
        dcc.Tab(label='Dashboard', value='dashboard'),
        dcc.Tab(label='Cadastro de Itens', value='items'),
        dcc.Tab(label='Cadastro de Valores', value='values'),
        dcc.Tab(label='Cadastro de Clientes', value='clients'),
        dcc.Tab(label='Relatórios', value='reports'),
        dcc.Tab(label='Entregas',value='entreg'),
    ]),
    html.Div(id='content')
])

@app.callback(
    Output('content', 'children'),
    Input('tabs', 'value')
)
def update_content(tab):
    if tab == 'dashboard':
        return html.Div([
            dcc.Graph(id='profit-graph'),
            dcc.Interval(
                id='interval-component',
                interval=60*1000,
                n_intervals=0
            )
        ])
    
    elif tab == 'items':
        return html.Div([
            html.H3('Cadastro de Itens'),
            html.Label('Nome do Item'),
            dcc.Input(id='item-name', type='text', placeholder='Digite o nome do item', style={'marginRight': '10px'}),
            html.Label('Categoria'),
            dcc.Input(id='item-category', type='text', placeholder='Digite a categoria do item', style={'marginRight': '10px'}),
            html.Label('Preço'),
            dcc.Input(id='item-price', type='number', placeholder='Digite o preço do item', style={'marginRight': '10px'}),
            html.Button('Salvar', id='save-item', n_clicks=0, style={'marginTop': '10px'})
        ])
    
    elif tab == 'values':
        return html.Div([
            html.H3('Cadastro de Valores'),
            html.Label('Descrição'),
            dcc.Input(id='value-description', type='text', placeholder='Digite a descrição do valor', style={'marginRight': '10px'}),
            html.Label('Valor'),
            dcc.Input(id='value-amount', type='number', placeholder='Digite o valor', style={'marginRight': '10px'}),
            html.Button('Salvar', id='save-value', n_clicks=0, style={'marginTop': '10px'})
        ])
    
    elif tab == 'clients':
        return html.Div([
            html.H3('Cadastro de Clientes'),
            html.Label('Nome do Cliente'),
            dcc.Input(id='client-name', type='text', placeholder='Digite o nome do cliente', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),
            html.Label('E-mail'),
            dcc.Input(id='client-email', type='email', placeholder='Digite o e-mail do cliente', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),
            html.Label('Telefone'),
            dcc.Input(id='client-phone', type='tel', placeholder='Digite o telefone do cliente', style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'}),
            html.Button('Salvar', id='save-client', n_clicks=0, style={'padding': '10px', 'textDecoration': 'none', 'color': '#007bff'})
        ])
    
    elif tab == 'reports':
        return html.Div([
            html.H3('Relatórios'),
        ])
    elif tab =='entreg':
        return html.Div([
            html.H3('Entregas'),
            html.Label('Endereço de Entrega'),
            dcc.Input(id='end-en',type='text',placeholder='Coloque o Endereço do Cliente', style={'padding': '10px', 'borderbox': ' none', 'textDecoration': 'none', 'color': '#007bff'})
        ])

@app.callback(
    Output('profit-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    # Usando a API Alpha Vantage para obter as taxas de câmbio
    api_key = 'ad22e03f8b88a1e1d4eca65cdae700b5'
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=USD&to_symbol=BRL&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    # Verificar se a resposta contém os dados esperados
    if "Time Series FX (Daily)" in data:
        time_series = data["Time Series FX (Daily)"]
        df = pd.DataFrame(columns=["Date", "Close"])
        
        for date, values in time_series.items():
            df = pd.concat([df, pd.DataFrame({"Date": [date], "Close": [float(values["4. close"])]})])
        
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        
        fig = px.line(df, x='Date', y='Close', title='Taxa de Câmbio USD/BRL')
    else:
        fig = px.line(title='Erro ao obter dados da API')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
