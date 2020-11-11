import dash 

app = dash.Dash(__name__, suppress_callback_exceptions=True, 
            meta_tags=[{'name': 'viewport', 
            'content': 'width=device-width, initial-scal=1.0'}]) #ensures mobile responsive app 

server = app.server 