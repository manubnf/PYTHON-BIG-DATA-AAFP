from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

electricity_data = pd.read_excel("./family_data/utility_assistance_electricity.xlsx")
income_data = pd.read_excel("./family_data/family_income.xlsx")
support_data = pd.read_csv("./family_data/family_support_data.csv")

support_summary = pd.DataFrame({
    "Type of Assistance": ["Electricity", "Food", "Healthcare"],
    "Families Assisted": [
        electricity_data["Family"].nunique(),
        support_data[support_data["Type"] == "Food"]["Family"].nunique(),
        support_data[support_data["Type"] == "Healthcare"]["Family"].nunique(),
    ],
    "Total Assistance": [
        electricity_data["Amount"].sum(),
        support_data[support_data["Type"] == "Food"]["Amount"].sum(),
        support_data[support_data["Type"] == "Healthcare"]["Amount"].sum(),
    ],
})

app = Dash(__name__)
server = app.server

figAssistanceSummary = px.bar(
    support_summary,
    x="Type of Assistance",
    y="Total Assistance",
    color="Families Assisted",
    title="Total Assistance Provided by Type",
    labels={"Total Assistance": "Total Amount (R$)", "Families Assisted": "Number of Families"},
)

figElectricityTrend = px.line(
    electricity_data,
    x="Reference",
    y="Amount",
    title="Electricity Assistance Over Time",
    markers=True,
    labels={"Amount": "Amount (R$)", "Reference": "Months/Year"},
)

figIncomeTrend = px.line(
    income_data,
    x="Period",
    y="Average Income",
    title="Average Family Income Over Time",
    markers=True,
    labels={"Average Income": "Average Income (R$)", "Period": "Months/Year"},
)

figAssistancePie = px.pie(
    support_summary,
    values="Families Assisted",
    names="Type of Assistance",
    title="Distribution of Families Assisted by Type of Assistance",
)

app.layout = html.Div(
    [
        html.H1("AAFP - Social Assistance Dashboard"),
        html.Div([
            dcc.Graph(id="graph_assistance_summary", figure=figAssistanceSummary),
            dcc.Graph(id="graph_electricity_trend", figure=figElectricityTrend),
        ], style={"display": "flex", "justify-content": "space-around"}),

        html.Div([
            dcc.Graph(id="graph_income_trend", figure=figIncomeTrend),
            dcc.Graph(id="graph_assistance_pie", figure=figAssistancePie),
        ], style={"display": "flex", "justify-content": "space-around"}),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host="0.0.0.0")
