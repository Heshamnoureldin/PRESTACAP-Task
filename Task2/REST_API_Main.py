import flask
from flask import request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import GameDatabase as DB
import sqlite3
import Path_Calculation as Path
import Map_Validation_Extraction as Map



# Take the Grid_Size as Input from the user 
Grid_Size =input('Please Enter Grid Size in Integer ==>>  ')
# Take the Map Discription(Obs,Mario,Princess and Spaces) as Input from the user 
Grid = input('Please Enter the Grid Like ''--m'',''-x-'',''-p-'' ==> ')
path =[] #initialize the Path list
Final_Result = [] # initialize the final result list (error_flag + path)
#convert Map Discription to a list of rows and columns
Grid = Map.convert_Sring_To_List(Grid)
#validate the map discription inserted by the user 
Error_Flag = Map.Input_Validation_Function (Grid_Size,Grid)
#In case there is no Error in map Desciption
if not Error_Flag:
    #Extract the obstacles ,mario and princess positions
    positions = Map.Extract_Obs_Mario_Pricess_Positions (Grid_Size ,Grid)
    walls = positions[0] #obstacles List
    width = height= int(Grid_Size) #Grid width and Height
    start = positions[1]  #Mario Position
    end = positions[2]    #princess Position
    a = Path.AStar()     #create an object of Astar class that has methods to calculate the shortest path 
    a.init_grid(width, height, walls, start, end)  #Initilaize the Grid 
    path = a.process() #The main method of the class responsible for path calculation 
    
Final_Result.append(Error_Flag)
Final_Result.append(path)


# Creates The Flask Application Object, Which Contains Data About The Application
# Also Contains Methods (Object Functions) That Tell The Application To Do Certain Actions
app = flask.Flask(__name__)

# Starts The Debugger
app.config["DEBUG"] = True

# AUTHORIZATION OBJECT
auth = HTTPBasicAuth()


# This Method to Check Username And Password
@auth.get_password
def get_password(username):
    if username == 'mario':
        return 'PRESTACAP'
    return None

# This Method to Handle Wrong Username And Password
# It Needs To Send The Unauthorized Error Code Back To The Client
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized Access'}), 401)


#Endpoint Nedded For The User To Get Game Result 
@app.route('/api/v1.0/game_results', methods=['GET'])
#To Invoke Return_Result_Save_IN_DB() Function That We Have To Send Our Credentials
@auth.login_required
def Return_Result_Save_IN_DB():
    #Save Game Results and User Inputs Into The Database
    DB.Insert_Into_Game_Database(Grid_Size , Grid , Final_Result)
    return jsonify({'Game Result': str(Final_Result)})


# The Purpose Of Our Page_Not_Found Function Is To Create An Error Page
# Seen By The User If The User Encounters An Error Or Inputs a Route That Hasn’t Been Defined
@app.errorhandler(404)
def Page_Not_Found(e):
    return "<h1>404</h1><p>The Resource Could Not Be Found.</p>", 404


# Endpoint Nedded For The User To Get Log Data From Database 
@app.route('/api/v1.0/log_data', methods=['GET'])
#To Invoke VIEW_LOGDATA_FROM_DATABASE()Function That We Have To Send Our Credentials
@auth.login_required
def VIEW_LOGDATA_FROM_DATABASE():
    LOG_DATA = DB.Read_From_Game_Database()
    return jsonify({'LOG_DATA ': LOG_DATA})

#Runs The Application Server
app.run()
