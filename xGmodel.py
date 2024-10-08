import pandas as pd
import numpy as np
import json

import statsmodels.api as sm
import statsmodels.formula.api as smf

with open('data/events_England.json') as f:
    data = json.load(f)

train = pd.DataFrame(data)
pd.unique(train['subEventName'])
shots = train[train['subEventName'] == 'Shot']
shots_model = pd.DataFrame(columns=['Goal', 'X', 'Y'])

for i, shot in shots.iterrows():

    header = 0
    for shottags in shot['tags']:
        if shottags['id'] == 403:
            header = 1
    # Only include non-headers
    if not (header):
        shots_model.at[i, 'X'] = 100 - shot['positions'][0]['x']
        shots_model.at[i, 'Y'] = shot['positions'][0]['y']
        shots_model.at[i, 'C'] = abs(shot['positions'][0]['y'] - 50)

        # Distance in metres and shot angle in radians.
        x = shots_model.at[i, 'X'] * 105 / 100
        y = shots_model.at[i, 'C'] * 65 / 100
        shots_model.at[i, 'Distance'] = np.sqrt(x ** 2 + y ** 2)
        a = np.arctan(7.32 * x / (x ** 2 + y ** 2 - (7.32 / 2) ** 2))
        if a < 0:
            a = np.pi + a
        shots_model.at[i, 'Angle'] = a

        # Was it a goal
        shots_model.at[i, 'Goal'] = 0
        for shottags in shot['tags']:
            # Tags contain that its a goal
            if shottags['id'] == 101:
                shots_model.at[i, 'Goal'] = 1

model_variables = ['Angle', 'Distance']
model = ''
for v in model_variables[:-1]:
    model = model + v + ' + '
model = model + model_variables[-1]

test_model = smf.glm(formula="Goal ~ " + model, data=shots_model,
                     family=sm.families.Binomial()).fit()

test_model.save("test_model.pkl")