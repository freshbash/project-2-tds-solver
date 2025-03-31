import pandas as pd
import re
from datetime import datetime

def q1(file):
    """Cleans, standardizes, filters, and computes the margin from a CSV sales dataset."""

    # Load CSV into DataFrame
    df = pd.read_excel(file, sheet_name="RawData" , dtype=str)

    # 1️⃣ Trim and Normalize Strings
    df["Customer Name"] = df["Customer Name"].str.strip()

    country_map = {
        "U.K":"UK",
        "US":"US",
        "IND":"IN",
        "United Arab Emirates":"AE",
        "IN":"IN",
        "U.S.A":"US",
        "India":"IN",
        "USA":"US",
        "U.A.E":"AE",
        "Brazil":"BR",
        "UAE":"AE",
        "AE":"AE",
        "Bra":"BR",
        "United States":"US",
        "United Kingdom":"UK",
        "UK":"UK",
        "France":"FR",
        "Fra":"FR",
        "FR":"FR",
        "BR":"BR"
    }

    df["Country"] = df["Country"].str.strip().replace(
        country_map
    )

    # 2️⃣ Standardize Date Formats
    def parse_date(date_str):
        for fmt in ("%m-%d-%Y", "%Y/%m/%d"):  # Handle multiple formats
            try:
                return datetime.strptime(date_str, fmt).isoformat()
            except ValueError:
                continue
        return None

    df["Date"] = df["Date"].apply(parse_date)

    # 3️⃣ Extract Product Name (Before "/")
    df["Product"] = df["Product/Code"].apply(lambda x: x.split("/")[0] if "/" in x else x)

    # 4️⃣ Clean and Convert Sales & Cost
    df["Sales"] = df["Sales"].str.replace("USD", "").str.strip().astype(float)
    df["Cost"] = df["Cost"].str.replace("USD", "").str.strip()
    
    # Fill missing cost values (50% of Sales)
    df["Cost"] = df["Cost"].apply(lambda x: float(x) if x else None)
    df["Cost"].fillna(df["Sales"] * 0.5, inplace=True)

    # 5️⃣ Filter Data (Before July 12, 2022, 13:15:29 IST & Product = Delta & Country = UK)
    cutoff_time = datetime(2022, 7, 12, 13, 15, 29)
    df = df[(df["Date"].apply(lambda x: datetime.fromisoformat(x) <= cutoff_time)) &
            (df["Product"] == "Delta") &
            (df["Country"] == "UK")]

    # 6️⃣ Compute Margin
    total_sales = df["Sales"].sum()
    total_cost = df["Cost"].sum()
    margin = ((total_sales - total_cost) / total_sales) * 100 if total_sales != 0 else 0

    return round(margin / 100, 2)
