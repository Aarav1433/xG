import numpy as np

import streamlit as st

from streamlit_image_coordinates import streamlit_image_coordinates

import statsmodels.api as sm

value = streamlit_image_coordinates("https://lh3.googleusercontent.com/fife/ALs6j_GdjcCsyRR6xgBsK4aoU0OdZv5L8gn_qqI6cFE8K8rikstuePskPNexpOTaxfMOKfX0pBP58nBz9KBtwzqmTrGlmDe0xs8JN5xzRFuLA12Zcj1ZAWzQZN2fVVEOYvLe-dRhF3NdJnlTimPHvYn7baIUtXr4Y8Ek2Izr_dZQdV-cmqN7T462HmSV5KNX_IzqxXBAXHT-IF51bYvEqywvI5SgERFrIthIWI3aJh9lpbWiMtXePx0wt2wZe8nsec8nJE6syK8kmoo7XWSfstWPO3tJlb5bzautws-gJ8kR25G0uavBxnRZ72PrtZ6c7lwNHNWe1fEydBCNoOZhBrJb6UA7igCow-pn0mq66c6TkIGZ0INd1ffH7xkmy0kxKFJ3uiuDMlU6f1vZOEj5zl3rcZLn2Umlb9VZrklt2YTkdpUnxl4abivFVSa17zUyj29uYPEWM-W9JKhdOVO4rUGxrlKt5Oiqbehoe9BCRhe0uCDrWgkl-dK8HiT-PwJu2nJWJ6rFEHqOTzNbZtaoMBEx3a4MyTRKpZPSTsEGH0KHCSaMh6XrV-fWsnLdTWIYR0a3fIA3AkJBVs8v86BNFvaPVnKqTWgE0asgIIeVtOAKbPVN8J3NKNWeThNhbr31k87nW6B5p8jDzNudkL6t8ihYrWxkKL-SNtS_DTlP1BtXYAdgfH37EKdOmzHPDefljYWqQ4V_cezD7JO2wkzWPfUu8FrPek2ibC0oLlUSm4ymmfIbc57tfrVON0aqnJEskuyVZHhRBxA9lJ4E3FFXP5TKtcYceu9Y2ZikJahl3J_yL015pUkYYcYnLTtcpJpvuhHN4V5B6MNhGR8tDLkEO8JXrEQYs-4Wzoo4plAcFbxuPVJBJ7Q-Ej737Xvtx2b0NBKhmMHzTN127C5oeAf9uM7MtrONIQH6tbd_7zamYKSVTabCbpNusybWiW1RQM50Opp0YPJqkeUivkGn5NAyrESR-2Bxg5Udk9I1WRrJ1icfOC1hXioVWPvLVwkehxx5RP8_YzNxmRVumjeFvMThr9L11NBxCvfqiK_p7ulyoMb7o-mDHNobqeSdlC8yY6HC10rMcAoeiAtKZRmJXXQpIdI_x64tij1u7M7BV3ubgRd7jpvyr-ebHHSOdSRY7aPAkAshxuagVOgoV8vUZa4bBk-2PfDzXMOG2fMkITrEZeq6zVqJ1NmfSi3-oJugyi_cOh5gZCvnso8aC76_qvdb1sRx7eYJimpoO_q6CgwlLZ0VcJq6E5N14iZxbHC3RZRplxUekT2eBjAZ3qC2cdgdaVvQZymozAx2Dtep0xHwTWVAuxDTM1YfSLCUw2FOZFe18LfuG_RSyPJx8f7FzDUikM_OLL13bUa-s_s1QB4kyjz5gRtUKHh6vP4-8X9foPlHtGcFjjSQA80vlYZocHPjVMACeQXJ9p4HCbvtNV3xXCYDdnNYHZBP0TN1OWtZw02PmrOakl82voRYySGzQ_zAykXzC3ghBYHWErqLZzWLbWpC3101Higqu2YHG7YaKXEEOLLvPsZF4vEqLn8OslfYLORr-lkr_FRngI9Ltd1kiXPJo43_Cck0zKG0GCdZbBqgeCmLzyQIOvqcgf1V7YV67wMYPw=w2880-h1800")

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
        x = (value["x"]/427)*65
        y = (value["y"]/512)*65

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

st.write("EXPECTED GOAL PROBABILITY:")
st.write(run_model(value))