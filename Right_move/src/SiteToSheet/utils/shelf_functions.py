import shelve

def make_data_shelf(path, key = 'link_data'):
    """
    Creates a shelf file named 'link_data' and initializes it with an empty dictionary.

    This function uses the `shelve` module to open a shelf file named 'link_data' in create mode ('c'). The shelf file is then populated with an empty dictionary under the key 'all_data'. Finally, the shelf file is closed.

    Parameters:
    None

    Returns:
    None
    """
    with shelve.open(path, 'c', writeback=True) as shelf:
        shelf[key] = {}
        shelf.close()

def get_shelf_data(path, key = 'link_data'):
    with shelve.open(path , 'c', writeback=True) as shelf:
        retrieved_data = shelf.get(key, {})
        shelf.close()
    return retrieved_data

def print_shelf_data(path, key = 'link_data'):
    with shelve.open(path , 'c', writeback=True) as shelf:
        retrieved_data = shelf.get(key, {})
        print(retrieved_data)
        shelf.close()
    return 

def check_links_shelf(path, links: list, key = 'link_data') -> list:
    with shelve.open(path, 'c', writeback=True) as shelf:
        new_links=[]
        previous_links = [] 
        retrieved_data = shelf.get(key, {})
        if retrieved_data is None:
            retrieved_data = {}
        for i in links:
            if i not in retrieved_data.keys():
                new_links.append(i)
            else:
                previous_links.append(i)
        shelf.close()
    return [new_links , previous_links]
                     
def update_shelf(path, new_data : dict, key = 'link_data'):
    """
    Updates the 'link_data' shelf with the new data provided in the 'new_data' dictionary.
    
    Args:
        new_data (dict): A dictionary containing the new data to be added to the shelf.
        
    Returns:
        dict: A dictionary containing the keys and values of the data that was added to the shelf.
        Keys are links and values are lists of data for each link.
    """
    with shelve.open(path, 'c', writeback=True) as shelf:
        retrieved_data = shelf.get(key, {})
        if retrieved_data is None:
            retrieved_data = {}
        added_data = {}
        for i in new_data.keys():
            if i not in retrieved_data.keys():
                added_data[i] = new_data[i]
        shelf[key] = {**retrieved_data, **added_data}
        shelf.close()
    return added_data

def clear_shelf(path):
    confirm = input("Are you sure you want to clear the shelf? (y/n): ")
    if confirm == "y":
        with shelve.open(path, 'c', writeback=True) as shelf:
            shelf.clear()
            shelf.close()


def update_auxilliary_shelf(path, new_data : dict ):
    """
    Updates the 'link_data' shelf with the new data provided in the 'new_data' dictionary.
    
    Args:
        new_data (dict): A dictionary containing the new data to be added to the shelf.
        
    Returns:
        dict: A dictionary containing the keys and values of the data that was added to the shelf.
        Keys are links and values are lists of data for each link.
    """
    with shelve.open(path, 'c', writeback=True) as shelf:
        retrieved_data = shelf.get('auxilliary', {})
        new_shelf = {**retrieved_data, **new_data}
        shelf['auxilliary'] = new_shelf
        shelf.close()
    return new_shelf