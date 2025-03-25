import pandas as pd

def predict_wine_quality(data, model):
    
    if type(data) == dict:
        df = pd.DataFrame(data)
    else:
        df = data
    #y_pred = model.predict(df)
    y_pred = model.predict(df).round().astype(int)
    return y_pred
