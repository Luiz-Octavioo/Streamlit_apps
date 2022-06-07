# -------------------------------------------------------------------------------#
# -----------------------------Streamlit Dashboard-------------------------------#
# Create by: Luiz Octavio                                                        #
# LAB: Grupo de Pesquisa em Interação Biosfera-Atmosfera                         #
# Universidade Federal do Estado de Mato Grosso                                  #
# Mestre e Doutorando no Programa de Pós Graduação em Fisica Ambiental           #
# Cuiabá, Mato Grosso                                                            #
#                                                                                #
#                                                                                #
#                                                                                #
# Version: 0.1                                                                   #
# Contato:luizpgfa@gmail.com | luizoctavio@fisica.ufmt.br                        #
# Lattes: http://lattes.cnpq.br/0811571185673375                                 #
# -------------------------------------------------------------------------------#


# import libs
import pandas as pd
import plotly.express as px
import streamlit as st

# set to wide mode
st.set_page_config(layout="wide")
# Get dataframe with streamlit
header = st.container()
user_input = st.container()
output_graphs = st.container()
author_credits = st.container()


# Create dashboard to show the table data and the graph

###############################################################################
# Prepare the data
# get all files in the folder
files = ['%_do_IndArtigo_dos_30%_dos_DPs_mais_produtivos.xlsx', 'DP_Orientacao_docente_andamento.xlsx',
         'DP_Orientacao_docente_concluida.xlsx',
         'DPs_Turmas_ministradas.xlsx', 'Media_capitulo_livro_por_DPs_por_ano.xlsx',
         'Media_de_artigos_B1_A1_A2_B1_com_discentes_DPs.xlsx',
         'Media_de_artigos_B1_A1_A2_B1_dos_DPs_por_ano.xlsx', 'Media_de_cursos_de_curta_duração_dos_DPs_por_ano.xlsx',
         'Media_de_livros_publicados_dos_Dps_por_ano.xlsx', 'Media_de_organizações_de_eventos_dos_DPs_por_ano.xlsx',
         'Media_de_produtos_de_editoria_dos_DPs_por_ano.xlsx',
         'Media_de_registros_patentes_DPs_por_ano.xlsx',
         'Media_ponderada_de_artigos_IndArtigo_com_discentes_por_DPs_por_ano.xlsx',
         'Media_ponderada_de_artigos_IndArtigo_por_DPs_por_ano.xlsx',
         'Percentual_de_DP_com_artigo_B1_A1_A2_B1_por_ano.xlsx']

# print(files)

# lista com os titulos
titles = ['% do IndArtigo_dos_30%_dos_DPs_mais_produtivos', 'DP_Orientacao_docente_andamento',
          'DP_Orientacao_docente_concluida',
          'DPs_Turmas_ministradas', 'Média_capitulo_livro_por_DPs_por_ano',
          'Média_de_artigos_B1(A1, A2 e B1)_com_discentes_DPs',
          'Média_de_artigos_B1(A1, A2 e B1)_dos_DPs_por_ano', 'Média_de_cursos_de_curta_duração_dos_DPs_por_ano',
          'Média_de_livros_publicados_dos_Dps_por_ano', 'Média_de_organizações_de_eventos_dos_DPs_por_ano',
          'Média_de_produtos_de_editoria_dos_DPs_por_ano',
          'Média_de_registros_patentes_DPs_por_ano',
          'Média_ponderada_de_artigos_IndArtigo_com_discentes_por_DPs_por_ano',
          'Média_ponderada_de_artigos_IndArtigo_por_DPs_por_ano', 'Percentual_de_DP_com_artigo_B1(A1, A2 e B1)_por_ano']

# git_path = 'https://github.com/Luiz-Octavioo/Streamlit_apps/raw/main/Dados/'
path = 'Dados/'

# Load data from files
# @st.cache(allow_output_mutation=True)
def load_data():
    dataframes = []
    for file in files:
        df = pd.read_excel(path+file, sheet_name="Planilha1")
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

with header:
    st.title("Indicadores sobre os Programas de Pós-Graduação conceito 4 da CAPES (2017-2020).")

# SIDEBAR
with user_input:
    st.sidebar.header('Seleção do Usuário')
    a = st.sidebar.selectbox("Por favor Selecione o Indicador", titles_split_join)
    dataframe = get_df(a)

    # Get the index of the FA/UFMT/MT
    idx_FA = get_index(dataframe)

    # subtitle
    st.subheader(a)

    # highlight the FA/UFMT/MT in dataframe
    color = (dataframe['PPG_Acrony'] == 'FA/UFMT/MT').map({True: 'background-color: firebrick', False: ''})


    # show dataframe and hide the index
    st.dataframe(dataframe.style.apply(lambda x: color))


# if theme of streamlit is dark, change the color of the chart


# GRAPHS
with output_graphs:
    st.header('Gráfico sobre o Indicador:')
    # Plotly if dark mode
    if st.checkbox('Modo escuro', value=True):
        fig = px.bar(dataframe, x='PPG_Acrony', y='INDICADOR', color='INDICADOR',
                     hover_data=['PPG', 'IES', 'UF', 'INDICADOR'],
                     color_continuous_scale='Reds', template='plotly_dark')

    else:
        fig = px.bar(dataframe, x='PPG_Acrony', y='INDICADOR', color='INDICADOR',
                     hover_data=['PPG', 'IES', 'UF', 'INDICADOR'],
                     color_continuous_scale='Reds', template='plotly_white')

        # Change color background
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False)) # plot_bgcolor="white", paper_bgcolor="white"

    # add labels and center titles
    fig.update_layout(title_text=a + ' (2017-2020)', xaxis_title='Programa de Pós-Graduação', yaxis_title='')

    # Rotate x-axis labels
    fig.update_layout(xaxis_tickangle=-45)

    # add annotations to idx_FA
    fig.add_annotation(
        x=dataframe.iloc[idx_FA]['PPG_Acrony'],
        y=dataframe.iloc[idx_FA]['INDICADOR'],
        text='Física Ambiental',
        showarrow=True,  # props arrow
        arrowhead=7,
        arrowsize=2,
        arrowwidth=1,
        arrowcolor='black',
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="white"
        ),
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
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'responsive': False})

# add figure to st.markdown in bottom left corner page
path_fig = 'https://pgfa.ufmt.br/images/logo-pgfa-v4.png'
st.markdown(f'<img src="{path_fig}" alt="logo" style="width:450px;height:100px;">', unsafe_allow_html=True)