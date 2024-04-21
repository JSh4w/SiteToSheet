

import shelve

data={'key':'value'}
# Step 1: Storing data
with shelve.open('mydata') as shelf:
    shelf['my_entry'] = data
    print("Data stored successfully.")

# Step 2: Retrieving data
with shelve.open('mydata', 'r') as shelf:
    retrieved_data = shelf['my_entry']
    print("Data retrieved successfully:")
    print(retrieved_data)
