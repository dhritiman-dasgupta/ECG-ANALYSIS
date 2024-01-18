from fastapi import FastAPI
from pydantic import BaseModel

class ECG(BaseModel):
    ecg: List[float]

# ------------------------------------------- importing dependencies ----------------------------------------#
import datetime
import os
import numpy as np
import pandas as pd
import math
import json
import neurokit2 as nk
import sklearn
import xgboost as xgb
from sklearn.multioutput import MultiOutputClassifier
import matplotlib.pyplot as plt
from joblib import load
# -----------------------------------------------------------------------------------------------------------#


# ------------------------------------------------ preprocessor ---------------------------------------------#
BASIC_SRATE = 500
def get_points(df_raw):
        ecg_signal=nk.ecg_clean(df_raw,sampling_rate=BASIC_SRATE)
        rpeaks = nk.ecg_peaks(ecg_signal, correct_artifacts=True, sampling_rate=BASIC_SRATE)[1]["ECG_R_Peaks"].tolist()
        waves_dwt = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=BASIC_SRATE, method="dwt")[1]
        # print(waves_dwt)
        points = dict()
        for key in waves_dwt.keys():
            points[key] = [i for i in waves_dwt[key] if math.isnan(i) != True]
            points['ECG_R_Peaks'] = rpeaks
        points['Heart_Rate'] = nk.ecg_rate(rpeaks,sampling_rate=BASIC_SRATE)
        return points,ecg_signal
# -----------------------------------------------------------------------------------------------------------#

# -------------------------------------------------- predictor ----------------------------------------------#
loaded_model = load('xgb_ECG.joblib')
def infer(input_signal):
    #sanity check
    if len(input_signal!=5000):
        raise Exception('Input sinal duration != 10s and/or sampling rate != 500Hz')

    #preprocess
    points,ecg_signal = get_points(input_signal)
    dataDict = {k:[] for k in ["P_val","T_val","R_val","R_std","P_dur","T_dur","QRS_Complex","PR_itvl","ST_itvl","QT_itvl","QRS_perd","Heart_Rate"]}
    dataDict["P_Value"].append(np.mean([ecg_signal[i] for i in points['ECG_P_Peaks']]))
    dataDict["T_Value"].append(np.mean([ecg_signal[i] for i in points['ECG_T_Peaks']]))
    dataDict["R_Value"].append(np.mean([ecg_signal[i] for i in points['ECG_R_Peaks']]))
    dataDict["R_Volatility"].append(np.std([ecg_signal[i] for i in points['ECG_R_Peaks']]))
    dataDict["P_Duration"].append(np.mean([(i[0]-i[-1])*0.002 for i in zip(points['ECG_P_Offsets'],points['ECG_P_Onsets'])]))
    dataDict["T_Duration"].append(np.mean([(i[0]-i[-1])*0.002 for i in zip(points['ECG_T_Offsets'],points['ECG_T_Onsets'])]))
    dataDict["QRS_Complex"].append(np.mean([(i[0]-i[-1])*0.002 for i in zip(points['ECG_R_Offsets'],points['ECG_R_Onsets'])]))
    dataDict["PR_Iterval"].append(np.mean([(i[0]-i[-1])*0.002 for i in zip(points['ECG_R_Onsets'],points['ECG_P_Onsets'])]))
    dataDict["ST_Iterval"].append(np.mean([(i[0]-i[-1])*0.002 for i in zip(points['ECG_T_Onsets'],points['ECG_R_Offsets'])]))
    dataDict["QT_Iterval"].append(np.mean([(i[0]-i[-1])*0.002 for i in zip(points['ECG_T_Offsets'],points['ECG_R_Onsets'])]))
    dataDict["QRS_Period"].append(np.mean([(points["ECG_R_Peaks"][i]-points["ECG_R_Peaks"][i-1])*0.002 for i in range(1,len(points['ECG_R_Peaks']))]))
    dataDict["Heart_Rate"].append(np.mean(points['Heart_Rate']))

    #inference
    test_array=np.array([i[0] for i in dataDict.values()]).reshape(1,-1)
    results = loaded_model.predict(test_array)[0]
    labels=["Arrhythmic_Beat","Structural_Condition","Secondary_Causality","Uncharacterised_Anomaly"]
    temp=' '.join([l*i for l,i in zip(labels,results)])
    if temp.strip().split(' ')==['']:
        suggestion="Cheers to a healthy heart!"
    elif len(temp.strip().split(' '))==1:
        suggestion="Try to be less stressed and care for your health."
    elif len(temp.strip().split(' '))==2:
        suggestion="Perhaps start looking for a professional opinion."
    else:
        suggestion="Seek help immediately!"

    #response
    data_=json.dumps({"ECG": ecg_signal, 'Stats':dataDict, "Diagnosis":{"Abnormalities":temp.strip(), "Remarks":suggestion}}, indent=4)
    # print(data_)
    return data_
# -----------------------------------------------------------------------------------------------------------#

app = FastAPI()

@app.get("/diagnose/")
async def diagnose(input_data: ECG):
    # Endpoint to handle the GET request and perform inference
    try:
        result = infer(input_data.ecg)
        return json.dumps({'status':200, 'response':result})
    except Exception as ex:
        return json.dumps({'status':404, 'response':str(ex)})
