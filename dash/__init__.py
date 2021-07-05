import dash
from callbacks import register_callback
from layout import output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
app.layout = output
register_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')
