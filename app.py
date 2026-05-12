
import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor

# =========================================
# PATHS
# =========================================
DATA_PATH = "base.csv"
DB_PATH = "database_clients.xlsx"

# =========================================
# LOAD MODELS
# =========================================
@st.cache_resource
def load_models():

    df = pd.read_csv(DATA_PATH, encoding="latin1").dropna()

    le_segment = LabelEncoder()
    df["SEGMENT"] = le_segment.fit_transform(df["SEGMENT"])

    features = [
        "CLT AGE",
        "CLT CATEGORIE",
        "SEGMENT",
        "CLT REV MENS NET",
        "MMM",
        "VOLUME DES REVENUS",
        "CREDIT CONSO",
        "CREDIT IMMO"
    ]

    X = df[features]
    y_class = df["CLASSE DE RISQUE"]
    y_reg = df["PRIME_ASSURANCE"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_scaled, y_class)

    reg = GradientBoostingRegressor(random_state=42)
    reg.fit(X_scaled, y_reg)

    return scaler, clf, reg, le_segment


scaler, clf, reg, le_segment = load_models()

# =========================================
# DATABASE
# =========================================
cols = [
    "Name",
    "CLT AGE",
    "CLT CATEGORIE",
    "SEGMENT",
    "CLT REV MENS NET",
    "MMM",
    "VOLUME DES REVENUS",
    "CREDIT CONSO",
    "CREDIT IMMO",
    "Risk",
    "Prime_ASSURANCE"
]

if os.path.exists(DB_PATH):
    db = pd.read_excel(DB_PATH)
else:
    db = pd.DataFrame(columns=cols)

# =========================================
# TITLE
# =========================================
st.markdown("## 👤 Client Prediction")

# =========================================
# INPUTS
# =========================================
name = st.text_input("Client Name")

age = st.number_input("CLT AGE", format="%.3f")
categorie = st.number_input("CLT CATEGORIE", format="%.3f")

segment = st.selectbox("SEGMENT", ["---SELECT---"] + list(le_segment.classes_))

income = st.number_input("CLT REV MENS NET", format="%.3f")
mmm = st.number_input("MMM", format="%.3f")
volume = st.number_input("VOLUME DES REVENUS", format="%.3f")
conso = st.number_input("CREDIT CONSO", format="%.3f")
immo = st.number_input("CREDIT IMMO", format="%.3f")

# =========================================
# PREDICT
# =========================================
if st.button("🚀 Predict"):

    if segment == "---SELECT---":
        st.warning("Select SEGMENT")
        st.stop()

    segment_encoded = le_segment.transform([segment])[0]

    X_input = np.array([[
        round(age, 3),
        round(categorie, 3),
        round(segment_encoded, 3),
        round(income, 3),
        round(mmm, 3),
        round(volume, 3),
        round(conso, 3),
        round(immo, 3)
    ]])

    X_scaled = scaler.transform(X_input)

    risk = clf.predict(X_scaled)[0]

    if risk == 1:
        status = "RISQUÉ"
        prime = 0.0
    else:
        status = "NON RISQUÉ"
        prime = float(reg.predict(X_scaled)[0])

    prime = round(prime, 3)

    st.success(f"Risk: {status}")
    st.info(f"Prime: {prime:.3f} DT")

    st.session_state.result = {
        "Risk": status,
        "Prime": prime,
        "SEGMENT": segment
    }

# =========================================
# SAVE CLIENT
# =========================================
if st.button("💾 Save Client"):

    if "result" not in st.session_state:
        st.warning("Predict first")
        st.stop()

    new_client = pd.DataFrame([{
        "Name": name,
        "CLT AGE": round(age, 3),
        "CLT CATEGORIE": round(categorie, 3),
        "SEGMENT": st.session_state.result["SEGMENT"],
        "CLT REV MENS NET": round(income, 3),
        "MMM": round(mmm, 3),
        "VOLUME DES REVENUS": round(volume, 3),
        "CREDIT CONSO": round(conso, 3),
        "CREDIT IMMO": round(immo, 3),
        "Risk": st.session_state.result["Risk"],
        "Prime_ASSURANCE": round(st.session_state.result["Prime"], 3)
    }])

    db = pd.concat([db, new_client], ignore_index=True)

    # =========================================
    # ROUND ALL NUMERIC COLUMNS TO 3 DECIMALS
    # =========================================
    numeric_cols = db.select_dtypes(include=[np.number]).columns
    db[numeric_cols] = db[numeric_cols].round(3)

    try:
        db.to_excel(DB_PATH, index=False)
        st.success("Client saved successfully ✅")

    except PermissionError:
        st.error("❌ Ferme database_clients.xlsx puis réessaie")


import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor

