import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Meu Dashboard Fundamental", layout="wide")

# --- PASSO CRUCIAL: COLOCA O TEU LINK AQUI ---
URL_DA_FOLHA = "https://docs.google.com/spreadsheets/d/1OQrHgjjdYI779gOLYq3Vev7qfnew-oACX8TLJU4Ld24/export?format=csv"

st.title("📊 Análise Fundamental Personalizada")

try:
    # 1. Ler os dados da Google Sheet
    df = pd.read_csv(URL_DA_FOLHA)
    
    # Limpar espaços em branco nos nomes das colunas
    df.columns = df.columns.str.strip()

    # 2. Barra Lateral para escolher a Empresa
    st.sidebar.header("Configurações")
    lista_empresas = df['Ticker'].unique()
    empresa_selecionada = st.sidebar.selectbox("Escolha o Ticker:", lista_empresas)

    # 3. Filtrar dados da empresa escolhida
    dados_empresa = df[df['Ticker'] == empresa_selecionada].iloc[0]

    # 4. Mostrar Métricas (Dashboards)
    st.header(f"🏢 {dados_empresa.get('Nome', 'Empresa')} ({empresa_selecionada})")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Preço", f"€{dados_empresa.get('Preço', 0)}")
    col2.metric("P/L", dados_empresa.get('PL', 'N/A'))
    col3.metric("ROE", f"{dados_empresa.get('ROE', 0)}%")
    col4.metric("Div. Yield", f"{dados_empresa.get('DY', 0)}%")

    # 5. História e Motores de Negócio
    st.subheader("📖 História e Motores de Negócio")
    st.info(dados_empresa.get('Descricao', 'Sem descrição na folha.'))

    # 6. Gráfico Simples (Se tiveres colunas de histórico na folha)
    st.subheader("📈 Evolução Visual")
    # Este gráfico usa as colunas da tua folha para comparar valores
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    fig = px.bar(df, x='Ticker', y=colunas_numericas[0], title="Comparação de Mercado")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao ler os dados: {e}")
    st.warning("Verifica se o link termina em 'export?format=csv' e se a folha está partilhada como 'Qualquer pessoa com o link'.")
