import pandas as pd

# -------------------- Extract District Data  --------------------------
def get_dist_totals(FILES, KEEP, Out_path):

    records = []

    for district, file in FILES.items():

        df = pd.read_excel(file, usecols=KEEP + ["Level", "TRU", "Name"])

        lookup_name = {
            "Dehradun": "Dehradun",
            "Haridwar": "Hardwar",      # Official Census 2011 spelling
            "Pauri Garhwal": "Garhwal", # Official Census 2011 name
        }.get(district, district)

        district_rows = df[
            (df["Level"] == "DISTRICT")
            & (df["TRU"] == "Total")
            & (df["Name"].astype(str).str.strip() == lookup_name)
        ]

        if district_rows.empty:
            raise ValueError(f"District '{district}' not found in {file}")

        district_row = district_rows.iloc[0]

        total_pop = district_row["TOT_P"]

        records.append({
            "District": district,
            "Population": total_pop,
            "Households": district_row["No_HH"],
            "Literates": district_row["P_LIT"],
            "Illiterates": district_row["P_ILL"],
            "Workers": district_row["TOT_WORK_P"],
            "NonWorkers": district_row["NON_WORK_P"],
            "Children_0_6": district_row["P_06"],
            "SC_Population": district_row["P_SC"],
            "ST_Population": district_row["P_ST"],

            "LiteracyRate": round(district_row["P_LIT"] / total_pop * 100, 2),
            "WorkerRate": round(district_row["TOT_WORK_P"] / total_pop * 100, 2),
            "ChildRate": round(district_row["P_06"] / total_pop * 100, 2),
            "SC_Rate": round(district_row["P_SC"] / total_pop * 100, 2),
            "ST_Rate": round(district_row["P_ST"] / total_pop * 100, 2),
        })

    pda_summary = pd.DataFrame(records)
    pda_summary.to_csv(
        Out_path / "census_district_summary.csv",
        index=False,
    )

    print(pda_summary)
    return pda_summary

# -------------------- Extract HMIS Data  --------------------------

def get_hmis_data(FILES, KEEP, Out_path):
    records = []

    for district, file in FILES.items():
        df = pd.read_excel(file, header=None)

        district_record = {
            "District": district,
        }

        for search_text, column_name in KEEP.items():
            match = df[
                df[2]
                .astype(str)
                .str.contains(
                    search_text,
                    case=False,
                    na=False,
                    regex=False,
                )
            ]

            if len(match):
                district_record[column_name] = match.iloc[0, 4]

            else:
                district_record[column_name] = None

        records.append(district_record)

    hmis_summary = pd.DataFrame(records)
    hmis_summary.to_csv(
        Out_path / "hmis_district_summary.csv",
        index=False,
    )
    print(hmis_summary)
    return hmis_summary