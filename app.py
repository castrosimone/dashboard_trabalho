

import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Análise de Casas para Aluguel no Brasil')

# Função para carregar dados a partir de um arquivo CSV carregado
@st.cache_data
def carregar_dados(arquivo_enviado):
    try:
        dados = pd.read_csv(arquivo_enviado)
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Interface de upload de arquivo
arquivo_enviado = st.file_uploader("Escolha um arquivo CSV", type="csv")

if arquivo_enviado is not None:
    # Texto de carregamento
    estado_carregamento = st.text('Carregando os dados...')
    
    # Chamar a função para carregar os dados
    dados = carregar_dados(arquivo_enviado)

    if dados is not None:
        estado_carregamento.text("Dados carregados com sucesso!")
        
        # Exibir os dados brutos opcionalmente
        if st.checkbox('Exibir dados brutos'):
            st.subheader('Dados Brutos')
            st.write(dados.head())

        # Seletor para escolher a cidade
        city = dados['city'].unique()  # Obter as cidades únicas do DataFrame
        cidade_selecionada = st.selectbox('Escolha uma cidade:', city)

        # Botão para calcular custos totais de aluguel para a cidade selecionada e mostrar os dados
        if st.button('Exibir dados da cidade e calcular custos'):
            # Verifica se as colunas necessárias estão presentes
            if 'city' in dados.columns and 'rent amount (R$)' in dados.columns:
                
                # Filtrar os dados pela cidade selecionada
                dados_cidade = dados[dados['city'] == cidade_selecionada]
                
                # Exibir os dados da cidade
                st.subheader(f'Dados dos imóveis em {cidade_selecionada}')
                st.write(dados_cidade)

                # Calcular o custo total de aluguel para a cidade selecionada
                custo_total = dados_cidade['rent amount (R$)'].sum()
                
                # Exibir o custo total
                st.subheader(f'Custo Total de Aluguel para {cidade_selecionada}')
                st.write(f'O custo total de aluguel em {cidade_selecionada} é R$ {custo_total:.2f}')

        

        # Slider para escolher o número de quartos
        if 'rooms' in dados.columns:  # Certificar-se que a coluna é "quartos"
            filtro_quartos = st.slider(
                'Filtrar por número de quartos', 
                int(dados['rooms'].min()), 
                int(dados['rooms'].max()), 
                int(dados['rooms'].mean())
            )
            
            # Filtrar os dados de acordo com o número de quartos
            dados_filtrados_quartos = dados[dados['rooms'] == filtro_quartos]
            
            # Exibir os dados filtrados
            st.subheader(f'Imóveis com {filtro_quartos} rooms')
            st.write(dados_filtrados_quartos)



            # Agrupar por cidade e calcular a média dos valores de aluguel
            media_aluguel_por_cidade = dados.groupby('city')['rent amount (R$)'].mean().reset_index()

            # Exibir a média do aluguel por cidade
            st.subheader('Média de Aluguel por Cidade')
            st.write(media_aluguel_por_cidade)

            # Criar o gráfico de comparação usando Plotly
            fig = px.bar(media_aluguel_por_cidade, 
                         x='city', 
                         y='rent amount (R$)', 
                         title='Comparação dos Valores Médios de Aluguel por Cidade',
                         labels={'rent amount (R$)': 'Valor Médio de Aluguel (R$)', 'city': 'Cidade'},
                         color='city')

            # Exibir o gráfico
            st.plotly_chart(fig)
else:
    st.write("Por favor, faça o upload de um arquivo CSV para começar.")
