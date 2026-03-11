""""Importando bibliotecas"""
import pandas as pd
import streamlit as st
import openpyxl as op 
import plotly.express as px
import plotly.graph_objects as go
import locale
import altair as alt


#Pagina cheia
st.set_page_config(layout='wide')

#"""Titulo da página"""
html_title = """
    <style>
    .title-test{
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    color: white;
    text-align: center;
    }

    /* Esconde o label do multiselect */
    .stMultiSelect label {
        
    }

    /* Texto das opções do dropdown */
    div[data-baseweb="menu"] span {
        font-size: 20px !important;
        color: white;
    }

    /* Fundo principal */
    section[data-testid="stAppViewContainer"] {
        background-color: #badea6;
    }

    /* Multiselect */
    div[data-testid="stMultiSelect"] > div {
        border: 2px;
        border-radius: 18px;
        padding: 6px;
    }

    /* Hover */
    div[data-testid="stMultiSelect"]:hover > div {
        background-color: #5058EB;
    }

    /* Tags selecionadas do multiselect */
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background-color: #5058EB !important;  /* VERDE */
        color: white !important;
        border-radius: 12px;
        padding: 10px 28px;
        font-weight: 500;
    }

    /* Botões */
    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
        height: 3em;
        border-radius: 6px;
        background-color: #28991f;
        color: white;
    }

    /* Botões da sidebar */
    div[data-testid="stSidebar"] .stButton > button {
        background-color: #dc3545;
        color: white;
        border-radius: 6px;
        border: none;
    }

    div[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #a71d2a;
    }
    </style>
"""
st.markdown(html_title, unsafe_allow_html=True)
st.markdown("<h1 class='title-test'>DASHBOARD DE VENDAS</h1>", unsafe_allow_html=True)

#"""Cabeçalho da página"""
st.divider()
co1, co2  = st.columns([1,1])
with co1:
    st.markdown(""" ### Visão Geral""")
    st.markdown("#### Este dashboard exibe os principais indicadores de vendas no período de 2012 a 2015. É possível aplicar filtros por intervalo de tempo, estado, ano e mês, para explorar tendências e desempenho comercial.")

with co2:
    st.markdown(""" #### Resumo Executivo""")
    st.markdown("#### No período de 2012 a 2015, observou-se crescimento no volume de vendas, embora tenha ocorrido redução no ticket médio. O segmento corporativo apresenta o maior faturamento, e os vendedores Artur Moreira e Josias Silva destacam-se como os mais produtivos.")

#Barra lateral
st.sidebar.divider()
st.sidebar.title('Opções de Filtros')

