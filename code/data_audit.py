import json
import pandas as pd

with open("wyndham_smartbin_filllevel.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("File loaded successfully!")
print("Number of records:", len(data["features"]))

#build data frame
records = []

for feature in data["features"]:
    properties = feature["properties"]
    coordinates = feature["geometry"]["coordinates"]

    record = properties.copy()
    record["longitude"] = coordinates[0]
    record["latitude"] = coordinates[1]

    records.append(record)

df = pd.DataFrame(records)

print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

df["timestamp"] = pd.to_datetime(df["timestamp"])

print("\nData types:")
print(df.dtypes)

missing_summary = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percent": (df.isnull().mean() * 100).round(2)
})

print(missing_summary)
print("Blank string check:")

for col in df.select_dtypes(include="str").columns:
    blank_count = (df[col].str.strip() == "").sum()
    print(f"{col}: {blank_count}")

duplicate_count = df.duplicated().sum()

print("Number of exact duplicate rows:", duplicate_count)
print("Duplicate percentage:",
      round((duplicate_count / len(df)) * 100, 2), "%")

duplicate_rows = df[df.duplicated(keep=False)].copy()

print("Total rows involved in duplicate groups:",
      len(duplicate_rows))

print("\nSample duplicate records:")

print(
    duplicate_rows
    .sort_values(["serialNumber", "timestamp"])
    .head(30)
    .to_string(index=False)
)

duplicate_group_sizes = (
    duplicate_rows
    .groupby(list(df.columns))
    .size()
    .value_counts()
    .sort_index()
)

print("\nDuplicate group sizes:")
print(duplicate_group_sizes)

duplicate_dates = (
    duplicate_rows
    .groupby("timestamp")
    .agg(
        rows_involved=("serialNumber", "size"),
        bins_affected=("serialNumber", "nunique")
    )
    .sort_values(
        ["bins_affected", "rows_involved"],
        ascending=False
    )
)

print(duplicate_dates.to_string())

df_raw = df.copy()
df_clean = df.drop_duplicates().copy()

print("Raw dataset rows:", len(df_raw))
print("Rows after removing exact duplicates:", len(df_clean))
print("Rows removed:", len(df_raw) - len(df_clean))

print("\nRemaining exact duplicates:")
print(df_clean.duplicated().sum())

bin_date_counts = (
    df_clean
    .groupby(["serialNumber", "timestamp"])
    .size()
    .reset_index(name="record_count")
)

multiple_bin_dates = bin_date_counts[
    bin_date_counts["record_count"] > 1
]

print("Number of bin-date combinations with multiple records:",
      len(multiple_bin_dates))

print("\nTotal records involved:")
print(multiple_bin_dates["record_count"].sum())

print("\nRecord-count distribution:")
print(
    multiple_bin_dates["record_count"]
    .value_counts()
    .sort_index()
)

problem_bin_dates = df_clean.merge(
    multiple_bin_dates[["serialNumber", "timestamp"]],
    on=["serialNumber", "timestamp"],
    how="inner"
)

print(
    problem_bin_dates
    .sort_values(["serialNumber", "timestamp", "latestFullness"])
    .to_string(index=False)
)

df_clean["ambiguous_bin_date"] = False

problem_keys = set(
    zip(
        multiple_bin_dates["serialNumber"],
        multiple_bin_dates["timestamp"]
    )
)

df_clean["ambiguous_bin_date"] = [
    (serial, date) in problem_keys
    for serial, date in zip(
        df_clean["serialNumber"],
        df_clean["timestamp"]
    )
]

print(df_clean["ambiguous_bin_date"].value_counts())

start_date = df_clean["timestamp"].min()
end_date = df_clean["timestamp"].max()

expected_dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

actual_dates = pd.DatetimeIndex(
    df_clean["timestamp"].unique()
)

missing_dates = expected_dates.difference(actual_dates)

print("Start date:", start_date)
print("End date:", end_date)

print("\nExpected calendar days:", len(expected_dates))
print("Observed unique dates:", len(actual_dates))
print("Missing calendar days:", len(missing_dates))

print("\nMissing dates:")
print(missing_dates)

coverage_results = []

