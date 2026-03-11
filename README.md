# Dashboard de Vendas com Python e Streamlit

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat&logo=pandas)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=flat&logo=plotly)](https://plotly.com/)

> Dashboard interativo para análise de vendas, permitindo explorar faturamento, volume de vendas e desempenho comercial através de filtros dinâmicos.

---

# Preview da Aplicação

<div align="center">
  <img src="preview.png"/>
</div>

---

---

# 🌐 Acesso à Aplicação

Você pode acessar o dashboard online através do Streamlit:

🔗 **Link da aplicação:**  
https://seu-link-do-streamlit.streamlit.app

---

Caso prefira executar localmente, siga as instruções na seção **Como Executar o Projeto**.

## 🎯 Sobre o Projeto

Este projeto consiste em um **Dashboard de Análise de Vendas desenvolvido com Python e Streamlit**, permitindo explorar dados comerciais de forma interativa.

A aplicação possibilita analisar **indicadores de desempenho de vendas entre 2012 e 2015**, oferecendo filtros dinâmicos para facilitar a exploração dos dados.

O objetivo é transformar dados brutos em **informações estratégicas para tomada de decisão**, permitindo visualizar tendências, desempenho de vendedores, segmentos e lojas.

---

## 🚀 Funcionalidades

### 📊 Indicadores Principais
- **Faturamento Total**
- **Quantidade de Vendas**
- **Ticket Médio**
- **Quantidade de Produtos Vendidos**

Todos os indicadores são **atualizados automaticamente conforme os filtros aplicados**.

---

### 🔎 Filtros Interativos

A aplicação permite filtrar os dados por:

- Intervalo de **datas**
- **Estado da loja**
- **Categoria do produto**
- **Ano**
- **Mês**

Isso permite análises específicas por período ou região.

---

### 📈 Visualizações de Dados

O dashboard apresenta diversos gráficos interativos:

#### 💰 Faturamento por Segmento
Gráfico de rosca mostrando a participação de cada segmento no faturamento total.

#### 👥 Faturamento por Vendedor
Gráfico de barras com o desempenho dos vendedores.

#### 📅 Faturamento por Mês
Análise da distribuição de vendas ao longo do ano.

#### 🏬 Vendas por Loja
Quantidade total de vendas realizadas por cada loja.

#### 📉 Tendência de Indicadores
Gráfico de linha mostrando a evolução de:
- Faturamento
- Quantidade de vendas
- Ticket médio

---

### 🔗 Análise de Correlação

O dashboard também apresenta uma **matriz de correlação entre indicadores**, permitindo analisar relações entre:

- Ano
- Faturamento
- Quantidade de vendas
- Ticket médio

Isso ajuda a identificar padrões como crescimento de vendas ou mudanças no comportamento de consumo.

---

## 🎨 Interface Personalizada

A aplicação possui uma interface customizada com:

- **CSS personalizado no Streamlit**
- Layout **wide (tela cheia)**
- **Cards de indicadores estilizados**
- Sidebar com **filtros dinâmicos**

O objetivo é oferecer uma experiência visual mais próxima de ferramentas profissionais de BI.

---

## 🛠️ Stack Tecnológica

### Core
- **Python 3.10+**
- **Streamlit**
- **Pandas**

### Visualização de Dados
- **Plotly Express**
- **Plotly Graph Objects**
- **Altair**

### Manipulação de Dados
- **OpenPyXL**
- **Pandas**

---

## 📂 Estrutura Esperada do Dataset

O dashboard utiliza um arquivo Excel com informações de vendas.

Principais colunas esperadas:

```
data_venda
valor_venda
estado_loja
categoria_produto
nome_vendedor
cod_loja
segmento_produto
cod_produto
nome_produto
```

---

## ▶️ Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seuusuario/dashboard-vendas-streamlit.git
cd dashboard-vendas-streamlit
```

---

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Executar a aplicação

```bash
streamlit run app.py
```

---

## 📊 Possíveis Extensões

Algumas melhorias futuras para o projeto:

- Upload de dataset direto pelo usuário
- Adicionar **mapa de vendas por estado**
- Implementar **forecast de vendas**
- Conectar com **banco de dados SQL**
- Deploy em **Streamlit Cloud**

---

