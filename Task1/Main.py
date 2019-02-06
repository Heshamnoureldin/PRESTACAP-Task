import Map_Validation_Extraction as Map
import Path_Calculation as Path

#initialize the Path list
path =[] 
# initialize the final result list (error_flag + path)
Final_Result = []
# Take the Grid_Size as Input from the user 
Grid_Size =input('Please Enter Grid Size in integer ==>>  ')
try:
    val = int(Grid_Size)
    # Take the Map Discription(Obs,Mario,Princess and Spaces) as Input from the user 
    Grid = input('Please Enter the Grid like ''--m'',''-x-'',''-p-'' ==> ')
    #Remove spaces in the user inputs and conver all char to lower case 
    Grid = Grid.lower().replace(" ","")
    #convert Map Discription to a list of rows and columns
    Grid = Map.convert_Sring_To_List(str(Grid))
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
#In Case The Grid_Size Inserted By The User Is Not a Number
except ValueError:
    Error_Flag = True
    
    
Final_Result.append(Error_Flag)
Final_Result.append(path)
print('Final Result [Error_Flag,Path]==> ',Final_Result) #the final result (error_flag,path)
