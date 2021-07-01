import dash
from callbacks import register_callback
from layout import output

app = dash.Dash()
app.layout = output
register_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')