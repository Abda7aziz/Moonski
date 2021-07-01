from dash.dependencies import Output,Input,State
import dash_html_components as html
import dash_table
import pandas as pd
from parser import parse_contents
import pandas as pd
import plotly.express as px

def register_callback(app):

    @app.callback(Output('dragged','data'),
                  Input('file','contents'),
                  State('file','filename'),
                  State('file','last_modified'))
    def store(content,filename,date):
        if content is not None:
            children = [parse_contents(c, n, d) for c, n, d in zip(content,filename,date)]
            return children[0].to_dict('records')


    @app.callback(Output('tab1','children'),
                  Input('dragged','data'))
    def raw(dragged):
        if dragged is not None:
            df = pd.DataFrame(dragged)
            return html.Div(
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                    ))


    @app.callback(Output('tab2','children'),
                  Input('dragged','data'))    
    def sum(dragged):
        if dragged is not None:
            df = pd.DataFrame(dragged)
            df = df[df.groupby('Stock').Date.transform('max') == df['Date']].drop_duplicates(['Date','Stock'],keep='last')
            df = df[df.Adj_Quantity != 0]
            df.drop(columns=['Cost_In_Market_Currency'],inplace=True)
            df['Transacted_Value'] = df.apply(lambda x: (x['Adj_Price']* x['Adj_Quantity'])*3.75 if x['Market'] != 'Saudi' else x['Adj_Price']* x['Adj_Quantity'],axis=1)
            df = df.round(2)
            return html.Div(
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                    ))

    @app.callback(Output('pie','figure'),
                  Input('dragged','data'))
    def pie(dragged):
        if dragged is not None:
            df = pd.DataFrame(dragged)
            df = df[df.groupby('Stock').Date.transform('max') == df['Date']].drop_duplicates(['Date','Stock'],keep='last')
            df = df[df.Adj_Quantity != 0]
            df.Stock = df.Stock.map(lambda x: x.split(' - ')[1] if ' - ' in x else x)
            df.drop(columns=['Cost_In_Market_Currency'],inplace=True)
            df['Transacted_Value'] = df.apply(lambda x: (x['Adj_Price']* x['Adj_Quantity'])*3.75 if x['Market'] != 'Saudi' else x['Adj_Price']* x['Adj_Quantity'],axis=1)
            df = df.round(2)
            fig = px.pie(df,values='Transacted_Value',names='Stock',title='Position Sizes')
            return fig