# =========================================
# PATHS
# =========================================
DATA_PATH = "base.csv"
DB_PATH = "database_clients.xlsx"

# =========================================
# LOAD MODELS
# =========================================
@st.cache_resource
def load_models():

    df = pd.read_csv(DATA_PATH, encoding="latin1").dropna()

    le_segment = LabelEncoder()
    df["SEGMENT"] = le_segment.fit_transform(df["SEGMENT"])

    features = [
        "CLT AGE",
        "CLT CATEGORIE",
        "SEGMENT",
        "CLT REV MENS NET",
        "MMM",
        "VOLUME DES REVENUS",
        "CREDIT CONSO",
        "CREDIT IMMO"
    ]

    X = df[features]
    y_class = df["CLASSE DE RISQUE"]
    y_reg = df["PRIME_ASSURANCE"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_scaled, y_class)

    reg = GradientBoostingRegressor(random_state=42)
    reg.fit(X_scaled, y_reg)

    return scaler, clf, reg, le_segment


scaler, clf, reg, le_segment = load_models()

# =========================================
# DATABASE
# =========================================
cols = [
    "Name",
    "CLT AGE",
    "CLT CATEGORIE",
    "SEGMENT",
    "CLT REV MENS NET",
    "MMM",
    "VOLUME DES REVENUS",
    "CREDIT CONSO",
    "CREDIT IMMO",
    "Risk",
    "Prime_ASSURANCE"
]

if os.path.exists(DB_PATH):
    db = pd.read_excel(DB_PATH)
else:
    db = pd.DataFrame(columns=cols)

# =========================================
# TITLE
# =========================================
st.markdown("## 👤 Client Prediction")

# =========================================
# INPUTS
# =========================================
name = st.text_input("Client Name")

age = st.number_input("CLT AGE", format="%.3f")
categorie = st.number_input("CLT CATEGORIE", format="%.3f")

segment = st.selectbox("SEGMENT", ["---SELECT---"] + list(le_segment.classes_))

income = st.number_input("CLT REV MENS NET", format="%.3f")
mmm = st.number_input("MMM", format="%.3f")
volume = st.number_input("VOLUME DES REVENUS", format="%.3f")
conso = st.number_input("CREDIT CONSO", format="%.3f")
immo = st.number_input("CREDIT IMMO", format="%.3f")

# =========================================
# PREDICT
# =========================================
if st.button("🚀 Predict"):

    if segment == "---SELECT---":
        st.warning("Select SEGMENT")
        st.stop()

    segment_encoded = le_segment.transform([segment])[0]

    X_input = np.array([[
        round(age, 3),
        round(categorie, 3),
        round(segment_encoded, 3),
        round(income, 3),
        round(mmm, 3),
        round(volume, 3),
        round(conso, 3),
        round(immo, 3)
    ]])

    X_scaled = scaler.transform(X_input)

    risk = clf.predict(X_scaled)[0]

    if risk == 1:
        status = "RISQUÉ"
        prime = 0.0
    else:
        status = "NON RISQUÉ"
        prime = float(reg.predict(X_scaled)[0])

    prime = round(prime, 3)

    st.success(f"Risk: {status}")
    st.info(f"Prime: {prime:.3f} DT")

    st.session_state.result = {
        "Risk": status,
        "Prime": prime,
        "SEGMENT": segment
    }

# =========================================
# SAVE CLIENT
# =========================================
if st.button("💾 Save Client"):

    if "result" not in st.session_state:
        st.warning("Predict first")
        st.stop()

    new_client = pd.DataFrame([{
        "Name": name,
        "CLT AGE": round(age, 3),
        "CLT CATEGORIE": round(categorie, 3),
        "SEGMENT": st.session_state.result["SEGMENT"],
        "CLT REV MENS NET": round(income, 3),
        "MMM": round(mmm, 3),
        "VOLUME DES REVENUS": round(volume, 3),
        "CREDIT CONSO": round(conso, 3),
        "CREDIT IMMO": round(immo, 3),
        "Risk": st.session_state.result["Risk"],
        "Prime_ASSURANCE": round(st.session_state.result["Prime"], 3)
    }])

    db = pd.concat([db, new_client], ignore_index=True)

    # =========================================
    # ROUND ALL NUMERIC COLUMNS TO 3 DECIMALS
    # =========================================
    numeric_cols = db.select_dtypes(include=[np.number]).columns
    db[numeric_cols] = db[numeric_cols].round(3)

    try:
        db.to_excel(DB_PATH, index=False)
        st.success("Client saved successfully ✅")

    except PermissionError:
        st.error("❌ Ferme database_clients.xlsx puis réessaie")

>>>>>>> d74a033c361b4fd6aa65ace6aaf0124e1151d0de
