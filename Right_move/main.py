from google_maps_class import house_hunter
from google_sheets_functions import sheet_hunter

import shelve



def get_shelf():
    my_dict = {"foo":"bar"}

    # file to be used
    shelf = shelve.open("filename.shlf")

    # serializing
    shelf["my_dict"] = my_dict

    shelf.close() # you must close the shelve file!!!


def push_shelf():
    shelf = shelve.open("filename.shlf") # the same filename that you used before, please
    my_dict = shelf["my_dict"]
    shelf.close()
    return my_dict

print(push_shelf())

#x=house_hunter({'Jonty':'Kings Langley','Taka':'Westminster','Jovan':'1 New St Square, London EC4A 3HQ '},'./link.txt')
#x.read(True,"transit",[0,1])
#x.output()
#csv_1= house_hunter({'Jonty':'Kings Langley','Taka':'Westminster','Jovan':'1 New St Square, London EC4A 3HQ '},'./link.txt')