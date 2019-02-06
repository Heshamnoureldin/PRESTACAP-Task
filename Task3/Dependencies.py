
def convert_Sring_To_List(string):
    #Remove any spaces from the input string
    string.replace(" ", "")
    #find elements between '-'and put them as elements of a list
    st_list = list(string.split("-"))
    return(st_list)

def Get_Element_Index (ls,element):
    #conver list of string points to list of actual points(tuples)
    try:
     ind = ls.index(element)
    except:
     ind = -1
    return(ind)
