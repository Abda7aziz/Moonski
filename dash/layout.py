import dash_core_components as dcc
import dash_html_components as html


def row1():
    return html.Div([
        html.H3('Stocks Portofolio',className='row'),
        dcc.Markdown("""
        Upload a __csv__ or a __xlsx__ file with the following columns
        * __Date__ : A date column preferably pre-formatted
        * __Type__ : Contains either _Buy_ or _Sell_ strings
        * __Stock__ : The ticker or name of the stock
        * __Market__ : '_Saudi_ , _US_ or _Crypto_ , etc.
        * __Quantity__ : Quantity of shares n the transactions
        * __Price__ : The price of the stock in the transaction
        """,className='nine columns'),
        dcc.RadioItems(id='currency',options=[
            {'label':'SAR','value':'SAR'},
            {'label':'USD','value':'USD'}
        ],value='SAR',className='three columns')
    ],className='row')

def row2():
    row =  html.Div([dcc.Upload(id='file',
    children=html.Div(['Drag and Drop or ',html.A('Select a File')],className='upload'),multiple=True
    ),dcc.Store(id='dragged')],className='row')
    return row

def tab1():
    return dcc.Tab(label='Raw Transactions',children=[
        html.Div(id='tab1',className='row')
    ])


def tab2():
    return dcc.Tab(label='Summary',children=[

        html.Div(id='tab2',className='row')
    ])

def tab3():
    return dcc.Tab(label='Portofolio',children=[
        html.Div(id='tab3',className='row')
    ])

def tab4():
    return dcc.Tab(label='Dashboard',children=[
        html.Div(children=[
            html.Div(dcc.Graph(id='pie'),className='six columns'),
            html.Div(dcc.Graph(id='totalgains'),className='six columns')
        ],className='row')
    ])

output = html.Div(children=[row1(),row2(),dcc.Tabs([tab1(),tab2(),tab3(),tab4()])])