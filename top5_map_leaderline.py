import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_excel("data/lastRank.xlsx")
gdf = gpd.read_file("data/bnd_sigungu_00_2025_2Q.shp")

df["시군구"] = df["지역명"].str.split("_").str[-1]

gdf = gdf.merge(
    df,
    left_on="SIGUNGU_NM",
    right_on="시군구",
    how="left"
)

# 강원 고성군 제거 (32600), 경남 고성군 유지 (38540)
gdf.loc[
    gdf["SIGUNGU_CD"] == "32600",
    ["지역명","최종점수","최종순위",
     "소멸위험성_zscore","관광수요_zscore",
     "관광소비_zscore","빈집_zscore","숙박공급압박_zscore"]
] = np.nan

top20 = gdf[gdf["최종순위"] <= 20]
top5 = gdf[gdf["최종순위"] <= 5]
gosung = gdf[gdf["SIGUNGU_CD"] == "38540"]

fig, ax = plt.subplots(figsize=(7.2,9))

gdf.plot(ax=ax,color="#F6F7F2",edgecolor="#D9D9D9",linewidth=0.4)
top20.plot(ax=ax,color="#C8E6C9",edgecolor="#81C784",linewidth=0.8)
top5.plot(ax=ax,color="#2E7D32",edgecolor="white",linewidth=1.2)
gosung.plot(ax=ax,color="#8BC34A",edgecolor="#33691E",linewidth=2)

offsets = {
    "임실군": (-90000, 25000),
    "고성군": (85000, -55000),
    "군위군": (85000, 30000),
    "함양군": (-70000, -50000),
    "부안군": (-90000, 10000),
}

for _, row in top5.iterrows():
    p = row.geometry.representative_point()
    dx, dy = offsets.get(row["SIGUNGU_NM"], (50000,50000))
    ax.annotate(
        f"{int(row['최종순위'])}  {row['SIGUNGU_NM']}",
        xy=(p.x,p.y),
        xytext=(p.x+dx,p.y+dy),
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="center",
        bbox=dict(facecolor="white",edgecolor="none",alpha=0.9,pad=1.5),
        arrowprops=dict(
            arrowstyle="-",
            color="black",
            lw=1.2,
            shrinkA=5,
            shrinkB=5
        ),
        zorder=20
    )

p = gosung.geometry.representative_point().iloc[0]
ax.scatter(
    p.x,p.y,
    marker="*",
    s=260,
    color="gold",
    edgecolors="black",
    linewidth=1.2,
    zorder=30
)

legend = [
    Patch(facecolor="#C8E6C9",edgecolor="gray",label="1차 후보 20"),
    Patch(facecolor="#2E7D32",edgecolor="gray",label="최종 TOP5"),
    Patch(facecolor="#8BC34A",edgecolor="gray",label="대표 사례(경상남도 고성군)")
]

ax.legend(handles=legend,loc="lower left",fontsize=10,frameon=True)

ax.set_title("최종 TOP5 강조 지도",fontsize=18,fontweight="bold",pad=15)
ax.set_axis_off()
plt.tight_layout()
plt.show()
