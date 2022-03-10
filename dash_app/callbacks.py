from dash.dependencies import Output,Input,State
import dash_html_components as html
import dash_table
import pandas as pd
from .parser import parse_contents,feature_eng,summary
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
import dash_core_components as dcc

def register_callback(dashapp):

    @dashapp.callback([Output('dragged','data'),
                #    Output('p','style'),
                   Output('main','style')],
                  [Input('file','contents'),
                   Input('currency','value')],
                   State('file','filename'),
                   State('file','last_modified'))
    def store(content,currency,filename,date):
        if content is not None:
            children = [parse_contents(c, n, d) for c, n, d in zip(content,filename,date)]
            return children[0].to_dict('records'),{'visibility':'visible'}
        else:
            return None,None

    @dashapp.callback([Output('assets1','children'),
                   Output('assets2','children'),
                   Output('assets3','children')],
                  [Input('dragged','data'),
                   Input('currency','value')])
    def titles(dragged,currency):
        if dragged is not None:
            df=summary(pd.DataFrame(dragged),monthly=True,holding=False,dollar=False if currency == 'SAR' else True)
            a1 = df['Realized_Gains/Losses'].sum()+df.Total_Cost.sum()
            a2 = df['Realized_Gains/Losses'].sum()
            a3 = a2/df.Total_Cost.sum()*100
            return f"{a1:,.2f}",f"{a2:,.2f}",f"%{a3:.2f}"
        else:
            return None,None,None

    @dashapp.callback(Output('table','children'),
                 [Input('dragged','data'),
                  Input('currency','value')])
    def raw(dragged,currency):
        if dragged is not None:
            dfh = summary(pd.DataFrame(dragged),monthly=False,holding=True,dollar=False if currency == 'SAR' else True)
            return html.Div(
                dash_table.DataTable(
                    data=dfh.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in dfh.columns],
                    style_header={'backgroundColor': 'grey'},
                    style_cell={
                        'backgroundColor': 'rgba(0, 0, 0, 0)',
                        'color': 'white',
                        'font-size':'24px'
                    },
                    ))
        else:
            return None


    @dashapp.callback(Output('chart1','children'),
                [Input('dragged','data'),
                 Input('currency','value')])
    def chart1(dragged,currency):
        if dragged is not None:
            dfm = summary(pd.DataFrame(dragged),monthly=True,dollar=False if currency == 'SAR' else True)
            fig = px.bar(dfm,x=dfm['Date'],y='Realized_Gains/Losses',color='Market',color_discrete_sequence=px.colors.diverging.Geyser,opacity=0.8)
            fig.update_traces(marker_line_color='#ccc',marker_line_width=2)
            fig.update_layout(height=1000,plot_bgcolor='#000',font=dict(color='white'),paper_bgcolor='#000')
            return dcc.Graph(figure=fig)
        else:
            return None

    @dashapp.callback(Output('chart2','children'),
                  [Input('dragged','data'),
                  Input('currency','value')])
    def pie(dragged,currency):
        if dragged is not None:
            dfh = summary(pd.DataFrame(dragged),holding=True,dollar=False if currency == 'SAR' else True)

            dfh=dfh[dfh.Total_Cost != 0]
            fig = px.sunburst(dfh,path=['Market','Stock'],
            values='Total_Cost',color='Total_Cost',color_continuous_scale=px.colors.sequential.Greens)
            fig.update_layout(paper_bgcolor='black',margin = dict(t=50, l=25, r=25, b=25),coloraxis_showscale=False)1
            return dcc.Graph(figure=fig)
        else:
            return None