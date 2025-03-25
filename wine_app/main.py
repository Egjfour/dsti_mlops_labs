import pickle
from flask import Flask, request, jsonify
from model_files.ml_model import predict_wine_quality

##creating a flask app and naming it "app"
app = Flask('app')
@app.route('/test', methods=['GET'])
def test():
    return 'Pinging Model Application!!'

@app.route('/predict', methods=['POST'])
def predict():
    wine_sample = request.get_json()
    print(wine_sample)
    with open('./model_files/model.bin', 'rb') as f_in:
        model = pickle.load(f_in)
        f_in.close()
    predictions = predict_wine_quality(wine_sample, model)
    result = list(predictions)
    # To be able to serialize it (int64 not serialisable)
    formatted_result = []
    for el in result:
        formatted_result.append(int(el))
    return jsonify(formatted_result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
