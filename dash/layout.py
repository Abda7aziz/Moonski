import dash_core_components as dcc
import dash_html_components as html

def row1():
    return html.Div([
        html.Div([
            html.H3('Stocks Portofolio'),
            dcc.Markdown(id='guide'),
            dcc.RadioItems(id='currency',options=[
                {'label':'SAR','value':'SAR'},
                {'label':'USD','value':'USD'}
            ],value='SAR',labelStyle={'display': 'inline-block'})
            ],className='three columns'),
        html.Div(id='totalgains',className='six columns')
    ],className='row')


def row2():
    row =  html.Div([dcc.Upload(id='file',
    children=html.Div(['Drag and Drop or ',html.A('Select a File',href='#')],className='upload'),multiple=True
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
            html.Div(dcc.Graph(id='pie'),className='six columns')
        ],className='row')
    ])

output = html.Div(children=[row1(),row2(),dcc.Tabs([tab1(),tab2(),tab3(),tab4()])])