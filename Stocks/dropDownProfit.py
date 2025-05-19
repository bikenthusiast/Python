import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from CleanPrice import clean_price

# Anzahl der gekauften Stücke pro Aktie (ISIN)
positions = {
    "US0378331005": 10,  # Apple
    "US5949181045": 5,   # Microsoft
    # Weitere Aktien ergänzen
}

# CSV-Datei einlesen
df = pd.read_csv("StockInputData.csv", parse_dates=["Date"])

# "Change" Spalte bereinigen
df["Change"] = pd.to_numeric(
    df["Change"].str.replace('%', '', regex=False).str.replace(',', '.', regex=False),
    errors='coerce'
)

# Preise bereinigen
df["Price"] = df["Price"].apply(clean_price)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Daten sortieren
df.sort_values(by=["ISIN", "Date"], inplace=True)

# Gewinne berechnen
def calculate_profit(group):
    group = group.copy()
    isin = group["ISIN"].iloc[0]
    quantity = positions.get(isin, 0)
    group["Initial Price"] = group["Price"].iloc[0]
    group["Absolute Gain"] = (group["Price"] - group["Initial Price"]) * quantity
    return group

df = df.groupby("ISIN").apply(calculate_profit)

# Gesamtportfolio über Zeit berechnen
portfolio = df.groupby("Date")["Absolute Gain"].sum().reset_index()
portfolio["Company"] = "📊 Gesamtportfolio"
portfolio["ISIN"] = "PORTFOLIO"

# Unternehmen extrahieren (inkl. Portfolio)
df = pd.concat([df, portfolio], ignore_index=True)
companies = df["Company"].unique()

# Subplots: 3 Zeilen → Preis, Veränderung, Gewinn
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=("Preisverlauf (€)", "Tägliche Veränderung (%)", "Bruttogewinn (€)")
)

# Dropdown Buttons vorbereiten
dropdown_buttons = []
for i, company in enumerate(companies):
    company_data = df[df["Company"] == company].sort_values(by="Date")

    # Preis (nur falls kein Portfolio, das hat keine Preisreihe)
    price_trace = go.Scatter(
        x=company_data["Date"],
        y=company_data["Price"] if company != "📊 Gesamtportfolio" else [None]*len(company_data),
        name=f"{company} Preis",
        visible=False
    )

    # Veränderung
    change_trace = go.Bar(
        x=company_data["Date"],
        y=company_data["Change"] if company != "📊 Gesamtportfolio" else [None]*len(company_data),
        name=f"{company} Veränderung",
        marker_color="orange",
        visible=False
    )

    # Gewinn
    gain_trace = go.Scatter(
        x=company_data["Date"],
        y=company_data["Absolute Gain"],
        name=f"{company} Gewinn",
        line=dict(width=3) if company == "📊 Gesamtportfolio" else {},
        visible=False
    )

    # Traces hinzufügen
    fig.add_trace(price_trace, row=1, col=1)
    fig.add_trace(change_trace, row=2, col=1)
    fig.add_trace(gain_trace, row=3, col=1)

    # Sichtbarkeiten konfigurieren
    visibility = [False] * (3 * len(companies))
    visibility[3 * i] = True     # Preis
    visibility[3 * i + 1] = True  # Veränderung
    visibility[3 * i + 2] = True  # Gewinn

    dropdown_buttons.append({
        "label": company,
        "method": "update",
        "args": [{"visible": visibility},
                 {"title": f"{company} – Interaktive Analyse"}]
    })

# Erste Firma sichtbar machen
fig.data[0].visible = True
fig.data[1].visible = True
fig.data[2].visible = True

# Layout
fig.update_layout(
    updatemenus=[{
        "buttons": dropdown_buttons,
        "direction": "down",
        "showactive": True,
        "x": 0.0,
        "xanchor": "left",
        "y": 1.25,
        "yanchor": "top"
    }],
    height=900,
    title=f"{companies[0]} – Interaktive Analyse",
    xaxis_title="Datum",
    yaxis_title="Preis (€)",
    xaxis2_title="Datum",
    yaxis2_title="Veränderung (%)",
    xaxis3_title="Datum",
    yaxis3_title="Bruttogewinn (€)",
    template="plotly_white"
)

fig.show()

