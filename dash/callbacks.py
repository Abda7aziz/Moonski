from dash.dependencies import Output,Input,State
import dash_html_components as html
import dash_table
import pandas as pd
from parser import parse_contents
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go

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
                  [Input('dragged','data'),
                  Input('currency','value')])
    def sum(dragged,currency):
        if dragged is not None:
            df = pd.DataFrame(dragged)
            if currency == 'SAR':
                df['Total_Cost'] = df.apply(lambda x: (x['Avg_Price']* x['Adj_Quantity'])*3.75 if x['Market'] != 'Saudi' else x['Avg_Price']* x['Adj_Quantity'],axis=1)
                df['Total_Realized'] = df.apply(lambda x: x['Total_Realized']*3.75 if x['Market'] != 'Saudi' else x['Total_Realized'],axis=1)
            if currency == 'USD':
                df['Total_Cost'] = df.apply(lambda x: (x['Avg_Price']* x['Adj_Quantity'])/3.75 if x['Market'] == 'Saudi' else x['Avg_Price']* x['Adj_Quantity'],axis=1)
                df['Total_Realized'] = df.apply(lambda x: x['Total_Realized']/3.75 if x['Market'] == 'Saudi' else x['Total_Realized'],axis=1)
            df = df[df.groupby('Stock').Date.transform('max') == df['Date']].drop_duplicates(['Date','Stock'],keep='last')
            df.drop(columns=['Price','Fee','Quantity','Date','Type','Cost_In_Market_Currency','Realized_Gains/Losses','%Realized_Gains/Losses'],inplace=True)
            df.rename(columns={'Adj_Quantity':'Holding_Quantity'},inplace=True)

            df = df.round(2)
            return html.Div(
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                    ))

    @app.callback([Output('pie','figure'),
                   Output('totalgains','figure')],
                  [Input('dragged','data'),
                  Input('currency','value')])
    def pie(dragged,currency):
        if dragged is not None:
            df = pd.DataFrame(dragged)
            df = df[df.groupby('Stock').Date.transform('max') == df['Date']].drop_duplicates(['Date','Stock'],keep='last')
            # df = df[df.Adj_Quantity != 0]
            df.Stock = df.Stock.map(lambda x: x.split(' - ')[1] if ' - ' in x else x)
            df.drop(columns=['Cost_In_Market_Currency'],inplace=True)
            if currency == 'SAR':
                df['Total_Cost'] = df.apply(lambda x: (x['Avg_Price']* x['Adj_Quantity'])*3.75 if x['Market'] != 'Saudi' else x['Avg_Price']* x['Adj_Quantity'],axis=1)
                df['Total_Realized'] = df.apply(lambda x: x['Total_Realized']*3.75 if x['Market'] != 'Saudi' else x['Total_Realized'],axis=1)
            if currency == 'USD':
                df['Total_Cost'] = df.apply(lambda x: (x['Avg_Price']* x['Adj_Quantity'])/3.75 if x['Market'] == 'Saudi' else x['Avg_Price']* x['Adj_Quantity'],axis=1)
                df['Total_Realized'] = df.apply(lambda x: x['Total_Realized']/3.75 if x['Market'] == 'Saudi' else x['Total_Realized'],axis=1)
            df = df.round(2)
            fig1 = px.pie(df[df.Adj_Quantity != 0],values='Total_Cost',names='Stock',title='Position Sizes')
            fig2 =   go.Figure(go.Indicator(
                mode = "number+delta",
                value = df.Total_Realized.sum()+df.Total_Cost.sum(),
                number = {'prefix': "$"},
                delta = {'position': "top", 'reference': df.Total_Cost.sum()}
            ))  
                # domain = {'x': [0, 1], 'y': [0, 1]}))
            return (fig1,fig2)
        else:
            return (None,None)