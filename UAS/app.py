import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# --- 1. DATA PREPARATION ---
url = 'https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv'
df = pd.read_csv(url)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

# --- 2. METRICS ---
total_cust = len(df)
churn_df = df[df['Churn'] == 'Yes']
churn_rate = (len(churn_df) / total_cust) * 100
revenue_at_risk = churn_df['MonthlyCharges'].sum()

# --- 3. CUSTOM NEON VISUALS ---
# A. Neon Gauge for Churn Rate
fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = churn_rate,
    number = {'suffix': "%", 'font': {'color': '#00D4FF', 'size': 50}},
    title = {'text': "CHURN VELOCITY", 'font': {'color': '#FFFFFF', 'size': 15}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"},
        'bar': {'color': "#00D4FF"},
        'bgcolor': "rgba(0,0,0,0)",
        'borderwidth': 2,
        'bordercolor': "#334155",
        'steps': [
            {'range': [0, churn_rate], 'color': 'rgba(0, 212, 255, 0.2)'}
        ],
    }
))
fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=50, b=0, l=30, r=30))

# B. Neon Area Chart
tenure_counts = df.groupby(['tenure', 'Churn']).size().reset_index(name='Counts')
fig_area = px.area(tenure_counts, x="tenure", y="Counts", color="Churn",
                   line_shape="spline",
                   color_discrete_map={'Yes': '#00D4FF', 'No': '#7000FF'},
                   title="<b>USER RETENTION LIFECYCLE</b>")

fig_area.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#FFFFFF"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=False, color="#64748B"),
    yaxis=dict(showgrid=True, gridcolor="#1E293B", color="#64748B")
)

# --- 4. STYLING HELPERS ---
card_style = {
    "background": "rgba(17, 25, 40, 0.75)",
    "backdropFilter": "blur(12px)",
    "borderRadius": "20px",
    "border": "1px solid rgba(255, 255, 255, 0.125)",
    "padding": "20px"
}

# --- 5. DASHBOARD LAYOUT ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(style={'backgroundColor': '#0B0F19', 'minHeight': '100vh', 'color': 'white', 'padding': '30px'}, children=[
    
    # Header Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("RETAIN_OS v2.6", className="fw-bold mb-0", style={'letterSpacing': '5px', 'color': '#00D4FF'}),
                html.P("PREDICTIVE CUSTOMER INTELLIGENCE", className="text-muted", style={'letterSpacing': '2px'})
            ])
        ], md=8),
        dbc.Col([
            html.Div([
                DashIconify(icon="solar:shield-warning-bold", width=30, color="#FF0055"),
                html.Span("HIGH RISK ALERT", className="ms-2 fw-bold", style={'color': '#FF0055'})
            ], className="text-end")
        ], md=4)
    ], className="mb-5 align-items-center"),

    # KPI Row
    dbc.Row([
        dbc.Col(html.Div([
            html.Small("DATABASE SIZE", className="text-muted"),
            html.H2(f"{total_cust:,}", style={'color': '#FFFFFF', 'fontWeight': '800'})
        ], style=card_style), md=3),
        
        dbc.Col(html.Div([
            html.Small("MONTHLY REVENUE RISK", className="text-muted"),
            html.H2(f"${revenue_at_risk:,.0f}", style={'color': '#7000FF', 'fontWeight': '800'})
        ], style=card_style), md=3),
        
        dbc.Col(html.Div([
            html.Small("HEALTH SCORE", className="text-muted"),
            html.H2("74.2%", style={'color': '#00FF94', 'fontWeight': '800'})
        ], style=card_style), md=3),
        
        dbc.Col(html.Div([
            html.Small("AVG TENURE", className="text-muted"),
            html.H2("32.4 Mo", style={'color': '#FFB800', 'fontWeight': '800'})
        ], style=card_style), md=3),
    ], className="mb-4 g-3"),

    # Main Visuals
    dbc.Row([
        # Gauge Chart
        dbc.Col(html.Div([
            dcc.Graph(figure=fig_gauge, config={'displayModeBar': False})
        ], style=card_style), md=4),
        
        # Area Chart
        dbc.Col(html.Div([
            dcc.Graph(figure=fig_area, config={'displayModeBar': False})
        ], style=card_style), md=8),
    ], className="g-3 mb-4"),

    # Bottom Analysis Section
    dbc.Row([
        dbc.Col(html.Div([
            html.H5("CONTRACTUAL RISK MATRIX", className="mb-4 fw-bold"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div(style={'width': '10px', 'height': '10px', 'backgroundColor': '#00D4FF', 'borderRadius': '50%'}),
                        html.Span("Month-to-Month", className="ms-3 text-white-50"),
                        html.H4("42% Churn Rate", className="ms-auto fw-bold", style={'color': '#00D4FF'})
                    ], className="d-flex align-items-center mb-3 p-3", style={'backgroundColor': 'rgba(255,255,255,0.03)', 'borderRadius': '12px'})
                ], md=6),
                dbc.Col([
                    html.Div([
                        html.Div(style={'width': '10px', 'height': '10px', 'backgroundColor': '#7000FF', 'borderRadius': '50%'}),
                        html.Span("Long Term Contract", className="ms-3 text-white-50"),
                        html.H4("6.4% Churn Rate", className="ms-auto fw-bold", style={'color': '#7000FF'})
                    ], className="d-flex align-items-center mb-3 p-3", style={'backgroundColor': 'rgba(255,255,255,0.03)', 'borderRadius': '12px'})
                ], md=6),
            ])
        ], style=card_style), width=12)
    ])
])

if __name__ == '__main__':
    app.run(debug=True, port=8055)

