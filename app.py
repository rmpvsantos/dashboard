import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Meu Dashboard", layout="wide")

# --- LEMBRETE: O LINK DEVE TERMINAR EM /export?format=csv ---
URL_DA_FOLHA = "https://docs.google.com/spreadsheets/d/1OQrHgjjdYI779gOLYq3Vev7qfnew-oACX8TLJU4Ld24/export?format=csv"
try:
    # 1. Ler a folha
    df = pd.read_csv(URL_DA_FOLHA)
    
    # Limpar nomes de colunas (tirar espaços e converter para minúsculas)
    df.columns = df.columns.str.strip()
    
    # 2. Mostrar a Tabela para sabermos o que lá está
    with st.expander("👁️ Ver os meus dados da Folha"):
        st.write(df)

    # 3. Escolher a empresa (Usa a primeira coluna da tua folha, seja qual for o nome)
    coluna_principal = df.columns[0] 
    lista_empresas = df[coluna_principal].unique()
    
    empresa_sel = st.sidebar.selectbox("Selecionar Empresa:", lista_empresas)
    dados = df[df[coluna_principal] == empresa_sel].iloc

    # 4. Mostrar os dados de forma simples
    st.header(f"📈 Análise: {empresa_sel}")
    
    # Criar colunas automáticas com base no que tens na folha
    cols = st.columns(len(df.columns))
    for i, nome_coluna in enumerate(df.columns):
        cols[i].metric(label=nome_coluna, value=dados[nome_coluna])

    # 5. Gráfico Automático
    st.subheader("📊 Comparativo")
    col_num = df.select_dtypes(include=['number']).columns.tolist()
    if col_num:
        fig = px.bar(df, x=coluna_principal, y=col_num[0], title=f"Comparação de {col_num[0]}")
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Erro: {e}")
    st.info("Dica: Abre a tua Google Sheet e confirma se a PRIMEIRA COLUNA contém os Tickers (ex: AAPL).")
