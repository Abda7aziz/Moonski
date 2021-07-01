import io
import datetime
import base64
import dash_html_components as html
import pandas as pd
import dash_table
import numpy as np

def fee(x):
    if x['Market'] == 'Saudi':
        return x['Quantity']*x['Price']*0.0014449*1.15
    elif x['Market'] == 'US':
        if min(x['Quantity']*x['Price']*0.02999,x['Quantity']*0.0199)>1.99:
            return min(x['Quantity']*x['Price']*0.02999,x['Quantity']*0.0199)*1.150753769
        else:
            return 1.99*1.150753769
    else:
        return 0

def transacted_value(x):
    if x['Type'] == 'Buy':
        return (x['Quantity']*x['Price']) + x['Fee']
    elif x['Type'] == 'Sell':
        return (x['Quantity']*x['Price']) - x['Fee']
    else:
        return x['Quantity']*x['Price']

def feature_eng(df):
    df = df.dropna()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Fee'] = df.apply(fee,axis=1)
    df['Cost_In_Market_Currency'] = df.apply(transacted_value,axis=1)
    df.sort_values(['Stock','Date','Type'], ascending=[True, True, True], inplace=True)
    df['Adj_Quantity'] = df.apply(lambda x: ((x.Type == "Buy") - (x.Type == "Sell")) * x['Quantity'], axis = 1)
    df['Adj_Quantity'] = df.groupby('Stock')['Adj_Quantity'].cumsum()
    df['Adj_Price'] = df.apply(lambda x: ((x.Type == "Buy") - (x.Type == "Sell")) * x['Cost_In_Market_Currency'], axis = 1)
    df['Adj_Price'] = df.groupby('Stock')['Adj_Price'].cumsum().div(df['Adj_Quantity'])
    df.loc[df['Type'] == 'Sell',['Adj_Price']] = np.NaN
    df.fillna(method='ffill', inplace=True)
    df = df.round(2)
    return df

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    df = feature_eng(df)

    return df
    # return html.Div([
    #     dash_table.DataTable(
    #         data=df.to_dict('records'),
    #         columns=[{'name': i, 'id': i} for i in df.columns]
    #     )
    # ])