import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from CleanPrice import clean_price  # deine Bereinigungsfunktion für Preise

# === Anzahl der gekauften Stücke pro Aktie (nach ISIN) ===
positions = pd.read_csv("InputData/StockProperty.csv")

# === CSV einlesen ===
df = pd.read_csv("InputData/StockInputData.csv", parse_dates=["Date"])

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

# === Gewinne und Wert berechnen ===
def calculate_profit(group):
    group = group.copy()
    isin = group["ISIN"].iloc[0]
    quantity = positions.get(isin, 0)
    group["Initial Price"] = group["Price"].iloc[0]
    group["Absolute Gain"] = (group["Price"] - group["Initial Price"]) * quantity
    group["Cumulative Gain"] = group["Absolute Gain"].cumsum()
    group["Value"] = group["Price"] * quantity
    return group

df = df.groupby("ISIN").apply(calculate_profit)

# === Portfolio berechnen (Gewinne) ===
portfolio = df.groupby("Date")["Absolute Gain"].sum().reset_index()
portfolio["Cumulative Gain"] = portfolio["Absolute Gain"].cumsum()
portfolio["Company"] = "📊 Gesamtportfolio"
portfolio["ISIN"] = "PORTFOLIO"

# === Portfolio berechnen (Wert) ===
portfolio_value = df[df["ISIN"] != "PORTFOLIO"].groupby("Date")["Value"].sum().reset_index()
portfolio_value["Company"] = "📈 Portfoliowert"
portfolio_value["ISIN"] = "PORTFOLIO"
portfolio_value.rename(columns={"Value": "Portfolio Value"}, inplace=True)

# === In Haupt-DataFrame einfügen ===
df = pd.concat([df, portfolio, portfolio_value], ignore_index=True)

# === Alle Unternehmen extrahieren ===
companies = df["Company"].unique()

# === Top Performer bestimmen ===
final_gains = df[df["Date"] == df["Date"].max()]
final_gains = final_gains.groupby("Company")["Cumulative Gain"].last().drop("📊 Gesamtportfolio", errors="ignore")
top_performer = final_gains.idxmax()

# === Subplots vorbereiten ===
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=("Preisverlauf (€)", "Tägliche Veränderung (%)", "Kumulierte Bruttogewinne (€) + Portfoliowert (€)")
)

# === Dropdown-Menü vorbereiten ===
dropdown_buttons = []
for i, company in enumerate(companies):
    company_data = df[df["Company"] == company].sort_values(by="Date")

    # Preis (für Portfolio nicht anzeigen)
    price_trace = go.Scatter(
        x=company_data["Date"],
        y=company_data["Price"] if company not in ["📊 Gesamtportfolio", "📈 Portfoliowert"] else [None] * len(company_data),
        name=f"{company} Preis",
        visible=False
    )

    # Veränderung (für Portfolio nicht anzeigen)
    change_trace = go.Bar(
        x=company_data["Date"],
        y=company_data["Change"] if company not in ["📊 Gesamtportfolio", "📈 Portfoliowert"] else [None] * len(company_data),
        name=f"{company} Veränderung",
        marker_color="orange",
        visible=False
    )

    # Kumulierte Gewinne
    is_top = company == top_performer
    gain_trace = go.Scatter(
        x=company_data["Date"],
        y=company_data["Cumulative Gain"] if "Cumulative Gain" in company_data else [None] * len(company_data),
        name=f"{company} Gewinn",
        line=dict(width=4, color="green" if is_top else None),
        visible=False
    )

    fig.add_trace(price_trace, row=1, col=1)
    fig.add_trace(change_trace, row=2, col=1)
    fig.add_trace(gain_trace, row=3, col=1)

    # Sichtbarkeit konfigurieren
    visibility = [False] * (3 * len(companies) + 1)  # +1 for portfolio value line
    visibility[3 * i] = True
    visibility[3 * i + 1] = True
    visibility[3 * i + 2] = True

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

# === Portfoliowert-Linie hinzufügen (immer sichtbar) ===
value_data = df[df["Company"] == "📈 Portfoliowert"]
fig.add_trace(
    go.Scatter(
        x=value_data["Date"],
        y=value_data["Portfolio Value"],
        name="📈 Portfoliowert",
        line=dict(color="blue", width=2, dash="dot"),
        visible=True  # always visible
    ),
    row=3, col=1
)

# === Layout ===
fig.update_layout(
    updatemenus=[{
        "buttons": dropdown_buttons,
        "direction": "down",
        "showactive": True,
        "x": 0.0,
        "xanchor": "left",
        "y": 1.3,
        "yanchor": "top"
    }],
    height=950,
    title=f"{companies[0]} – Interaktive Analyse",
    xaxis_title="Datum",
    yaxis_title="Preis (€)",
    xaxis2_title="Datum",
    yaxis2_title="Veränderung (%)",
    xaxis3_title="Datum",
    yaxis3_title="€",
    template="plotly_white"
)

# === Plot anzeigen ===
fig.show()