for bin_id, group in df_clean.groupby("serialNumber"):

    first_date = group["timestamp"].min()
    last_date = group["timestamp"].max()

    expected_bin_dates = pd.date_range(
        start=first_date,
        end=last_date,
        freq="D"
    )

    actual_bin_dates = pd.DatetimeIndex(
        group["timestamp"].unique()
    )

    missing_bin_dates = expected_bin_dates.difference(
        actual_bin_dates
    )

    coverage_results.append({
        "serialNumber": bin_id,
        "first_date": first_date,
        "last_date": last_date,
        "records": len(group),
        "unique_dates": group["timestamp"].nunique(),
        "expected_days": len(expected_bin_dates),
        "missing_days": len(missing_bin_dates)
    })

coverage_df = pd.DataFrame(coverage_results)

print(coverage_df.to_string(index=False))

regular_bin_dates = pd.DatetimeIndex(
    df_clean[
        df_clean["serialNumber"] == 1511190
    ]["timestamp"].unique()
)

expected_full_range = pd.date_range(
    start=df_clean["timestamp"].min(),
    end=df_clean["timestamp"].max(),
    freq="D"
)

missing_regular_bin = expected_full_range.difference(
    regular_bin_dates
)

# Dates missing for this bin but NOT missing from the entire dataset
extra_missing_dates = missing_regular_bin.difference(
    missing_dates
)

print("Total missing days for bin 1511190:",
      len(missing_regular_bin))

print("Globally missing days:",
      len(missing_dates))

print("Additional missing dates for regular bin:",
      len(extra_missing_dates))

print("\nAdditional missing dates:")
print(extra_missing_dates)

print("Number of reporting bins on each additional missing date:\n")

for date in extra_missing_dates:
    bins_reporting = df_clean.loc[
        df_clean["timestamp"] == date,
        "serialNumber"
    ].nunique()

    reporting_ids = df_clean.loc[
        df_clean["timestamp"] == date,
        "serialNumber"
    ].unique()

    print(
        date.date(),
        "- bins reporting:", bins_reporting,
        "- IDs:", reporting_ids
    )

bin_consistency = (
    df_clean
    .groupby("serialNumber")
    .agg(
        descriptions=("description", "nunique"),
        positions=("position", "nunique"),
        ageThresholds=("ageThreshold", "nunique"),
        fullnessThresholds=("fullnessThreshold", "nunique"),
        longitudes=("longitude", "nunique"),
        latitudes=("latitude", "nunique")
    )
)

print(bin_consistency.to_string())

description_check = (
    df_clean
    .groupby("description")["serialNumber"]
    .nunique()
    .sort_values(ascending=False)
)

duplicate_descriptions = description_check[
    description_check > 1
]

print("Descriptions used by multiple serial numbers:")
print(duplicate_descriptions)
if len(duplicate_descriptions) > 0:

    affected_descriptions = duplicate_descriptions.index

    description_details = (
        df_clean[
            df_clean["description"].isin(affected_descriptions)
        ][
            ["serialNumber", "description",
             "longitude", "latitude",
             "fullnessThreshold"]
        ]
        .drop_duplicates()
        .sort_values(["description", "serialNumber"])
    )

    print("\nDetails:")
    print(description_details.to_string(index=False))

    bin_1192 = (
    df_clean[df_clean["serialNumber"] == 1511192]
    [["timestamp", "latestFullness"]]
    .rename(columns={"latestFullness": "fullness_1511192"})
)

bin_1212 = (
    df_clean[df_clean["serialNumber"] == 1511212]
    [["timestamp", "latestFullness"]]
    .rename(columns={"latestFullness": "fullness_1511212"})
)

comparison = bin_1192.merge(
    bin_1212,
    on="timestamp",
    how="inner"
)

comparison["same_fullness"] = (
    comparison["fullness_1511192"] ==
    comparison["fullness_1511212"]
)

print("Dates compared:", len(comparison))
print("Same fullness:", comparison["same_fullness"].sum())
print("Different fullness:", (~comparison["same_fullness"]).sum())

print(
    "Percentage identical:",
    round(comparison["same_fullness"].mean() * 100, 2),
    "%"
)

print("\nExample dates where they differ:")
print(
    comparison[
        comparison["same_fullness"] == False
    ].head(10).to_string(index=False)
)

