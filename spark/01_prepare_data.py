import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output paths
input_file = BASE_DIR / "data" / "raw" / "Online Retail.xlsx"
output_file = BASE_DIR / "data" / "processed" / "online_retail.csv"

# Read Excel dataset
print("Reading e-commerce dataset...")

df = pd.read_excel(input_file)

# Display basic information
print("\nDataset loaded successfully!")
print("Shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

# Save as CSV
df.to_csv(output_file, index=False)

print("\nCSV file created successfully!")
print("Saved at:", output_file)