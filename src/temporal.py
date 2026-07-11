from pathlib import Path

import pandas as pd

def load_statistics(csv_file):
    return pd.read_csv(csv_file)

def pivot_statistics(df):
    """
    Convert long-format stats into wide format
    """

    wide = (
        df.pivot_table(
            index=["district", "year"],
            columns="index",
            values="mean",
        )
        .reset_index()
    )

    wide.columns.name = None

    return wide

def calculate_changes(df):
    """
    Calculate year-to-year and overall changes.
    """

    records = []

    for district in df["district"].unique():

        district_df = (
            df[df["district"] == district]
            .sort_values("year")
        )

        row = {
            "district": district,
        }

        for index in ["NDVI", "NDWI", "NDBI"]:

            values = district_df[index].values

            row[f"{index}_2016"] = values[0]
            row[f"{index}_2022"] = values[1]
            row[f"{index}_2025"] = values[2]

            row[f"{index}_change_16_22"] = values[1] - values[0]
            row[f"{index}_change_22_25"] = values[2] - values[1]
            row[f"{index}_change_16_25"] = values[2] - values[0]

        records.append(row)

    return pd.DataFrame(records)

def export_temporal_summary(wide_df, change_df, output_dir):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    wide_df.to_csv(
        output_dir / "temporal_summary.csv",
        index=False,
    )

    change_df.to_csv(
        output_dir / "district_changes.csv",
        index=False,
    )


def calculate_percentage_changes(changes_df):
    """
    Calculate percentage change from 2016 to 2025.
    """
    df = changes_df.copy()

    #Percentage change for NDVI only
    df["NDVI_pct_change"] = (
        df["NDVI_change_16_25"]
        / df["NDVI_2016"]
    ) * 100

    return df

def rank_districts(change_df):
    """
    Rank districts based on environmental change.
    """

    rankings = {
        "ndvi_loss":
            change_df.sort_values(
                "NDVI_change_16_25"
            ),

        "ndvi_gain":
            change_df.sort_values(
                "NDVI_change_16_25",
                ascending=False
            ),

        "ndbi_increase":
            change_df.sort_values(
                "NDBI_change_16_25",
                ascending=False
            ),

        "ndwi_increase":
            change_df.sort_values(
                "NDWI_change_16_25",
                ascending = False,
            ),
    }

    return rankings

def export_rankings(rankings, output_dir):

    output_dir = Path(output_dir)

    for name, table in rankings.items():

        table.to_csv(
            output_dir / f"{name}.csv",
            index=False,
        )

def generate_summary(rankings):

    rows = []

    metrics = {
        "Largest NDVI Loss": ("ndvi_loss", "NDVI_change_16_25"),
        "Largest NDVI Gain": ("ndvi_gain", "NDVI_change_16_25"),
        "Largest NDBI Increase": ("ndbi_increase", "NDBI_change_16_25"),
        "Largest NDWI Increase": ("ndwi_increase", "NDWI_change_16_25"),
    }

    for label, (key, column) in metrics.items():
        top = rankings[key].iloc[0]

        rows.append({
            "Metric": label,
            "District": top["district"],
            "Value": top[column],
        })

    return pd.DataFrame(rows)


#Wrapper Function
def temporal_analysis(input_csv, output_dir):

    df = load_statistics(input_csv)
    wide = pivot_statistics(df)
    changes = calculate_changes(wide)
    changes = calculate_percentage_changes(changes)
    rankings = rank_districts(changes)
    summary = generate_summary(rankings)

    summary.to_csv(
    output_dir / "change_summary.csv",
    index=False,
    )
    
    export_temporal_summary(
        wide,
        changes,
        output_dir,
    )

    export_rankings(
        rankings,
        output_dir,
    )

    return wide, changes, rankings

