import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from CleanPrice import clean_price  # deine Bereinigungsfunktion für Preise

# === Anzahl der gekauften Stücke pro Aktie (nach ISIN) ===
# Anzahl der gekauften Stücke pro Aktie (ISIN)
positions = {
    "US0378331005": 11,     # Apple
    "US67066G1040": 20,     # NVIDIA
    "DE0008404005": 7,      # Allianz
    "NL0010273215": 3,      # ASML
    "US02079K1079": 12,      # Alphabet
    "IL0011334468": 8,      # CyberArk
    "US0231351067": 7,      # Amazon
}
# === CSV einlesen ==
# === "Change" bereinigen ===
df["Change"] = pd.to_numeric(
    df["Change"].str.replace('%', '', regex=False).str.replace(',', '.', regex=False),
    errors='coerce'
)

# === Preise bereinigen ===
df["Price"] = df["Price"].apply(clean_price)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# === Sortieren ===
df.sort_values(by=["ISIN", "Date"], inplace=True)

# === Gewinne berechnen ===
def calculate_profit(group):
    group = group.copy()
    isin = group["ISIN"].iloc[0]
    quantity = positions.get(isin, 0)
    group["Initial Price"] = group["Price"].iloc[0]
    group["Absolute Gain"] = (group["Price"] - group["Initial Price"]) * quantity
    group["Cumulative Gain"] = group["Absolute Gain"].cumsum()
    return group

df = df.groupby("ISIN").apply(calculate_profit)

# === Portfolio berechnen (kumuliert) ===
portfolio = df.groupby("Date")["Absolute Gain"].sum().reset_index()
portfolio["Cumulative Gain"] = portfolio["Absolute Gain"].cumsum()
portfolio["Company"] = "📊 Gesamtportfolio"
portfolio["ISIN"] = "PORTFOLIO"

# === In Haupt-DataFrame einfügen ===
df = pd.concat([df, portfolio], ignore_index=True)

# === Alle Unternehmen extrahieren ===
companies = df["Company"].unique()

# === Top Performer bestimmen ===
final_gains = df[df["Date"] == df["Date"].max()]
final_gains = final_gains.groupby("Company")["Cumulative Gain"].last().drop("📊 Gesamtportfolio")
top_performer = final_gains.idxmax()

# === Subplots vorbereiten ===
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=("Preisverlauf (€)", "Tägliche Veränderung (%)", "Kumulierte Bruttogewinne (€)")
)

# === Dropdown-Menü vorbereiten ===
dropdown_buttons = []
for i, company in enumerate(companies):
    company_data = df[df["Company"] == company].sort_values(by="Date")

    # Preis (für Portfolio nicht anzeigen)
    price_trace = go.Scatter(
        x=company_data["Date"],
        y=company_data["Price"] if company != "📊 Gesamtportfolio" else [None] * len(company_data),
        name=f"{company} Preis",
        visible=False
    )

    # Veränderung (für Portfolio nicht anzeigen)
    change_trace = go.Bar(
        x=company_data["Date"],
        y=company_data["Change"] if company != "📊 Gesamtportfolio" else [None] * len(company_data),
        name=f"{company} Veränderung",
        marker_color="orange",
        visible=False
    )

    # Kumulierte Gewinne
    is_top = company == top_performer
    gain_trace = go.Scatter(
        x=company_data["Date"],
        y=company_data["Cumulative Gain"],
        name=f"{company} Gewinn",
        line=dict(width=4, color="green" if is_top else None),
        visible=False
    )

    # Traces hinzufügen
    fig.add_trace(price_trace, row=1, col=1)
    fig.add_trace(change_trace, row=2, col=1)
    fig.add_trace(gain_trace, row=3, col=1)

    # Sichtbarkeit konfigurieren
    visibility = [False] * (3 * len(companies))
    visibility[3 * i] = True     # Preis
    visibility[3 * i + 1] = True  # Veränderung
    visibility[3 * i + 2] = True  # Gewinn

    dropdown_buttons.append({
        "label": company + (" ⭐" if is_top else ""),
        "method": "update",
        "args": [{"visible": visibility},
                 {"title": f"{company} – Interaktive Analyse"}]
    })

# Erste Firma sichtbar machen
fig.data[0].visible = True
fig.data[1].visible = True
fig.data[2].visible = True

# === Layout ===
fig.update_layout(
    updatemenus=[{
        "buttons": dropdown_buttons,
        "direction": "down",
        "showactive": True,
        "x": 0.0,
        "xanchor": "left",
        "y": 1.28,
        "yanchor": "top"
    }],
    height=950,
    title=f"{companies[0]} – Interaktive Analyse",
    xaxis_title="Datum",
    yaxis_title="Preis (€)",
    xaxis2_title="Datum",
    yaxis2_title="Veränderung (%)",
    xaxis3_title="Datum",
    yaxis3_title="Kumulierte Bruttogewinne (€)",
    template="plotly_white"
)

# === Plot anzeigen ===
fig.show()
