import dash
from .callbacks import register_callback
from .layout import outer,html_index

def register_dashboard(app):
    dashapp = dash.Dash(server=app) 
    dashapp.index_string = html_index()
    dashapp.layout = outer()
    register_callback(dashapp)

