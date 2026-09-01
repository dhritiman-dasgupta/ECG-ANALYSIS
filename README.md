# ECG-ANALYSIS

**A three-lead ECG telemetry platform on Azure.** A wearable streams samples into IoT Hub, a
Stream Analytics job lands them in Azure SQL, a Django CRM gives a clinician a per-patient
view of every scan, and an XGBoost service turns a ten-second trace into interval
measurements and a screening flag. A React Native app is the patient-facing end.

![Azure IoT Hub](https://img.shields.io/badge/Azure-IoT%20Hub%20%C2%B7%20Stream%20Analytics%20%C2%B7%20SQL-0078D4?logo=microsoftazure&logoColor=white)
![Django 4.1](https://img.shields.io/badge/Django-4.1-092E20?logo=django&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-inference-009688?logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/model-XGBoost%20multi--output-EB5B25)
![Expo / React Native](https://img.shields.io/badge/Expo-React%20Native%200.70-000020?logo=expo&logoColor=white)
![License MIT](https://img.shields.io/badge/license-MIT-7AA116)

<p align="center">
  <img src="https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/c89f0c00-556c-4abd-9894-76676cf86900" alt="Architecture: five wearable devices (MC01–MC05) publish to Azure IoT Hub; a Stream Analytics job reads from the hub and writes to Azure SQL Server; an Azure VM hosts the Django CRM for doctors and patients and serves the React Native mobile app; a machine-learning diagnosis engine sits alongside the VM." width="100%">
</p>

---

## What this is

The interesting part of a remote-monitoring system is not the model at the end of it. It is
the seam between a battery-powered sensor that speaks in short bursts and a clinician who
needs a patient record that is always there. This repository is one end-to-end pass at that
seam, built on managed Azure services so that the only code that has to exist is the code at
the edges: what the device sends, what the clinician sees, and what the model decides.

Three design choices shape it:

- **The ingest path holds no application code.** Devices publish to IoT Hub; a Stream
  Analytics job moves rows into Azure SQL. Adding a device is a hub registration, not a
  deployment, and the sample rows carry `EventProcessedUtcTime` from Stream Analytics rather
  than a device clock — so the record's ordering does not depend on the wearable's sense of
  time.
- **The clinician view is the Django admin, deliberately.** For a caseload of a few dozen
  patients, the admin already gives search, filtering, per-patient inlines and authentication.
  `PatientAdmin` lists a patient's scans inline and links through to their raw traces
  (`analysis/admin.py:13-22`); the scans themselves are read-only in the UI, because a
  telemetry record should not be editable by hand.
- **Analysis works on features, not raw waveform.** The service does not feed 5,000 samples to
  a network. It delineates the beat first — R-peaks, then P/QRS/T onsets and offsets — and
  classifies twelve clinical measurements. That keeps the model small, and it means every
  input to a prediction is a quantity a cardiologist already reads off a strip.

## Status

Built in **January 2024** as a student project on an *Azure for Students* subscription. The
cloud resources behind it have since been torn down, so this is a reference architecture and a
record of how the pieces fit — not a running service.

Read it with three things in mind:

- **This is not a medical device** and nothing in it has been clinically validated. The
  classifier's output is a screening signal in a coursework project, not a diagnosis.
- **There are no measured numbers in this repository** — no latency, throughput or accuracy
  figures — and none are claimed. The model was trained elsewhere and only the serialised
  artefact (`Api_For_12_Lead_Conversion/xgb_ECG.joblib`) is committed, with no training script,
  dataset reference or evaluation to go with it.
- **The committed configuration is a development scaffold**, not the deployed one. The Django
  project points at local SQLite with `DEBUG = True`; in the deployed system the CRM read from
  Azure SQL.

## How the data flows

| # | Stage | Where it lives | What it does |
|---|---|---|---|
| 1 | Device | `IoT Device/Sample_Code_To_Send_Data.py` | Publishes `{"device_id", "data": [(index, mV), ...]}` to IoT Hub over the `azure-iot-device` SDK. |
| 2 | Ingest | Azure IoT Hub | Per-device identity and auth; no application code. |
| 3 | Transform | Azure Stream Analytics | Reads the hub, writes rows into Azure SQL, stamping `EventProcessedUtcTime`. |
| 4 | Store | Azure SQL | One row per scan: device, JSON sample block, processed-at time. |
| 5 | Clinical view | `CRM_ECG_DATA _ANALYSIS/` | Django 4.1 CRM — patients, devices, and their scans. |
| 6 | Analysis | `Api_For_12_Lead_Conversion/` | FastAPI service: delineate the beat, extract twelve measurements, classify. |
| 7 | Patient app | `ecg-app-final/` | Expo / React Native app charting a patient's own statistics. |

## Repository layout

```
IoT Device/                     Reference publisher for the wearable (Python, azure-iot-device)
CRM_ECG_DATA _ANALYSIS/
  ecgappcrm/
    analysis/                   Patient · Device · ecgdata models, admin-driven clinician UI
    ecgappcrm/                  Django project settings and URLs
Api_For_12_Lead_Conversion/
  api.py                        FastAPI /diagnose endpoint — delineation, features, inference
  xgb_ECG.joblib                Serialised XGBoost multi-output classifier
ecg-app-final/                  Expo / React Native patient app (drawer nav, chart-kit graphs)
```

## The data model

Three tables carry the whole system (`analysis/models.py`):

- **`Patient`** — patient ID, name, contact, age, and the `device_id` they were issued.
- **`Device`** — the device-to-patient assignment, so a returned unit can be reissued.
- **`ecgdata`** — one scan: a foreign key to the patient, the originating `device_id`, the raw
  samples as a `JSONField`, and `EventProcessedUtcTime`.

The `device_id` appears on both `Patient` and `ecgdata`. That is deliberate rather than
redundant: telemetry arrives keyed only by device, so a scan has to be storable before it is
attributed, and `ecgdata` keeps the device that actually produced it even if the assignment
later changes.

## The analysis service

`Api_For_12_Lead_Conversion/api.py` exposes `/diagnose`, taking a ten-second single-lead trace
at 500 Hz (5,000 samples). It:

1. Cleans the signal and detects R-peaks with **neurokit2**, correcting artifacts
   (`api.py:26-27`).
2. Delineates P, QRS and T onsets and offsets by discrete wavelet transform (`api.py:28`).
3. Derives twelve features — P/T/R amplitudes, R-wave volatility, P and T durations, QRS
   complex width, PR / ST / QT intervals, R-R period and heart rate (`api.py:47-59`).
4. Runs an XGBoost multi-output classifier over those twelve values, returning four
   independent flags: `Arrhythmic_Beat`, `Structural_Condition`, `Secondary_Causality`,
   `Uncharacterised_Anomaly` (`api.py:63-64`).

**A naming caveat, stated plainly.** The directory is called `Api_For_12_Lead_Conversion`
after the project's original goal — reconstructing a twelve-lead ECG from three leads. The
code that is actually committed does not do lead reconstruction; it is the morphology-feature
classifier described above. The directory name has been left as it is so that it matches the
project write-up, but the README should not be read as claiming a capability the code does not
contain.

## Known limitations

Listed rather than buried, because they are the honest state of a two-week build:

- **The analysis service is not runnable as committed.** It has no `requirements.txt` and no
  container, loads its model by relative path, and has defects in the request path — a missing
  `typing.List` import, a feature-dictionary key mismatch between where keys are declared and
  where they are written, and a length check whose parentheses put the comparison inside
  `len()`. It reads as reference code for the pipeline shape, not as a service.
- **No model provenance.** No training script, dataset citation, class balance or evaluation
  accompanies `xgb_ECG.joblib`, so its output cannot be assessed by a reader.
- **No non-admin web UI.** `analysis/views.py` is the generated stub and `urls.py` routes only
  `/admin/`. Everything a clinician does happens through the Django admin.
- **The mobile app has no live backend.** `App.js:144` fetches `/statistics` from a hardcoded
  ngrok tunnel that expired in 2024; the API base needs to be a configured value.
- **No tests.** `analysis/tests.py` is the Django stub.
- **The device sample is a publisher, not firmware.** It sends one hardcoded message; the real
  wearable's acquisition and framing code is not in this repository.

## Running it

There is no one-command bring-up, and reproducing the original deployment means standing up
the Azure side yourself:

1. **Azure** — an IoT Hub, a Stream Analytics job with the hub as input and Azure SQL as
   output, the SQL database, and a VM to host the CRM.
2. **Device** — register a device on the hub and export its connection string as
   `IOTHUB_DEVICE_CONNECTION_STRING`, then run `IoT Device/Sample_Code_To_Send_Data.py`.
3. **CRM** — from `CRM_ECG_DATA _ANALYSIS/ecgappcrm/`: `python manage.py migrate`,
   `python manage.py createsuperuser`, `python manage.py runserver`, then `/admin/`. Point
   `DATABASES` at Azure SQL and set `DEBUG = False`, `ALLOWED_HOSTS` and a fresh `SECRET_KEY`
   from the environment before exposing it.
4. **Analysis service** — `uvicorn api:app` from `Api_For_12_Lead_Conversion/`, after
   installing `fastapi`, `neurokit2`, `xgboost`, `scikit-learn`, `pandas` and `joblib`, and
   addressing the defects listed above.
5. **Mobile app** — `npm install && npx expo start` in `ecg-app-final/`, with the API base
   pointed at your own host.

## Deployment, as it was

<p align="center">
  <img src="https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/0c7e7866-1637-499e-95bc-4dd533d2e921" alt="Azure portal showing the ECG_DATA_ANALYSIS_HEALTH_HACTIVISTS resource group in East US with eleven resources: an IoT Hub, a Stream Analytics job, a SQL server and database, and the virtual machine, disk, network interface, virtual network, public IP, network security group and SSH key that host the CRM." width="100%">
</p>

<p align="center">
  <img src="https://github.com/dhritiman-dasgupta/ECG-ANALYSIS/assets/84367714/643d09c8-ee3c-493c-8022-78cde130505c" alt="Three photographs of the hand-built acquisition device — a perfboard prototype with a colour TFT display and three buttons — showing it joining Wi-Fi, reporting CONNECTED, and then offering its three modes: ECG continuous monitor, ECG store monitor, and pulse monitor." width="100%">
  <br><em>The acquisition device: a perfboard prototype that joins Wi-Fi, then publishes three-lead ECG over MQTT to IoT Hub.</em>
</p>

## License

MIT — see [LICENSE](LICENSE).
