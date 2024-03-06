import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("supermarket_sales.csv", sep = ";", decimal = ",", thousands=".")
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values("Date")

icon = open("icon.png", "rb").read()

st.set_page_config(
    page_title="Faturamente de Loja",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
)
st.sidebar.image(icon, width=100, use_column_width=False)

cities = df["City"].unique()

df["Month"] = df["Date"].apply(lambda x : str(x.year) + "-" +str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())
st.sidebar.markdown("### Cidades")
selecionar_cidade = list(cities)

for city in cities:
    checkbox = st.sidebar.checkbox(city, value=True)
    if not checkbox:
        selecionar_cidade.remove(city)

df_filtro = df[(df["Month"] == month) & (df["City"].isin(selecionar_cidade))]

nav = st.title("Faturamento Supermercado")

color_map_city = {
    'Sao Paulo': '#00BFFF',
    'Guarulhos': '#1E90FF',
    'Mogi das Cruzes': '#0000CD',
}

color_map_prod = {
    'Esportes e viagens': '#191970',
    'Casa e estilo de vida': '#87CEFA',
    'Acessorios eletronicos': '#00008B',
    'Saude e beleza': '#0000FF',
    'Acessorios de Moda': '#00BFFF',
    'Alimentos e bebidas': '#1E90FF',
}

color_map_payment = {
    "PIX": "#1E90FF",
    "Dinheiro": "#00BFFF",
    "Cartao de Credito": "#0000CD",
}
color_map_dia = {
    "Date" : "#0000CD",
}

colu, colu3 = st.columns([2, 1])
colu1, colu2 = st.columns([1, 2])

total_dia = df_filtro.groupby("Date")[["Total"]].sum().reset_index()
fig_date = px.bar(total_dia, x="Date", y="Total", title="Faturamento por Dia", color_discrete_sequence=px.colors.qualitative.Set1, barmode="group")
fig_date.update_traces(selector=dict(type='bar'), hoverinfo='skip', hovertemplate="<b>%{y}</b><extra></extra>", marker_color=color_map_dia['Date'])
colu.plotly_chart(fig_date, use_container_width=True)

avg_rating_per_day = df_filtro.groupby(['Date'])['Rating'].mean().reset_index()
fig_avalia = px.line(avg_rating_per_day, x='Date', y='Rating', title='Avaliação Média das Lojas')
st.plotly_chart(fig_avalia, use_container_width=True)

total_city = df_filtro.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(total_city, x="City", y="Total", color="City", title="Faturamento Mensal", color_discrete_map=color_map_city)
fig_city.update_traces(selector=dict(type='bar'), hoverinfo='skip', hovertemplate="<b>%{y}</b><extra></extra>")
colu3.plotly_chart(fig_city, use_container_width=True)

total_prod = df_filtro.groupby("Product line")[["Total"]].sum().reset_index()
fig_prod = px.bar(total_prod, x="Total", y="Product line", color="Product line", title="Faturamento por tipo de produto",  orientation="h", barmode="group", color_discrete_map=color_map_prod,)
fig_prod.update_traces(selector=dict(type='bar'), hoverinfo='skip', hovertemplate="<b>%{x}</b><extra></extra>")
colu2.plotly_chart(fig_prod, use_container_width=True)

fig_pizza = px.pie(df_filtro, values="Total", names="Payment", color="Payment", title="Faturamento por opção de pagamento", color_discrete_map=color_map_payment)
fig_pizza.update_traces(selector=dict(type='pie'), hoverinfo='skip', hovertemplate="")
colu1.plotly_chart(fig_pizza, use_container_width=True)