print("Longitude range:")
print("Min:", df_clean["longitude"].min())
print("Max:", df_clean["longitude"].max())

print("\nLatitude range:")
print("Min:", df_clean["latitude"].min())
print("Max:", df_clean["latitude"].max())

invalid_longitude = (
    (df_clean["longitude"] < -180) |
    (df_clean["longitude"] > 180)
).sum()

invalid_latitude = (
    (df_clean["latitude"] < -90) |
    (df_clean["latitude"] > 90)
).sum()

zero_coordinates = (
    (df_clean["longitude"] == 0) &
    (df_clean["latitude"] == 0)
).sum()

print("\nInvalid longitude records:", invalid_longitude)
print("Invalid latitude records:", invalid_latitude)
print("Zero-coordinate records:", zero_coordinates)

print("Unique fullness values:")
print(sorted(df_clean["latestFullness"].unique()))

print("\nFullness value counts:")
print(
    df_clean["latestFullness"]
    .value_counts()
    .sort_index()
)

print("\nMinimum fullness:",
      df_clean["latestFullness"].min())

print("Maximum fullness:",
      df_clean["latestFullness"].max())

expected_fullness_values = {0, 2, 4, 6, 8, 10}

unexpected_values = set(
    df_clean["latestFullness"].unique()
) - expected_fullness_values

print("\nUnexpected fullness values:",
      unexpected_values)

print("Unique reason values:")
print(df_clean["reason"].unique())

print("\nReason counts:")
print(df_clean["reason"].value_counts())

print("\nReason × Fullness:")
reason_fullness = pd.crosstab(
    df_clean["reason"],
    df_clean["latestFullness"]
)

print(reason_fullness)

threshold_check = (
    df_clean
    .groupby("fullnessThreshold")
    .agg(
        records=("serialNumber", "size"),
        bins=("serialNumber", "nunique"),
        min_fullness=("latestFullness", "min"),
        max_fullness=("latestFullness", "max")
    )
)

print(threshold_check)

print("\nRecords where fullness exceeds threshold:")

above_threshold = df_clean[
    df_clean["latestFullness"] >
    df_clean["fullnessThreshold"]
]

print("Count:", len(above_threshold))

print("\nFullness values above threshold:")
print(
    above_threshold[
        ["fullnessThreshold", "latestFullness"]
    ]
    .value_counts()
    .sort_index()
)

print("Position:")
print(df_clean["position"].value_counts(dropna=False))

print("\nAge Threshold:")
print(df_clean["ageThreshold"].value_counts(dropna=False))

print("\nNumber of unique values:")
print("position:", df_clean["position"].nunique())
print("ageThreshold:", df_clean["ageThreshold"].nunique())

transition_base = (
    df_clean[
        df_clean["ambiguous_bin_date"] == False
    ]
    .copy()
)

transition_base = transition_base.sort_values(
    ["serialNumber", "timestamp"]
)

transition_base["previous_date"] = (
    transition_base
    .groupby("serialNumber")["timestamp"]
    .shift(1)
)

transition_base["previous_fullness"] = (
    transition_base
    .groupby("serialNumber")["latestFullness"]
    .shift(1)
)

transition_base["days_between"] = (
    transition_base["timestamp"] -
    transition_base["previous_date"]
).dt.days

print("Rows in cleaned dataset:", len(df_clean))
print("Rows excluded as ambiguous:",
      df_clean["ambiguous_bin_date"].sum())

print("\nDays between consecutive observations:")
print(
    transition_base["days_between"]
    .value_counts()
    .sort_index()
    .to_string()
)

largest_gaps = transition_base[
    transition_base["days_between"] >= 20
][
    [
        "serialNumber",
        "previous_date",
        "timestamp",
        "days_between",
        "previous_fullness",
        "latestFullness"
    ]
].sort_values(
    "days_between",
    ascending=False
)

print(largest_gaps.to_string(index=False))

daily_transitions = transition_base[
    transition_base["days_between"] == 1
].copy()

daily_transitions["fullness_change"] = (
    daily_transitions["latestFullness"] -
    daily_transitions["previous_fullness"]
)

print("Number of valid one-day transitions:",
      len(daily_transitions))

print("\nDaily fullness changes:")
print(
    daily_transitions["fullness_change"]
    .value_counts()
    .sort_index()
)

