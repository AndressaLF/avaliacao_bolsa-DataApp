# alterando para fazer o commit

# importando as bibliotecas

import streamlit as st  # biblioteca responsável por transformar scripts de dados em aplicativos web
import pandas as pd  # biblioteca responsável por
import plotly.express as px  
import plotly.graph_objects as go

import yfinance as yf  # responsável pela base de dados dinâmica


# Essa função converte o df que será exportado no final
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


def main():
    st.title("Analisando Ações - Andressa Lima")  # api reference - text elements
    st.image("data.jpg")  # api reference - media elements
    
    # criando um dicionário com o nome das empresas e simbolos
    simbolos_empresas = {'Ibovespa':'^BVSP','Via Varejo':'VIIA3.SA', 
                        'Apple':'AAPL', 'Petrobras':'PBR'}
    
    # criando o select box com o nome das opções é uma tupla com a pergunta e opções
    option = st.selectbox('Qual empresa você deseja analisar?', tuple(simbolos_empresas.keys()))
    st.write('Vocês selecionou: ', option)  # mostrando a opção selecionada

    # importando os dados e resetando o index(data) é necessário transformar o index em coluna
    df = yf.Ticker(simbolos_empresas[option]).history(start="2018-01-01").reset_index()
    #df_new = df
    #df_new["Date"] = df["Date"].dt.date
    df["Date"] = pd.to_datetime(df["Date"].dt.date, format="%Y-%m-%d")
    st.write(df.head())  # mostrando os dados no streamlit
    
    
    st.text("Visualizando os últimos registros do dataset...") 
    slider = st.slider("Valores", 0, 100)  # api reference - slider  | Criando uma regua com valores de 0 a 100
    st.dataframe(df.tail(slider))  # retorna o tail do valor que o slider está


    st.title("Gráfico - Fechamento das Ações")  
    fig1 = px.line(df, x="Date", y="Close", title="Fechamento das Ações", template='seaborn')  # criando gráfico de linha
    #st.plotly_chart(fig1, use_container_width=True) # outra forma de mostrar os gráficos
    st.write(fig1)# mostrando o gráfico na tela
    
    
    st.title("Gráfico - Dividendos")
    dividendos = df.groupby(df["Date"].dt.year)["Dividends"].sum().reset_index()  # calculando os dividendos
    fig2 = px.line(dividendos, x="Date", y="Dividends", title="Dividendos Anuais", template='seaborn')
    st.write(fig2)

    # Gráfico de candlestick
    st.subheader("Gráfico de Candlestick")
    st.text("Podemos analisar a oscilação entre a abertura e o fechamento, e se a ação fechou maior ou menor que o preço de abertura, para isso só analisar pela cor,os vermelhos fecharam com o preço menor do que o de abertura e os verdes fecharam com o preço maior do que o de abertura.")
    
    df_grafico = df.nlargest(7, "Date")
    fig3 = go.Figure(data=[go.Candlestick(x=df_grafico['Date'],
                open=df_grafico['Open'],
                high=df_grafico['High'],
                low=df_grafico['Low'],
                close=df_grafico['Close'])])
    
    fig3.update_layout(title='Candlestick últimos 7 dias', template='seaborn')
    st.write(fig3)
    
    # Adicionando o botão de download - widgests- button
    csv = convert_df(df)

    st.download_button(
    label="Download dos dados em CSV",
    data=csv,
    file_name='acoes.csv',
    mime='text/csv',
)








if __name__ == '__main__':
    main()
    
