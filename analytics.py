def choir_summary(df):
    summary = df.groupby("choir").agg(
        total_students=("identification_no", "count"),
        graduated=("graduation_status", lambda x: (x == "graduated").sum()),
    ).reset_index()

    summary["not_graduated"] = summary["total_students"] - summary["graduated"]

    summary["success_rate"] = (
        summary["graduated"] / summary["total_students"] * 100
    )

    return summary