#Carregamento do arquivo
#uploader = st.sidebar.file_uploader('Insira o Arquivo', type=["xlsx","xls","csv"])
uploader = 'dataset_vendas.xlsx'
#verifica se o arquivo foi enviado
if uploader is not None:
    try:
        df= pd.read_excel(uploader)
    except Exception as e:
         st.error('Carregue um arquivo, Por favor!')

    #Ajustar a coluna de data para criar filtros
    df['data_venda'] = pd.to_datetime(df['data_venda'],errors='coerce')
    df['data_venda_br'] = df['data_venda'].dt.strftime('%d %m %y')

    df['ano'] = df['data_venda'].dt.year
    df['mes'] = df['data_venda'].dt.month
    df['mes_nome'] = df['data_venda'].dt.strftime('%B')#nome do mês em portugues
    
    ordem_meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
               'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    
    vendas_por_mes = df.groupby('mes_nome')['valor_venda'].sum().reset_index()

    # Padronizar para minúsculas
    vendas_por_mes['mes_nome'] = vendas_por_mes['mes_nome'].str.lower()

    # Reordenar
    vendas_por_mes['mes_nome'] = pd.Categorical(vendas_por_mes['mes_nome'], categories=ordem_meses, ordered=True)
    vendas_por_mes = vendas_por_mes.sort_values('mes_nome')

    #Filtros de data inicio e final
    data_inicio = st.sidebar.date_input(
    'Data inicial',
    value=df['data_venda'].min(),
    min_value=df['data_venda'].min(),
    max_value=df['data_venda'].max()
    )
    data_fim = st.sidebar.date_input(
    'Data final',
    value=df['data_venda'].max(),
    min_value=df['data_venda'].min(),
    max_value=df['data_venda'].max()
    )

    #Aplicar filtro de tempo
    df_filtrado = df[
                    (df['data_venda']>=pd.to_datetime(data_inicio))&
                    (df['data_venda']<=pd.to_datetime(data_fim))
                    ]
    
    # --- Filtros ---
    estados = df["estado_loja"].unique().tolist()
    estado_selecionado = st.sidebar.multiselect("Filtrar Estado", estados)

    categoria = df["categoria_produto"].unique().tolist()
    categoria_selecionado = st.sidebar.multiselect("Filtrar Categoria", categoria)

    anos = sorted(df['ano'].unique().tolist())
    ano_selecionado = st.sidebar.selectbox('Filtrar Ano', ['Todos'] + anos)

    mapa_meses = {
    1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
    5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
    9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
}
    ordem_meses = list(mapa_meses.values())

    # Traduz os meses logo após criar a coluna
    df['mes_nome'] = df['data_venda'].dt.month.map(mapa_meses)
    df_filtrado['mes_nome'] = df_filtrado['data_venda'].dt.month.map(mapa_meses)

    # Criar coluna auxiliar com posição do mês
    df_filtrado['ordem'] = df_filtrado['mes_nome'].apply(
        lambda x: ordem_meses.index(x) if x in ordem_meses else -1
    )

    # Agora sim o agrupamento funciona
    vendas_mes = (
    df_filtrado.groupby(['mes_nome','ordem'])['valor_venda']
    .sum()
    .reset_index()
    .sort_values('ordem')
    )

    meses = [m for m in ordem_meses if m in df['mes_nome'].unique()]

    mes_selecionado = st.sidebar.selectbox('Filtrar Mês', ['Todos'] + ordem_meses)

    # --- Aplicar filtros ---
    df_filtrado = df.copy()
    # Data
    df_filtrado = df_filtrado[
      (df_filtrado['data_venda'] >= pd.to_datetime(data_inicio)) &
      (df_filtrado['data_venda'] <= pd.to_datetime(data_fim))
    ]     
    if categoria_selecionado:
        df_filtrado = df_filtrado[df_filtrado['categoria_produto'].isin(categoria_selecionado)]

    if estado_selecionado:
        df_filtrado = df_filtrado[df_filtrado['estado_loja'].isin(estado_selecionado)]

    if ano_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['ano'] == ano_selecionado]

    if mes_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['mes_nome'] == mes_selecionado]

    # --- Criar coluna auxiliar com posição do mês ---
    df_filtrado['ordem'] = df_filtrado['mes_nome'].apply(
        lambda x: ordem_meses.index(x)
    )

