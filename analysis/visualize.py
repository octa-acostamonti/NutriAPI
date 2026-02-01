import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_FILE = PROJECT_DIR / "enriched_products.json"
OUTPUT_DIR = SCRIPT_DIR / "plots"

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["price_per_100g"] = (df["price"] / df["product_quantity_g"]) * 100
    df["protein_per_peso"] = df["proteina_g_100g"] / df["price_per_100g"]
    df["calories_per_peso"] = df["caloria_kcal_100g"] / df["price_per_100g"]
    df["main_category"] = df["category"].str.split("/").str[0]
    return df


def plot_nutriscore_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scores = df["nutriscore_grade"].value_counts()
    order = ["a", "b", "c", "d", "e", "unknown", "not-applicable"]
    scores = scores.reindex([s for s in order if s in scores.index])
    
    colors = {"a": "#038141", "b": "#85BB2F", "c": "#FECB02", "d": "#EE8100", "e": "#E63E11", 
              "unknown": "#999999", "not-applicable": "#CCCCCC"}
    bar_colors = [colors.get(s, "#999999") for s in scores.index]
    
    bars = ax.bar(scores.index, scores.values, color=bar_colors, edgecolor='white', linewidth=1.5)
    
    for bar, val in zip(bars, scores.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, f'{val:,}', 
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel("Nutri-Score", fontsize=12)
    ax.set_ylabel("Number of Products", fontsize=12)
    ax.set_title("Nutri-Score Distribution\n(A=Best, E=Worst)", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "nutriscore_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: nutriscore_distribution.png")


def plot_nova_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    nova_data = df["nova_group"].dropna().astype(int).value_counts().sort_index()
    labels = {1: "1: Unprocessed", 2: "2: Culinary", 3: "3: Processed", 4: "4: Ultra-processed"}
    colors = ["#2E7D32", "#7CB342", "#FBC02D", "#D32F2F"]
    
    bars = ax.bar([labels.get(i, str(i)) for i in nova_data.index], nova_data.values, color=colors)
    
    for bar, val in zip(bars, nova_data.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{val:,}', 
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel("NOVA Group", fontsize=12)
    ax.set_ylabel("Number of Products", fontsize=12)
    ax.set_title("NOVA Food Processing Classification\n(1=Least processed, 4=Ultra-processed)", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "nova_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: nova_distribution.png")


def plot_price_by_retailer(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    valid = df[(df["price"] > 0) & (df["product_quantity_g"] > 0)].copy()
    ean_counts = valid.groupby("ean").size()
    multi_eans = ean_counts[ean_counts > 1].index
    multi = valid[valid["ean"].isin(multi_eans)]
    
    avg_prices = multi.groupby("retailer")["price_per_100g"].mean().sort_values()
    
    colors = ["#1976D2", "#388E3C", "#F57C00", "#7B1FA2"]
    bars = ax.barh(avg_prices.index, avg_prices.values, color=colors)
    
    for bar, val in zip(bars, avg_prices.values):
        ax.text(val + 30, bar.get_y() + bar.get_height()/2, f'${val:,.0f}', 
                ha='left', va='center', fontweight='bold')
    
    ax.set_xlabel("Average Price per 100g ($)", fontsize=12)
    ax.set_ylabel("Retailer", fontsize=12)
    ax.set_title("Average Price per 100g by Retailer\n(Products available in multiple stores)", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "price_by_retailer.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: price_by_retailer.png")


def plot_cheapest_retailer_wins(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    valid = df[(df["price"] > 0) & (df["product_quantity_g"] > 0)].copy()
    ean_counts = valid.groupby("ean").size()
    multi_eans = ean_counts[ean_counts > 1].index
    multi = valid[valid["ean"].isin(multi_eans)]
    
    cheapest = multi.loc[multi.groupby("ean")["price"].idxmin()]
    wins = cheapest["retailer"].value_counts()
    
    colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0"]
    explode = [0.05 if i == 0 else 0 for i in range(len(wins))]
    
    wedges, texts, autotexts = ax.pie(wins.values, labels=wins.index, autopct='%1.1f%%', 
                                       colors=colors, explode=explode, startangle=90)
    
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    
    ax.set_title("Which Retailer Has the Lowest Price?\n(For products in multiple stores)", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "cheapest_retailer.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: cheapest_retailer.png")


def plot_top_protein_value(df):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    valid = df[(df["price"] > 0) & (df["product_quantity_g"] > 0) & (df["proteina_g_100g"].notna())].copy()
    valid = valid.drop_duplicates(subset=["ean"], keep="first")
    top = valid.nlargest(15, "protein_per_peso")
    
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(top)))[::-1]
    
    y_pos = range(len(top))
    bars = ax.barh(y_pos, top["protein_per_peso"].values, color=colors)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([name[:40] for name in top["product_name"].values])
    
    for bar, val, prot in zip(bars, top["protein_per_peso"].values, top["proteina_g_100g"].values):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{val:.3f} g/$ ({prot:.1f}g prot/100g)', 
                ha='left', va='center', fontsize=9)
    
    ax.set_xlabel("Grams of Protein per Peso", fontsize=12)
    ax.set_title("Best Value Protein Sources\n(Most protein per peso spent)", fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_protein_value.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: top_protein_value.png")


def plot_category_prices(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    valid = df[(df["price"] > 0) & (df["product_quantity_g"] > 0)].copy()
    valid = valid.drop_duplicates(subset=["ean"], keep="first")
    
    cat_stats = valid.groupby("main_category")["price_per_100g"].agg(["mean", "count"])
    cat_stats = cat_stats[cat_stats["count"] >= 10].sort_values("mean")
    
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(cat_stats)))
    
    bars = ax.barh(cat_stats.index, cat_stats["mean"].values, color=colors)
    
    for bar, val, count in zip(bars, cat_stats["mean"].values, cat_stats["count"].values):
        ax.text(val + 50, bar.get_y() + bar.get_height()/2, 
                f'${val:,.0f} ({count} products)', 
                ha='left', va='center', fontsize=9)
    
    ax.set_xlabel("Average Price per 100g ($)", fontsize=12)
    ax.set_title("Average Price per 100g by Category", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "category_prices.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: category_prices.png")


def plot_protein_vs_price(df):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    valid = df[(df["price"] > 0) & (df["product_quantity_g"] > 0) & 
               (df["proteina_g_100g"].notna()) & (df["price_per_100g"] < 10000)].copy()
    valid = valid.drop_duplicates(subset=["ean"], keep="first")
    
    scatter = ax.scatter(valid["price_per_100g"], valid["proteina_g_100g"], 
                         c=valid["protein_per_peso"], cmap="RdYlGn", 
                         alpha=0.6, s=30, edgecolors='white', linewidth=0.5)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Protein per Peso (g/$)", fontsize=10)
    
    top5 = valid.nlargest(5, "protein_per_peso")
    for _, row in top5.iterrows():
        ax.annotate(row["product_name"][:25], 
                   (row["price_per_100g"], row["proteina_g_100g"]),
                   xytext=(10, 5), textcoords='offset points', fontsize=8,
                   arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    
    ax.set_xlabel("Price per 100g ($)", fontsize=12)
    ax.set_ylabel("Protein per 100g (g)", fontsize=12)
    ax.set_title("Protein vs Price\n(Green = Better value)", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "protein_vs_price.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: protein_vs_price.png")


def plot_products_by_retailer(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    counts = df["retailer"].value_counts()
    colors = ["#E91E63", "#9C27B0", "#3F51B5", "#00BCD4"]
    
    bars = ax.bar(counts.index, counts.values, color=colors, edgecolor='white', linewidth=1.5)
    
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{val:,}', 
                ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax.set_xlabel("Retailer", fontsize=12)
    ax.set_ylabel("Products with Nutritional Data", fontsize=12)
    ax.set_title("Products with Nutritional Information by Retailer", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "products_by_retailer.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: products_by_retailer.png")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    print("=" * 50)
    print("GENERATING VISUALIZATIONS")
    print("=" * 50)
    
    print("\nLoading data...")
    df = load_data()
    
    print("\nGenerating plots...\n")
    
    plot_nutriscore_distribution(df)
    plot_nova_distribution(df)
    plot_price_by_retailer(df)
    plot_cheapest_retailer_wins(df)
    plot_top_protein_value(df)
    plot_category_prices(df)
    plot_protein_vs_price(df)
    plot_products_by_retailer(df)
    
    print(f"\n✓ All plots saved to {OUTPUT_DIR}/")
    print("=" * 50)


if __name__ == "__main__":
    main()
