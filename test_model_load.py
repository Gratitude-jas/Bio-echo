import pickle

model = pickle.load(open("models/rf_model.pkl", "rb"))
sample_input = [[0.1, 0.2, 0.3, 150, 0.01, 0.02, 20]]
prediction = model.predict(sample_input)
print("Prediction:", prediction)