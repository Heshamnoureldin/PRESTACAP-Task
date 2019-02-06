import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.plotly as py
import plotly.graph_objs as go
import base64
import os
import Path_Calculation as PC
import Dependencies as D

#import image that will be use as map background
image_path =os.getcwd() + "\mario.jpg"
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
#add the prefix that plotly will want when using the string as source
encoded_image = "data:image/png;base64," + encoded_string

    
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("SUPER MARIO GAME",style={'color': '#D03B3B','font-family':'Charcoal','font-size': '60px'}),
        html.P("Please Enter The Required Data To Start The Game",style={'color': 'black','font-family':'Charcoal','font-size': '20px','font-style': 'bold '}),
    ], className="jumbotron text-center" ,style={'background-color':'#F7ECD1'}),

    html.Div([
        html.Div([
            html.Div([

                     html.Div([
                         html.Div([
                         ], className="col-md-3"),

                         html.Div([

                             html.Div([
                                 html.Div([
                                     html.Div([
                                         html.Div([
                                             html.Div([
                                                 html.H6('Grid size')
                                             ], className="col-md-3")
                                         ], className="row"),
                                         html.Div([
                                             html.Div([
                                                 dcc.Input(id='gSize', style={'width': 200,'border': '2px solid MediumSeaGreen','background-color': '#EFF9FF'},value='',
                                                           placeholder='Ex:  3', type='number')
                                             ], className="col-md-9")
                                         ], className="row")
                                     ], className="form-group")
                                 ], className="col-md-12")
                             ], className="row"),

                             html.Div([
                                 html.Div([
                                     html.Div([
                                         html.Div([
                                             html.Div([
                                                 html.H6('Mario')
                                             ], className="col-md-3")
                                         ], className="row"),
                                         html.Div([
                                             html.Div([
                                                 dcc.Input(id='mario',style={'width': 200,'border': '2px solid MediumSeaGreen','background-color': '#EFF9FF'}, value='',
                                                           placeholder='Ex:  (0,2)', type='text')
                                             ], className="col-md-9")
                                         ], className="row")
                                     ], className="form-group")
                                 ], className="col-md-12")
                             ], className="row"),

                             html.Div([
                                 html.Div([
                                     html.Div([
                                         html.Div([
                                             html.Div([
                                                 html.H6('Princess')
                                             ], className="col-md-3")
                                         ], className="row"),
                                         html.Div([
                                             html.Div([
                                                 dcc.Input(id='princess',style={'width': 200,'border': '2px solid MediumSeaGreen','background-color': '#EFF9FF'}, value='',
                                                           placeholder='Ex:  (2,1)', type='text')
                                             ], className="col-md-9")
                                         ], className="row")
                                     ], className="form-group")
                                 ], className="col-md-12")
                             ], className="row"),

                             html.Div([
                                 html.Div([
                                     html.Div([
                                         html.Div([
                                             html.Div([
                                                 html.H6('Obstacles')
                                             ], className="col-md-3")
                                         ], className="row"),
                                         html.Div([
                                             html.Div([
                                                 dcc.Input(id='obst',style={'width': 200,'border': '2px solid MediumSeaGreen','background-color': '#EFF9FF'}, value='',
                                                           placeholder='Ex:  (1,1)-(1,2)-...', type='text')
                                             ], className="col-md-9")
                                         ], className="row")
                                     ], className="form-group")
                                 ], className="col-md-12")
                             ], className="row"),

                             html.Div([
                                 html.Div([
                                     html.Button(id='btn',style={'width': 200}, n_clicks=0, children='Play',
                                                 className="button-primary")
                                 ], className="col-md-12")
                             ], className="row")

                         ], className="col-md-3"),

                         html.Div([

                             html.Div([dcc.Graph(id='grid')])

                         ], className="col-md-6")
                     ], className="row" )

                     ], className="col-md-12")
        ], className="row")
    ], className="container")

])

#This callback will be triggered once the button is clicked which leads to execute update_outpute() function
@app.callback(Output('grid', 'figure'),
              [Input(component_id='btn', component_property='n_clicks')],
              [State('gSize', 'value'), State('mario', 'value'),
               State('princess', 'value'), State('obst', 'value')]
              )
