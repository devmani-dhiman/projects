import pandas as pd
import pandas as pd 
from sklearn.datasets import load_iris
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

st.title("ML web App using streamlit!!")

st.write("""
## Predicting the Flower species

This app will predict the species on the basis of Length and width
of sepal and petal
"""
)



st.sidebar.header("Input Parameters")

def input_parameters():
    sepal_length = st.sidebar.slider("Sepal Length",4.0, 8.0, 5.8)
    sepal_width = st.sidebar.slider("Sepal Width", 2.0, 5.0, 3.0)
    petal_length = st.sidebar.slider("Petal Length", 1.0, 7.0, 4.3)
    petal_width = st.sidebar.slider("Petal Width", 0.1, 3.0, 1.3)

    data = {"sepal_length": sepal_length,
     "sepal_width": sepal_width,
      "petal_length": petal_length,
       "petal_width": petal_width}

    features = pd.DataFrame(data, index = [0])

    return features

df = input_parameters()

st.subheader("Input feature selection")
st.write(df)


iris = load_iris()
data = iris.data
target = iris.target

clf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123)
clf.fit(data, target)

prediction = clf.predict(df)
prediction_prob = clf.predict_proba(df)

st.subheader("Class labels and their corresponding index values")
st.write(iris.target_names[prediction])

st.subheader("Prediction")
st.write(prediction)

st.subheader("Prediction Probability")
st.write(prediction_prob)