import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
cars = data.cars()

#app = dash.Dash(__name__,external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

# app.layout = html.Div("Hello World - I am alive. Conda is the worst")

## Plotting

def plot_cars(xcol = 'Horsepower',ycol='Miles_per_Gallon'):
    chart = alt.Chart(cars).mark_point().encode(
        x=xcol,
        y=ycol)

    return chart.interactive().to_html()

## Layout Components

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("GitHub", href="https://github.com"),
                dbc.DropdownMenuItem("Twitter", href="https://twitter.com"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

plot1 = html.Iframe(id='altair_chart',srcDoc=plot_cars(xcol = 'Miles_per_Gallon'),
style={'width': '100%', 'height': '400px'})

plot2 = html.Iframe(id='altair_chart2',srcDoc=plot_cars(xcol = 'Horsepower'),
style={'width': '100%', 'height': '400px'})


random_text= dcc.Markdown('''

        # Title of my Dashboard
        
        ## Level 2 header

        ### Level 3 header
        
        This is a really really long paragraph.
        
        ''')

## Layout
app.layout = dbc.Container([navbar,

    dbc.Alert("Welcome to my app!", color="info"),
    html.Div(
    [
        # html.H1("Title of my Dashboard"),
        # html.H2("Level 2 header"),
        # html.H3("Level 3 header"),
        # html.Blockquote("This is a really really long paragraph."),
        # DCC
        random_text,
        dcc.Checklist(["New York", "Vancouver", "Kelowna"], ["YXX", "YVR", "YYZ"]),
        dcc.Slider(
            min=-5,
            max=10,
            value=0,
            marks={-5: "Really Cold", 0: "Freezing", 3: "Kelowna", 10: "Really Hot"},
        ),
        dcc.Dropdown(id='chart_dropdown',value='Horsepower',options = [{'label': i, 'value': i} for i in cars.columns if i not in ['Name'] ]),
        dcc.Dropdown(id='chart_dropdown2',value='Miles_per_Gallon',options = [{'label': i, 'value': i} for i in cars.columns if i not in ['Name'] ]),
        plot1,
#        plot2,

    ])
])

## Callback functions
@app.callback(
    Output('altair_chart','srcDoc'), # Specifies where the output of plot_cars() "goes"
    Input('chart_dropdown', 'value'),
    Input('chart_dropdown2', 'value'))
def update_plot(xcol,ycol):
    return plot_cars(xcol,ycol)


if __name__ == "__main__":
    app.run_server(host="127.0.0.1", debug=True)