
def convert_Sring_To_List(string):
    #Remove any spaces from the input string
    string.replace(" ", "")
    print(string)
    #split the string before and after ',' in separate element in the list
    st_list = list(string.split(","))
    return(st_list)

def Get_Element_Index (ls,element):
    #conver list of string points to list of actual points(tuples)
    try:
     ind = ls.index(element)
    except:
     ind = -1
    return(ind)


def Input_Validation_Function (Grid_Size , Grid):
      ch_list =['x','p','m','-']
      Grid_Size = int(Grid_Size) # convert Gride size string input by the user to integer 
      m_Counter = 0              #initialize 'm' counter
      p_Counter = 0              #initialize 'p' counter
      # check that the grid rows is equal to grid_size
      if(len(Grid)==Grid_Size):
            # iterate on each row in the grid to check the that the number of colums are equal to grid_size
            # and cheack that mario and princess are exist in one position only
            for element in Grid:
                  if(len(element)==Grid_Size):
                       for char in element:
                           #check if the grid contains chars other than 'x','p','m','-'
                           if not (Get_Element_Index (ch_list,char) > -1):
                               return(True)
                       m_Counter += element.count('m') #count mario positions in each row and accumlate the result in the counter 
                       p_Counter += element.count('p') #count Princess positions in each row and accumlate the result in the counter
                  #number of columns in some of the rows are not equal grid_size
                  else:
                        return(True)
            # cheack that mario and princess are exist in one position only
            if((m_Counter==0 or m_Counter >1) or (p_Counter==0 or p_Counter >1)):
                  return(True)
            # mario and princess are exist in more than one position or not exixt 
            else:
                  return(False)
      #The grid rows are not equl grid_size
      else:
            return(True)

def Extract_Obs_Mario_Pricess_Positions (Grid_Size ,Grid):
      Grid_Size = int(Grid_Size)
      Obs_list =[]
      for row in range(0,Grid_Size):
            for col in range(0,Grid_Size):
                  #'x' Means that there is an obstacle
                  if(Grid[row][col] =='x'):
                        Obs_list.append((row,col))
                  #'m' is an indication for mario position
                  elif(Grid[row][col] =='m'):
                        Mario_position =(row,col)
                  #'p' is an indication for princess position
                  elif(Grid[row][col] =='p'):
                        Princess_position = (row,col)
      return(Obs_list,Mario_position,Princess_position)
