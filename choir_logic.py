import pandas as pd
from database import connect_db
import streamlit as st
def load_full_dataset():
    conn = connect_db()

    choir = pd.read_sql("SELECT * FROM choir_data", conn)
    grad = pd.read_sql("SELECT * FROM graduation_data", conn)

    conn.close()

    choir["identification_no"] = choir["identification_no"].astype(str).str.strip()
    grad["identification_no"] = grad["identification_no"].astype(str).str.strip()

    choir = choir.drop_duplicates(subset=["identification_no"])

    grad["year_of_graduation"] = pd.to_numeric(grad["year_of_graduation"], errors="coerce")
    grad = grad.sort_values("year_of_graduation").drop_duplicates(
        subset=["identification_no"], keep="last"
    )

    # ✅ FIX: Only keep needed columns from grad to avoid name_x / name_y collision
    grad_cols = ["identification_no", "institute", "course_name", "year_of_graduation"]
    grad = grad[[c for c in grad_cols if c in grad.columns]]

    df = pd.merge(choir, grad, on="identification_no", how="left")

    required = ["name", "choir", "gender", "status", "institute", "course_name", "year_of_graduation","comment"]
    for col in required:
        if col not in df.columns:
            df[col] = None

    df["name"] = df["name"].fillna("Unknown")
    df["graduated"] = df["year_of_graduation"].notna()
    df["status"] = df["status"].fillna("alive")

    return df

