import json
import pickle
import numpy as np

locations = None
data_columns = None
model = None

def get_estimated_price(location, total_sqft, bhk, bath):
    try:
        loc_index = data_columns.index(location.lower())  # To calculate the index of the location
    except:
        loc_index = -1
    
    x = np.zeros(len(data_columns))
    x[0]= total_sqft
    x[1]= bath
    x[2]= bhk

    if loc_index >= 0:
        x[loc_index] = 1
    
    
    return round(model.predict([x])[0], 2)

def get_location_names():
    return locations

def load_resources():
    print("Loading related data. Please Wait!")
    global locations
    global data_columns
    global model
    
    with open(r'D:\Python\Web_deployment\House_pred\server\resources\columns.json', 'r') as f:
        data_columns = json.load(f)['data_columns']
        locations = data_columns[3:]

    with open(r'D:\Python\Web_deployment\House_pred\server\resources\property_prediction.pickle', 'rb') as f:
        model = pickle.load(f)

    print("Loading Completed. Thank you for your patience!")


if __name__ == "__main__":
    load_resources()
    #print(get_location_names())
    #print(get_estimated_price("1st Phase JP Nagar", 1500, 3, 3))
    #print(get_estimated_price("Ejipura", 1000, 2, 2))