# --- Agrupamento ---
    vendas_mes = (
        df_filtrado.groupby(['mes_nome', 'ordem'])['valor_venda']
        .sum()
        .reset_index()
        .sort_values('ordem')
    )

    #Colunas para ajustar cartão de indicadores
    coluna1,coluna2,coluna3,coluna4 = st.columns([3,3,3,3])

    with st.expander("Explicação dos Indicadores"):
        st.markdown("""
        #### 🔍 Indicadores Principais
        - **Faturamento**: Soma total das vendas no período selecionado.  
        - **Quantidade de Vendas**: Número total de transações realizadas.  
        - **Ticket Médio**: Valor médio por venda, calculado como Faturamento ÷ Qtde de Vendas.  
        - **Quantidade de Produtos**: Número de produtos únicos vendidos.
        """)

    #INDICADORES
    Faturamento = df_filtrado['valor_venda'].sum()
    with coluna1:
        st.markdown(f"""
        <div style="
            background:#7376FA;
            padding:15px;
            border-radius:20px;
            text-align:center;
            color:white;
            font-size:32px;
            font-weight:bold;
        ">
            Faturamento<br>
            R$ {Faturamento:,.0f}
        </div>
        """, unsafe_allow_html=True)

    Qtde_vendas = len(df_filtrado)

    with coluna2:
        st.markdown(f"""
        <div style="
            background:#7376FA;
            padding:15px;
            border-radius:20px;
            text-align:center;
            color:white;
            font-size:32px;
            font-weight:bold;
        ">
            Qtde_Vendas<br>
            {Qtde_vendas:,.0f}
        </div>
        """, unsafe_allow_html=True)

    Ticket = round(df_filtrado['valor_venda'].mean(),2)

    with coluna3:
        st.markdown(f"""
        <div style="
            background:#7376FA;
            padding:15px;
            border-radius:20px;
            text-align:center;
            color:white;
            font-size:32px;
            font-weight:bold;
        ">
            Ticket_Médio<br>
            R${Ticket:,.0f}
        </div>
        """, unsafe_allow_html=True)   

    Qtd_Produtos = df_filtrado['nome_produto'].nunique() 

    with coluna4:
        st.markdown(f"""
        <div style="
            background:#7376FA;
            padding:15px;
            border-radius:20px;
            text-align:center;
            color:white;
            font-size:32px;
            font-weight:bold;
        ">
            Qtde_Produtos<br>
            {Qtd_Produtos:,.0f}
        </div>
        """, unsafe_allow_html=True)    


    #Colunas para separar os Graficos
    col1,  col3 = st.columns([ 3,6])

    #Calculos para adicionar nos Graficos
    grafico_linha = df_filtrado.groupby('ano').agg(
        Faturamento = ('valor_venda','sum'),
        Qtde_vendas = ('cod_produto','count')
    ).reset_index()
    grafico_linha['Ticket'] = grafico_linha['Faturamento']/ grafico_linha['Qtde_vendas']
    vendas_vendedor = df_filtrado.groupby(['nome_vendedor']).agg({'valor_venda':'sum'}).sort_values(by='valor_venda', ascending=True).reset_index()
    vendas_loja = df_filtrado.groupby(['cod_loja']).size().reset_index(name='Qtd_Vendas').sort_values(by='Qtd_Vendas',ascending=False)
    vendas_segmento = df_filtrado.groupby(['segmento_produto']).agg({'valor_venda':'sum'})

    st.divider()#Linha no final do Dashboard

    with col1:
        fig_rosca = px.pie(
            vendas_segmento,
            values="valor_venda",
            names=vendas_segmento.index,
            title=" ",
            hole=0.5  # transforma em rosca
            )
        fig_rosca.update_layout(
            width=600,
            height=450
        )
        st.subheader('💰Faturamento por Segmento')
        st.plotly_chart(fig_rosca,use_container_width=True)
    
    with col1:
        fig = px.bar(vendas_vendedor,
            x='valor_venda',
            y='nome_vendedor',
            text='valor_venda',
            labels={'valor_venda':"Valor Vendas(R$)"},
            template='plotly_dark'
        )
        st.subheader('👥**Faturamento por Vendedor**')
        st.plotly_chart(fig, use_container_width=True)


    with col3:
        fig = px.bar(
            vendas_mes,
            x='mes_nome',
            y='valor_venda',
            text='valor_venda',
            labels={'mes_nome': 'Mês', 'valor_venda': 'Total de Vendas (R$)'},
            template='plotly_dark'
        )
        st.subheader(' Faturamento por Mês')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        fig = px.bar(
            vendas_loja,
            x='cod_loja',
            y='Qtd_Vendas',
            text='Qtd_Vendas',
            labels={'Qtd_Vendas': 'Quantidade'},
            template='plotly_dark'
        )
        st.subheader('🏬 Quantidade de Vendas por Loja')
        st.plotly_chart(fig, use_container_width=True)    

    with col3:
        grafico_linha['ano'] = grafico_linha['ano'].astype(str)
        st.subheader('Tendência das Váriaveis')
        st.line_chart( grafico_linha.set_index('ano')[['Faturamento', 'Qtde_vendas', 'Ticket']], height=350
            
    )
        
    corr = grafico_linha[['ano','Faturamento','Qtde_vendas','Ticket']].corr()
    with col1:

        if len(grafico_linha) > 1:
            corr = grafico_linha[['ano','Faturamento','Qtde_vendas','Ticket']].corr()
            st.subheader('Correlação entre Váriaveis')
            st.dataframe(corr.style.background_gradient(cmap='Blues'))
            st.markdown("""
    #### 🔗 Correlação Entre Variáveis
    ##### A matriz abaixo mostra o grau de relação entre os indicadores.  Valores próximos de 1 ou -1 indicam forte correlação positiva ou negativa. Por exemplo, uma correlação negativa entre **ano** e **ticket médio** sugere que, com o passar dos anos, o valor médio por venda caiu.
    """)

        else:
            st.subheader("Indicadores do Ano Selecionado")
            st.dataframe(grafico_linha[['ano','Faturamento','Qtde_vendas','Ticket']])
            st.write("#### Como não é possivel mostrar a correlação somente de um ano, vou mostrar o total dos indicadores" )
        
    with col3:
        with st.expander("Gráfico de Tendência"):
            st.markdown("""
    #### Evolução Anual
    ##### Este gráfico mostra a evolução do faturamento, quantidade de vendas e ticket médio ao longo dos anos. Observe como o volume de vendas cresce, enquanto o ticket médio apresenta queda — indicando uma possível mudança na estratégia comercial ou perfil de cliente.
    """)