def update_output(btnStart, Size, Mario, Princess, Obs):
    
    #Extract List of Obstacles from Obs String assigned by the user
    Obs_list = D.convert_Sring_To_List(Obs)
    #concert sting List to List of points
    Obs_list = [eval(Obs_list[i]) for i in range(len(Obs_list))]
    
    #Extract Mario Position from String assigned by the user
    Mario_position_List = D.convert_Sring_To_List(Mario)
    #concert sting List to List of points
    Mario_position_List = [eval(Mario_position_List[i]) for i in range(len(Mario_position_List))]
    Mario_position = Mario_position_List[0]
    
    #Extract Princess Position from String assigned by the user
    Princess_position_List = D.convert_Sring_To_List(Princess)
    #concert sting List to List of points
    Princess_position_List = [eval(Princess_position_List[i]) for i in range(len(Princess_position_List))]
    Princess_position = Princess_position_List[0]
    
    Size = int(Size)
    Final_Data = go.Scatter(
        x=[0, 4],
        y=[0, 4],
        text=['', ''],
        mode='text'
    )
    #list of grids and points on the graph
    ls = []
    for x in range(0, Size):
        for y in range(0, Size):
            col = 'rgba(255, 255, 255, 0.3)'
            #check if this point is obstacle to make this brown as indication for obstacle 
            if (D.Get_Element_Index(Obs_list,(x,y))> -1):
                col = 'rgba(160,82,45, 1)'
            #check if this point is Mario to make this square blue as indication for Mario
            if (Mario_position[0] == x and Mario_position[1] == y):
                col = 'rgba(65,105,225, 1)'
            #check if this point is Princess to make this square Pink as indication for Mario 
            if (Princess_position[0] == x and Princess_position[1] == y) :
                col = 'rgba(255, 105, 180, 1)'
            point = {'type': 'rect','x0': x,'y0': y,'x1': x + 1,'y1': y + 1,
                     'line': {'color': 'rgba(0,0,0, 1)','width':2 },
                     'fillcolor': col,
                    }
            #add the result grid to the list of rect to be drawn
            ls.append(point)
            
    #object of Astar class that calcuate shortest path
    a = PC.AStar()
    #initlize the map with the values inseted by the user (Grid Size,Mario Position,Princess Position , Obstacles) 
    a.init_grid(Size, Size , Obs_list, Mario_position, Princess_position)
    #start processing to calculate the shortest path
    path = a.process()
    #The final path to be drawn on the map graphically
    Final_path =[]
    #This loop is responsible for adding 0.5 to each point of the resulted path in poth X&y to draw the line in the
    #center of the grid as resulted points are the borders of the grid not the center
    if path is not None:
        for i in path:
          x = i[0] +0.5
          y = i[1] +0.5
          Final_path.append(tuple((x,y)))
          
        #The Line of the shortest path to be drawn on the map 
        for i in range(0, len(Final_path)-1):
            line = {'type': 'line','x0': Final_path[i][0],'y0': Final_path[i][1],'x1': Final_path[i+1][0],'y1': Final_path[i+1][1],
                    'line': {'color': 'rgb(18, 52, 54)','width': 3 },
                   }
            #add the line to the list of figures to be drawn
            ls.append(line)
    #return thr graph of the game result
    return {'data': [Final_Data], 'layout': go.Layout(xaxis=dict(range=[0, Size], showgrid=False, ticks='', showticklabels=False),
                                                  yaxis=dict(range=[0, Size], showgrid=False, ticks='', showticklabels=False),
                                                  shapes=ls, margin=go.layout.Margin(l=50,  r=50, b=100, t=30, pad=4),
                                                  images= [dict(source= encoded_image,xref= "x",yref= "y",
                                                           x= 0,y= Size,sizex= Size,sizey= Size,sizing= "stretch",
                                                           opacity= 0.9,layer= "below")])
            }


if __name__ == '__main__':
    app.run_server(debug=True)
