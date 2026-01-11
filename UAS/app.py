import dash
from dash import dcc, html
# HAPUS: import dash_bootstrap_components as dbc 
# HAPUS: from dash_iconify import DashIconify 
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
# A. Neon Gauge for Churn Rate (TIDAK ADA PERUBAHAN)
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

# B. Neon Area Chart (TIDAK ADA PERUBAHAN)
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
# Penambahan styling untuk layout grid
row_style = {'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px', 'marginBottom': '15px'}
col_style_kpi = {'flex': '1 1 23%', 'minWidth': '150px'}
col_style_visuals = {'flex': '1 1 45%', 'minWidth': '300px'}

# --- 5. DASHBOARD LAYOUT ---
# external_stylesheets dihilangkan karena dbc.themes.DARKLY dihapus
app = dash.Dash(__name__) 

app.layout = html.Div(style={'backgroundColor': '#0B0F19', 'minHeight': '100vh', 'color': 'white', 'padding': '30px'}, children=[
    
    # Header Section (Mengganti dbc.Row dan dbc.Col)
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '40px'}, children=[
        # Kiri: Judul
        html.Div(children=[
            html.H1("RETAIN_OS v2.6", style={'letterSpacing': '5px', 'color': '#00D4FF', 'fontSize': '32px', 'fontWeight': 'bold', 'marginBottom': '0'}),
            html.P("PREDICTIVE CUSTOMER INTELLIGENCE", style={'letterSpacing': '2px', 'color': '#A0AEC0', 'marginTop': '5px'})
        ]),
        # Kanan: Alert (Mengganti DashIconify)
        html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
            # Ganti Iconify dengan Div kosong sebagai placeholder
            html.Div(style={'width': '30px', 'height': '30px', 'backgroundColor': '#FF0055', 'borderRadius': '50%'}),
            html.Span("HIGH RISK ALERT", style={'marginLeft': '10px', 'fontWeight': 'bold', 'color': '#FF0055'})
        ])
        ]),

    # KPI Row (Mengganti dbc.Row dan dbc.Col)
    html.Div(style=row_style, children=[
        html.Div(html.Div([
            html.Small("DATABASE SIZE", style={'color': '#A0AEC0'}),
            html.H2(f"{total_cust:,}", style={'color': '#FFFFFF', 'fontWeight': '800'})
        ], style=card_style), style=col_style_kpi),
        
        html.Div(html.Div([
            html.Small("MONTHLY REVENUE RISK", style={'color': '#A0AEC0'}),
            html.H2(f"${revenue_at_risk:,.0f}", style={'color': '#7000FF', 'fontWeight': '800'})
        ], style=card_style), style=col_style_kpi),
        
        html.Div(html.Div([
            html.Small("HEALTH SCORE", style={'color': '#A0AEC0'}),
            html.H2("74.2%", style={'color': '#00FF94', 'fontWeight': '800'})
        ], style=card_style), style=col_style_kpi),
        
        html.Div(html.Div([
            html.Small("AVG TENURE", style={'color': '#A0AEC0'}),
            html.H2("32.4 Mo", style={'color': '#FFB800', 'fontWeight': '800'})
        ], style=card_style), style=col_style_kpi),
    ]),

    # Main Visuals (Mengganti dbc.Row dan dbc.Col)
    html.Div(style=row_style, children=[
        # Gauge Chart
        html.Div(html.Div([
            dcc.Graph(figure=fig_gauge, config={'displayModeBar': False})
        ], style=card_style), style={'flex': '1 1 30%', 'minWidth': '280px'}),
        
        # Area Chart
        html.Div(html.Div([
            dcc.Graph(figure=fig_area, config={'displayModeBar': False})
        ], style=card_style), style={'flex': '1 1 65%', 'minWidth': '500px'}),
    ]),

   # Bottom Analysis Section (DIPERBAIKI)
        html.Div(style=row_style, children=[
            html.Div(html.Div([
                html.H3("CUSTOMER SEGMENTATION INSIGHTS", style={'color': '#FFFFFF', 'fontWeight': '700'}),
                html.P("Segmentasi pelanggan berdasarkan lama berlangganan dan biaya bulanan...", style={'color': '#A0AEC0'})
            ], style=card_style), style={'flex': '1 1 48%', 'minWidth': '300px'}),
            
            html.Div(html.Div([
                html.H3("PREDICTIVE MODELING OVERVIEW", style={'color': '#FFFFFF', 'fontWeight': '700'}),
                html.P("Model prediktif menggunakan variabel seperti lama berlangganan...", style={'color': '#A0AEC0'})
            ], style=card_style), style={'flex': '1 1 48%', 'minWidth': '300px'}),
        ]) # Tutup Row ini
    ]) # <--- TAMBAHKAN INI (Tutup Children utama dari html.Div pertama)

if __name__ == '__main__':
    app.run(debug=True, port=8055)
