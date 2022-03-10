import dash_core_components as dcc
import dash_html_components as html
from .components import index

def html_index():
    return index

def hero():
    return html.Div(className='hero')

def grid1():
    return html.Div([
        html.Div(id='w-node-_8c7cab7a-95bc-6772-9458-b5c210b781f7-2a6ed86d',
        children=html.H3([html.Span('Upload',className='text-span'),' your transaction data or simply,',html.Br(),\
            html.Span('Drag & Drop',className='text-span'),' it in the box'],className='heading')
                ),
        html.Div(id='control',children=[
            dcc.RadioItems(id='currency',options=[{'label':i,'value':i} for i in ['SAR','USD']],value='SAR')
        ]),
        html.Div(html.P([
            html.Span('Data must be either csv or excel data, and should contain the following:',className='pheading'),html.Br(),
            html.Span('Date',className="text-span"),': a simple transaction date, preferably with time for a better accuracy.',html.Br(),\
            html.Span('Stock',className="text-span"),': The ticker or name of the stock (Must be consistent',html.Br(),\
            html.Span('Type',className="text-span"),': The transaction tpe (Buy, Sell, or Dividends ',html.Br(),\
            html.Span('Market',className="text-span"),': US, Saudi, or Crypto etc.',html.Br(),\
            html.Span('Price',className="text-span"),': The transacted stock price.',html.Br(),\
            html.Span('Fee',className="text-span"),': optional.'],id='p',className='desc')
                ),
        html.Div(id='uploaddiv',children=[
            dcc.Upload(id='file',children=html.Div(['Drag and Drop or ',html.A('Select a File',href='#')],className='uploader'),multiple=True),
            dcc.Store(id='dragged')
                ])
            ],className='w-layout-grid grid1')

def grid2():
    return html.Div(id='main',children=[
        html.Div([
            html.Div([
                html.H1('Total Assets'),html.H1(id='assets1',className='assets')
            ],className='_2verdiv'),
            html.Div([
                html.H1('Change'),html.H1(id='assets2',className='assets')
            ],className='_2verdiv'),
            html.Div([
                html.H1('Change Percentage'),html.H1(id='assets3',className='assets')
            ],className='_2verdiv')
        ],className='_3hordiv'),
        html.Div([
            html.Div(id='table',className='div-block-2'),
            html.Div(id='chart1',className='div-block-2'),
            html.Div(id='chart2',className='div-block-2')
        ],className='_2verdiv stretch')
    ],className='w-layout-grid grid2')

def outer():
    return html.Div([hero(),grid1(),grid2()])