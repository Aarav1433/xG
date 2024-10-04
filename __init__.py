import numpy as np

import streamlit as st
from streamlit_drawable_canvas import st_canvas

import statsmodels.api as sm

import pandas as pd

from PIL import Image

field = Image.open("field.jpg")
canvas_result = st_canvas(
    background_image=field,
    drawing_mode="point", stroke_width = 5, stroke_color="red", height=512, width=427, update_streamlit=True
)

test_model = sm.load("test_model.pkl")
model_variables = ['Angle', 'Distance']

def calculate_xG(sh):
    b = test_model.params
    bsum = b[0]
    for i, v in enumerate(model_variables):
        bsum = bsum + b[i + 1] * sh[v]
    xG = 1 / (1 + np.exp(bsum))
    return xG

def run_model(value):
    if value is not None:
        y = (value.pop()/510)*65
        x = (value.pop()/427)*65

        sh = dict()
        a = np.arctan(7.32 * x / (x ** 2 + abs(y - 65 / 2) ** 2 - (7.32 / 2) ** 2))
        if a < 0:
            a = np.pi + a
        sh['Angle'] = a
        sh['Distance'] = np.sqrt(x ** 2 + abs(y - 65 / 2) ** 2)

        final = calculate_xG(sh)
        return ("%.17f" % final).rstrip('0').rstrip('.')
    else:
        return "PLEASE SELECT A POSITION"


if canvas_result.json_data is not None:
    print(canvas_result.json_data)
    objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    values = list()
    for (i,object) in enumerate(objects.values.tolist()):
        x = (object[4])
        y = (object[5])
        value = []
        value.append(x+6.5)
        value.append(y)
        values.append({"Shot Number": i+1, "xG": run_model(value)})
    if len(values) > 0:
        st.dataframe(values)
