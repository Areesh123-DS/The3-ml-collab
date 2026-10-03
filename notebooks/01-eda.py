# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] deletable=true editable=true slideshow={"slide_type": ""}
# # 01  Exploratory Data Analysis: California Housing
#
# Explore the raw dataset tracked by DVC ('data/raw/california_housing.csv')
# Target: 'MedHouseVal', the median house value in units of $100,000
# 'add_bedroom_ratio' lives in 'src/features.py' (unit-tested in 'tests/') so the
# training pipeline can reuse it. It is a row-wise ratio, so it causes no data leakage.

# %%
import matplotlib.pyplot as plt
import pandas as pd

from src.config import RAW_DATA_DIR
from src.features import add_bedroom_ratio

TARGET = "MedHouseVal"

# %%
df = pd.read_csv(RAW_DATA_DIR / "california_housing.csv")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
df.head()

# %%
df.info()
df.describe().transpose()

# %%
print("Missing values per column:")
print(df.isna().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# %%
cap = df[TARGET].max()
n_capped = (df[TARGET] == cap).sum()
print(f"Max target value: {cap}")
print(f"Rows at the cap: {n_capped} ({n_capped / len(df):.1%})")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df[TARGET], bins=50, edgecolor="black")
ax.axvline(cap, color="red", linestyle="--", label=f"cap = {cap}")
ax.set_xlabel("MedHouseVal ($100k)")
ax.set_ylabel("Count")
ax.set_title("Distribution of median house value")
ax.legend()
plt.show()

# %%
df.drop(columns=TARGET).hist(bins=50, figsize=(14, 10), edgecolor="black")
plt.suptitle("Feature distributions")
plt.tight_layout()
plt.show()

# %%
outlier_cols = ["AveRooms", "AveBedrms", "AveOccup", "Population"]

fig, axes = plt.subplots(1, len(outlier_cols), figsize=(16, 4))
for ax, col in zip(axes, outlier_cols):
    ax.boxplot(df[col])
    ax.set_title(col)
plt.suptitle("Features with extreme values")
plt.tight_layout()
plt.show()

df[outlier_cols].quantile([0.5, 0.99, 1.0])

# %%
df.corr()[TARGET].drop(TARGET).sort_values(ascending=False)

# %%
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df["MedInc"], df[TARGET], s=3, alpha=0.3)
ax.set_xlabel("MedInc (median income, $10k)")
ax.set_ylabel("MedHouseVal ($100k)")
ax.set_title("Median income vs. house value")
plt.show()

# %%
fig, ax = plt.subplots(figsize=(8, 7))
sc = ax.scatter(df["Longitude"], df["Latitude"], c=df[TARGET], cmap="viridis", s=3, alpha=0.5)
fig.colorbar(sc, ax=ax, label="MedHouseVal ($100k)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("House value by location")
plt.show()

# %%
df_feat = add_bedroom_ratio(df)
print(df_feat["BedroomRatio"].describe())
print(f"\nCorrelation with target: {df_feat['BedroomRatio'].corr(df_feat[TARGET]):.3f}")

# %%
corr = df.corr()
fig, ax = plt.subplots(figsize=(9, 7))
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
ax.set_yticks(range(len(corr.columns)), corr.columns)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
fig.colorbar(im, ax=ax)
ax.set_title("Correlation matrix")
plt.tight_layout()
plt.show()
