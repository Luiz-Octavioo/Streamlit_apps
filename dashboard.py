# import libs
import pandas as pd
import plotly.express as px
import streamlit as st
import os

# set dir
os.chdir('C:/Users/Luiz/OneDrive/Documentos/Marcelao/PGFA/AutoAvaliacao')

# Create dashboard to show the table data and the graph

###############################################################################
# Prepare the data
# get all files in the folder
files = ['%_do_IndArtigo_dos_30%_dos_DPs_mais_produtivos.xlsx', 'DP_Orientacao_docente_andamento.xlsx', 'DP_Orientacao_docente_concluida.xlsx',
         'DPs_Turmas_ministradas.xlsx', 'Média_capitulo_livro_por_DPs_por_ano.xlsx', 'Média_de_artigos_B1_A1_A2_B1_com_discentes_DPs.xlsx',
         'Média_de_artigos_B1_A1_A2_B1_dos_DPs_por_ano.xlsx', 'Média_de_cursos_de_curta_duração_dos_DPs_por_ano.xlsx',
         'Média_de_livros_publicados_dos_Dps_por_ano.xlsx', 'Média_de_organizações_de_eventos_dos_DPs_por_ano.xlsx', 'Média_de_produtos_de_editoria_dos_DPs_por_ano.xlsx',
         'Média_de_registros_patentes_DPs_por_ano.xlsx', 'Média_ponderada_de_artigos_IndArtigo_com_discentes_por_DPs_por_ano.xlsx',
         'Média_ponderada_de_artigos_IndArtigo_por_DPs_por_ano.xlsx', 'Percentual_de_DP_com_artigo_B1_A1_A2_B1_por_ano.xlsx']

print(files)

# lista com os titulos
titles = ['% do IndArtigo_dos_30%_dos_DPs_mais_produtivos', 'DP_Orientacao_docente_andamento', 'DP_Orientacao_docente_concluida',
         'DPs_Turmas_ministradas', 'Média_capitulo_livro_por_DPs_por_ano', 'Média_de_artigos_B1_A1_A2_B1_com_discentes_DPs',
         'Média_de_artigos_B1_A1_A2_B1_dos_DPs_por_ano', 'Média_de_cursos_de_curta_duração_dos_DPs_por_ano',
         'Média_de_livros_publicados_dos_Dps_por_ano', 'Média_de_organizações_de_eventos_dos_DPs_por_ano', 'Média_de_produtos_de_editoria_dos_DPs_por_ano',
         'Média_de_registros_patentes_DPs_por_ano', 'Média_ponderada_de_artigos_IndArtigo_com_discentes_por_DPs_por_ano',
         'Média_ponderada_de_artigos_IndArtigo_por_DPs_por_ano', 'Percentual_de_DP_com_artigo_B1_A1_A2_B1_por_ano']


# Load data from files
def load_data():
    dataframes = []
    for file in files:
        df = pd.read_excel(file, sheet_name="Planilha1")
        dataframes.append(df)
    return dataframes


# load all data
dfs = load_data()
# print(dfs)

# organize dataframes
dfs_organized = []
for df in dfs:
    PPGS = []
    for i in df['PPG']:
        if i.find(' ') != -1:
            x = i.split(' ')[0][0] + i.split(' ')[1][0]
            # print(letters)
        PPGS.append(x)
    # Create a new column with the PPG
    df['PPG_Acrony'] = PPGS
    # Combine with other columns
    df['PPG_Acrony'] = df['PPG_Acrony'] + '/' + df['IES'] + '/' + df['UF']
    # Remove all elements in list PPGS
    PPGS.clear()
    # print(df)
    dfs_organized.append(df)

# sep each value list by _
titles_split = []
for i in titles:
    titles_split.append(i.split('_'))

# join each value list by ' '
titles_split_join = []
for i in titles_split:
    titles_split_join.append(' '.join(i))

# Insert the titles in the dataframe
dfs_organizedI = []
for df, title in zip(dfs_organized, titles_split_join):
    df['Title'] = title
    dfs_organizedI.append(df)


# get FA/UFMT/MT index
def get_index(df):
    idx_FA = df[df['PPG_Acrony'] == 'FA/UFMT/MT'].index
    idx_FA = df.index[idx_FA[0]]
    return idx_FA


# Create function to get the dataframe to start the dashboard
# find dataframe by title
def get_df(title):
    for df in dfs_organizedI:
        if df['Title'][0] == title:
            return df.drop(df.columns[[4, 8]], axis=1)

# print(dfs_organizedI)

##############################################################################
# DASHBOARD
# set to wide mode
st.set_page_config(layout="wide")
# Get dataframe with streamlit
header = st.container()
user_input = st.container()
output_graphs = st.container()
author_credits = st.container()



with header:
    st.title("Analise de dados sobre os Programas de Pós-Graduação")

# SIDEBAR
with user_input:
    st.sidebar.header('Seleção do Usuário')
    a = st.sidebar.selectbox("Por favor Selecione o Indicador", titles_split_join)
    dataframe = get_df(a)

    # Get the index of the FA/UFMT/MT
    idx_FA = get_index(dataframe)

    # subtitle
    st.subheader(a)

    # show dataframe
    st.dataframe(dataframe)

# GRAPHS
with output_graphs:
    st.header('Gráficos')
    # Plotly
    fig = px.bar(dataframe, x='PPG_Acrony', y='INDICADOR', color='INDICADOR',
                 hover_data=['PPG', 'IES', 'UF', 'INDICADOR'],
                 color_continuous_scale='magma', template='plotly_dark')

    # add labels and center titles
    fig.update_layout(title_text=a, xaxis_title='Programa de Pós-Graduação', yaxis_title='')
    # fig.update_layout(title_x=0.5)

    # add annotations to idx_FA
    fig.add_annotation(
        x=dataframe.iloc[idx_FA]['PPG_Acrony'],
        y=dataframe.iloc[idx_FA]['INDICADOR'],
        text='Física Ambiental',
        showarrow=True,  # props arrow
        arrowhead=7,
        arrowsize=2,
        arrowwidth=1,
        arrowcolor='white',
        xref='x',
        yref='y',
        align='center',
        font_size=14,
        bgcolor='#900C3F',
        opacity=1
    )

    # align plot in center of page
    fig.update_layout(height=600, width=900)

    # show plot and change location to displayModeBar
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'responsive': True})

# AUTHOR CREDITS
with author_credits:
    st.header('Créditos')
    st.markdown("""
    #### Por: [Luiz Octávio](http://lattes.cnpq.br/0811571185673375)
    """, unsafe_allow_html=True)
