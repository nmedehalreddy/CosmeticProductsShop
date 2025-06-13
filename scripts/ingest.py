import pandas as pd
import os

def load_opencorporates():
    url = "https://example.com/opencorp-dataset.csv"
    df = pd.read_csv(url)
    df = df.dropna(subset=["name", "country"])
    df["name"] = df["name"].str.strip()
    return df

def save_clean_data(df, name):
    os.makedirs("data/clean", exist_ok=True)
    df.to_csv(f"data/clean/{name}.csv", index=False)

if __name__ == "__main__":
    df = load_opencorporates()
    save_clean_data(df, "opencorporates")
