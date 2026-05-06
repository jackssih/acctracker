import pandas as pd
from database import connect_db
import uuid


# ---------------- ID GENERATOR ----------------
def generate_id():
    return str(uuid.uuid4()).replace("-", "")[:8].upper()


# ---------------- GRADUATION UPLOAD ----------------
def upload_graduation_data(file):
    conn = connect_db()

    try:
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file, encoding="utf-8")

        df.columns = df.columns.str.strip().str.lower()

        # REQUIRED
        if "identification_no" not in df.columns:
            raise ValueError("Graduation file MUST have identification_no")

        if "year_of_graduation" not in df.columns:
            raise ValueError("Missing year_of_graduation")

        df["identification_no"] = df["identification_no"].astype(str).str.strip()
        df["year_of_graduation"] = pd.to_numeric(df["year_of_graduation"], errors="coerce")

        df = df.dropna(subset=["identification_no"])

        df = df.drop_duplicates(subset=["identification_no"], keep="last")

        existing = pd.read_sql("SELECT identification_no FROM graduation_data", conn)
        existing_ids = existing["identification_no"].astype(str).str.strip()

        df = df[~df["identification_no"].isin(existing_ids)]
        # After cleaning, before to_sql:
        df = df.drop(columns=["name"], errors="ignore")
        df.to_sql("graduation_data", conn, if_exists="append", index=False)
        df.to_sql("graduation_data", conn, if_exists="append", index=False)

        print(f"Uploaded {len(df)} graduation records")

    except Exception as e:
        print("GRAD UPLOAD ERROR:", e)

    finally:
        conn.close()

# ---------------- CHOIR UPLOAD ----------------
def upload_choir_data(file):
    conn = connect_db()

    try:
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file, encoding="utf-8", error_bad_lines=False)

        # CLEAN COLUMN NAMES FIRST (VERY IMPORTANT)
        df.columns = df.columns.str.strip().str.lower()

        # STANDARDIZE NAMES BEFORE ANYTHING ELSE
        df = df.rename(columns={
            "full name": "name",
            "student_name": "name",
            "student id": "identification_no",
            "id": "identification_no",
            "choir name": "choir"
        })

        # FORCE REQUIRED FIELDS
        if "name" not in df.columns:
            raise ValueError("Missing name column in upload file")

        if "choir" not in df.columns:
            raise ValueError("Missing choir column in upload file")

        # CLEAN VALUES BEFORE ID GENERATION
        df["name"] = df["name"].astype(str).str.strip()
        df["choir"] = df["choir"].astype(str).str.strip()

        # DROP BAD ROWS (CRITICAL FIX)
        df = df.dropna(subset=["name", "choir"])
        df = df[df["name"] != ""]
        df = df[df["name"].str.lower() != "none"]

        # ENSURE ID COLUMN
        if "identification_no" not in df.columns:
            df["identification_no"] = None

        # GENERATE IDS
        df["identification_no"] = df["identification_no"].apply(
            lambda x: x if pd.notna(x) and str(x).strip() != "" else generate_id()
        )

        df["status"] = "alive"

        # FINAL CLEAN
        df = df[["identification_no", "name", "choir", "gender", "status"]]

        # INSERT
        df.to_sql("choir_data", conn, if_exists="append", index=False)

        print(f"Uploaded {len(df)} students")

    except Exception as e:
        print("UPLOAD ERROR:", e)

    finally:
        conn.close()