print("\nTransition direction:")

print(
    "Increase:",
    (daily_transitions["fullness_change"] > 0).sum()
)

print(
    "No change:",
    (daily_transitions["fullness_change"] == 0).sum()
)

print(
    "Decrease:",
    (daily_transitions["fullness_change"] < 0).sum()
)

decreases = daily_transitions[
    daily_transitions["fullness_change"] < 0
]

decrease_patterns = (
    decreases
    .groupby(
        ["previous_fullness", "latestFullness"]
    )
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

print("Daily decrease patterns:")
print(decrease_patterns.to_string(index=False))

to_zero = daily_transitions[
    (daily_transitions["fullness_change"] < 0) &
    (daily_transitions["latestFullness"] == 0)
]

print("Number of decreases ending at zero:",
      len(to_zero))

print("\nReason recorded after decrease to zero:")
print(
    to_zero["reason"]
    .value_counts()
)

print("\nPrevious fullness × current reason:")
print(
    pd.crosstab(
        to_zero["previous_fullness"],
        to_zero["reason"]
    )
)

transition_by_bin = (
    daily_transitions
    .groupby("serialNumber")
    .agg(
        daily_transitions=("fullness_change", "size"),
        increases=("fullness_change", lambda x: (x > 0).sum()),
        unchanged=("fullness_change", lambda x: (x == 0).sum()),
        decreases=("fullness_change", lambda x: (x < 0).sum())
    )
)

transition_by_bin["decrease_pct"] = (
    transition_by_bin["decreases"] /
    transition_by_bin["daily_transitions"] * 100
).round(2)

transition_by_bin["increase_pct"] = (
    transition_by_bin["increases"] /
    transition_by_bin["daily_transitions"] * 100
).round(2)

print(
    transition_by_bin
    .sort_values("daily_transitions")
    .to_string()
)

bin_1511202 = df_clean[
    df_clean["serialNumber"] == 1511202
]

print("Bin 1511202 details:\n")

print("Description:")
print(bin_1511202["description"].unique())

print("\nFullness values:")
print(
    bin_1511202["latestFullness"]
    .value_counts()
    .sort_index()
)

print("\nReason values:")
print(
    bin_1511202["reason"]
    .value_counts()
)

print("\nFirst 10 observations:")
print(
    bin_1511202[
        ["timestamp", "latestFullness", "reason"]
    ]
    .sort_values("timestamp")
    .head(10)
    .to_string(index=False)
)

print("\nLast 10 observations:")
print(
    bin_1511202[
        ["timestamp", "latestFullness", "reason"]
    ]
    .sort_values("timestamp")
    .tail(10)
    .to_string(index=False)
)

bin_variation = (
    df_clean
    .groupby("serialNumber")
    .agg(
        fullness_levels=("latestFullness", "nunique"),
        min_fullness=("latestFullness", "min"),
        max_fullness=("latestFullness", "max"),
        reason_levels=("reason", "nunique")
    )
)

print(
    bin_variation
    .sort_values("fullness_levels")
    .to_string()
)

print("\nBins with only one fullness level:")
print(
    bin_variation[
        bin_variation["fullness_levels"] == 1
    ]
)

processed_df = df_clean.copy()

# Sort for easier time-series use
processed_df = processed_df.sort_values(
    ["serialNumber", "timestamp"]
).reset_index(drop=True)

# Export to CSV
processed_df.to_csv(
    "smart_bin_processed.csv",
    index=False
)

print("Processed dataset exported successfully!")
print("File: smart_bin_processed.csv")
print("Rows:", len(processed_df))
print("Columns:", len(processed_df.columns))

print("\nColumns:")
print(processed_df.columns.tolist())

# Read the processed CSV back in
check_df = pd.read_csv(
    "smart_bin_processed.csv"
)

print("File validation")
print("----------------")
print("Rows:", len(check_df))
print("Columns:", len(check_df.columns))

print("\nColumn names:")
print(check_df.columns.tolist())

print("\nExact duplicate rows:",
      check_df.duplicated().sum())

print("\nAmbiguous records:")
print(check_df["ambiguous_bin_date"].value_counts())

print("\nUnique bins:",
      check_df["serialNumber"].nunique())