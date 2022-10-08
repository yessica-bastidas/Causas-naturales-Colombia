# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 17:31:33 2022


"""

# CARGAR LIBRERIAS
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64

# CARGAR LA BASE
df = pd.read_csv('base_datos.csv') # base 
df.columns = df.columns.map(str.lower) # convertir en minusculas las columnas
df['fecha'] = pd.to_datetime(df['fecha'], format = '%Y/%m/%d') # convertir fecha en formato datetime
#st.text(df) # visualizar base de datos


# DASHBOARD

st.set_page_config(layout="wide")


# Título principal
st.markdown("<h1 style='text-align: center; color: green;'>Afectación a las personas por diferentes causas naturales en 2018, 2019 y 2020 🌎</h1>", unsafe_allow_html=True)

# Función para descargar base de datos
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

#----------------------------------------
selected = option_menu(
    menu_title =None,
    options=["Introducción", "Personas", "Viviendas","Conclusiones"],
    icons=["book","person","house"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "icon":{"font-size":"25px"},
        "nav-link-selected":{"background-color":"orange"}}
    )
    
if selected == "Introducción":
    st.title("Introducción")
    st.markdown("<h4 style= color: black;'> Se analiza el tipo de afectación a las personas por diferentes causas naturales registrados por la Unidad Nacional para la Gestión del Riesgo de Desastres (UNGRD), ocurridos en Colombia entre los años 2018, 2019 y 2020. Debido a los recientes fenómenos naturales que han causado situaciones de emergencia en distintas localidades del país, dejando muchas personas afectadas. El objetivo de este estudio es identificar las zonas con mayor número de personas damnificadas dependiendo de los tipos de eventos y poder realizar una hipótesis que ayuden a la disminución de víctimas.</h4>", unsafe_allow_html= True)

    c20,c21,c22 = st.columns((1,1,1)) # Se divide la columna en 3 para agregar las imagenes
    with c20:
        st.image("https://cdn.pixabay.com/photo/2017/02/27/08/50/cyclone-2102397_960_720.jpg",
             width=300)
    with c21:
        st.image("https://cdn.pixabay.com/photo/2013/06/09/09/07/explosion-123690_960_720.jpg",
             width=300)
    with c22:
        st.image("https://cdn.pixabay.com/photo/2012/10/26/01/19/hurricane-63005_960_720.jpg",
            width=300)
    st.markdown("Elaborador por: Yessica Bastidas, Santiago Bustos, Juan Diego Correa y Juan Carlos Gómez.")

if selected == "Personas":
    st.title("Personas")
    
    # Indicadores
    c1, c2, c3, c4= st.columns((1,1,1,1)) # Dividir el ancho en 4 columnas de igual tamaño

    #---------------Fallecidos
    c1.markdown("<h3 style='text-align: left; color: gray;'> Fallecidos </h3>", unsafe_allow_html=True)

    fallecidos = round(df['fallecidos'].sum()) #Total de personas fallecidas

    c1.text('Total: '+str(fallecidos))

    #---------------Afectados
    c2.markdown("<h3 style='text-align: left; color: gray;'> Afectados </h3>", unsafe_allow_html=True)

    afectados = df['afectados'].sum()  #Total de personas afectadas

    c2.text('Total: '+str(afectados))

    #---------------Heridos
    c3.markdown("<h3 style='text-align: left; color: gray;'> Heridos </h3>", unsafe_allow_html=True)

    heridos = df['heridos'].sum() #Total de personas heridas

    c3.text('Total: '+str(heridos))

    #---------------Desaparecidos
    c4.markdown("<h3 style='text-align: left; color: gray;'> Desaparecidos </h3>", unsafe_allow_html=True)

    desaparecidos = df['desaparecidos'].sum()  #Total de personas desaparecidas

    c4.text('Total: '+str(desaparecidos))
    
    #----------------------------------------
    #SECCIÓN 1
    st.markdown("<h3 style='text-align: center; color: green;'>¿Cuántos afectados hubo por cada departamento de Colombia?</h3>", unsafe_allow_html= True)
    
    #Agrupar por departamentos el número de personas afectadas
    df1 = df.groupby(['departamento'])[['afectados']].sum().reset_index().sort_values('afectados', ascending = False)
    
    # crear gráfica
    fig = px.bar(df1, x='departamento',y='afectados', barmode= 'group', text_auto='.2s',
                 color_discrete_sequence=px.colors.qualitative.Set3,
                 width=1250,height=500)
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Departamento',
        yaxis_title = 'Cantidad de personas afectadas',
        template = 'simple_white',
        title_x = 0.5)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    st.plotly_chart(fig)
    #----------------------------------------
    #SECCIÓN 2
    st.markdown("<h3 style='text-align: center; color: green;'>Principales eventos en los departamentos con mayor personas afectadas</h3>", unsafe_allow_html= True)
    
    c5, c6, c7 = st.columns((1,1,1)) # Dividir el ancho en 3 columnas de igual tamaño
    
    #---------Chocó
    c5.markdown("<h3 style='text-align: center; color: black;'>Top 5 en Choco</h3>", unsafe_allow_html= True)
    
    # Crear la base de datos filtrando por chocó y luego agrupando por el tipo de evento
    df2 = df[df['departamento'].isin(['CHOCO'])]
    df2 = df2.groupby(['tipo_de_evento'])[['afectados']].sum().reset_index().sort_values('afectados', ascending = False).head(5)
    
    num = df2['afectados'].head(5).sum()
    
    # crear gráfica:
    fig = px.pie(df2 , values = 'afectados', names = 'tipo_de_evento', hole = .5,
                 color_discrete_sequence=px.colors.qualitative.Light24,
                 width=420)
    
    # agregar detalles a la gráfica:
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b>Evento<b>',
        title_x = 0.5,
        annotations = [dict(text = str(num), x=0.5, y = 0.5, font_size = 20, showarrow = False )])
    
    c5.plotly_chart(fig)
    

    #---------La Guajira
    c6.markdown("<h3 style='text-align: center; color: black;'>Top 5 en la Guajira</h3>", unsafe_allow_html= True)
    
    # Crear la base de datos filtrando por la guaira y luego agrupando por el tipo de evento
    df3 = df[df['departamento'].isin(['LA GUAJIRA'])]
    df3 = df3.groupby(['tipo_de_evento'])[['afectados']].sum().reset_index().sort_values('afectados', ascending = False).head(5)
    
    num = df3['afectados'].head(5).sum()

    # crear gráfica:
    fig = px.pie(df3 , values = 'afectados', names = 'tipo_de_evento', hole = .5,
                 color_discrete_sequence=px.colors.qualitative.Light24,
                 width=400)
    
    # agregar detalles a la gráfica:
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b>Evento<b>',
        title_x = 0.5,
        annotations = [dict(text = str(num), x=0.5, y = 0.5, font_size = 20, showarrow = False )])
    
    c6.plotly_chart(fig)
    
    #---------Bolivar
    c7.markdown("<h3 style='text-align: center; color: black;'>Top 5 en Bolivar</h3>", unsafe_allow_html= True)
    
    # Crear la base de datos filtrando por bolivar y luego agrupando por el tipo de evento
    df4 = df[df['departamento'].isin(['BOLIVAR'])]
    df4 = df4.groupby(['tipo_de_evento'])[['afectados']].sum().reset_index().sort_values('afectados', ascending = False).head(5)
    
    num = df4['afectados'].head(5).sum()
    
    # crear gráfica:
    fig = px.pie(df4 , values = 'afectados', names = 'tipo_de_evento', hole = .5,
                 color_discrete_sequence=px.colors.qualitative.Light24,
                 width=420)
    
    # agregar detalles a la gráfica:
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b>Evento<b>',
        title_x = 0.5,
        annotations = [dict(text = str(num), x=0.5, y = 0.5, font_size = 20, showarrow = False )])
    
    c7.plotly_chart(fig)

    #----------------------------------------------------------------------
    #SECCIÓN 3
    
    st.markdown("<h3 style='text-align: center; color: green;'>¿En qué mes hay más inundaciones?</h3>", unsafe_allow_html= True)
    
    c8, c9 = st.columns((1,1))
    
    # Crear base de datos con el mes
    c8.markdown("<h3 style='text-align: center; color: black;'>Chocó</h3>", unsafe_allow_html= True)
    
    #-------Chocó
    # Se filtra por tipo de evento inundación, departamento chocó y se agrupa por mes
    df0 = df[['fecha','departamento','tipo_de_evento','afectados']]
    df0 = df0[df0['tipo_de_evento'].isin(['INUNDACION'])]
    df0 = df0[df0['departamento'].isin(['CHOCO'])]
    df0['fecha'] = df0['fecha'].dt.month
    
    df0=df0.groupby(['fecha'])[['afectados']].sum().reset_index()
    
    # crear gráfica
    fig = px.bar(df0, x='fecha',y='afectados', barmode= 'group',
                 color_discrete_sequence=px.colors.qualitative.Light24,
                 text_auto='.2s',
                 width=650,height=400)
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Mes',
        yaxis_title = 'Cantidad de personas afectadas',
        template = 'simple_white',
    legend_title = '<b>Evento<b>',
        title_x = 0.5)
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    c8.plotly_chart(fig)
    
    #-----Demás departamentos
    c9.markdown("<h3 style='text-align: center; color: black;'>Demás departamentos</h3>", unsafe_allow_html= True)
    
    # Se filtra por tipo de evento inundación, todos los departamentos excluyendo Chocó y se agrupa por mes
    df0 = df[['fecha','departamento','tipo_de_evento','afectados']]
    df0 = df0[df0['tipo_de_evento'].isin(['INUNDACION'])]
    df0 = df0[df0['departamento'].isin(['AMAZONAS','ANTIOQUIA','ARAUCA','ATLANTICO','BOLIVAR','BOYACA','CALDAS','CAQUETA',
                                        'CASANARES','CAUCA','CESAR','CORDOBA','CUNDINAMARCA','GUAINIA','GUAVIARE','HUILA','LA GUAJIRA',
                                        'MAGDALENA','META','NARIÃ‘O','NORTE DE SANTANDER','PUTUMAYO','QUINDIO','RISARALDA','SAN ANDRES',
                                        'SANTANDER','SUCRE','TOLIMA','VALLE DEL CAUCA','VAUPES','VICHADA'])]
    df0['fecha'] = df0['fecha'].dt.month
    df0=df0.groupby(['fecha'])[['afectados']].sum().reset_index()
    
    # crear gráfica
    fig = px.bar(df0, x='fecha',y='afectados', barmode= 'group',
                 color_discrete_sequence=px.colors.qualitative.Light24,
                 text_auto='.2s',
                 width=650,height=400)
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Mes',
        yaxis_title = 'Cantidad de personas afectadas',
        template = 'simple_white',
        legend_title = '<b>Evento<b>',
        title_x = 0.5)
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    c9.plotly_chart(fig)
    #------------------------------
    #GRAFICA 4

    st.markdown("<h3 style='text-align: center; color: green;'>¿Cuáles son los eventos que más causan personas heridas?</h3>", unsafe_allow_html= True)
    c12, c13 = st.columns((2,1)) # Dividir el ancho en 2 columnas de igual tamaño

    # crear base 
    df0 = df.groupby(['tipo_de_evento'])[['heridos']].sum().sort_values('heridos', ascending = False).rename(columns={'heridos':'counts'})
    df0['ratio'] = df0.apply(lambda x: x.cumsum()/df0['counts'].sum())

    # definir figura
    fig = go.Figure([go.Bar(x=df0.index, y=df0['counts'], yaxis='y1', name='sessions id'),
                     go.Scatter(x=df0.index, y=df0['ratio'], yaxis='y2', name='Heridos', hovertemplate='%{y:.1%}', marker={'color': 'black'})])

    # agregar detalles
    fig.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                      title={'text': '<b> Heridos por tipo de evento<b>', 'x': .5}, 
                      yaxis={'title': 'Heridos'},
                      yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]})

    c12.plotly_chart(fig)

    # Hacer un checkbox
    if st.checkbox('Obtener datos por evento y departamento', False):
        
        # Código para generar el DataFrame
        df0 = df.groupby(['tipo_de_evento','departamento'])[['heridos']].sum().reset_index().sort_values('heridos', ascending = False).rename(columns={'tipo_de_evento':'evento'})
        
        # Código para convertir el DataFrame en una tabla plotly resumen
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df0.columns),
            fill_color='lightblue',
            line_color='darkslategray'),
            cells=dict(values=[df0.evento, df0.departamento, df0.heridos],fill_color='white',line_color='lightgrey'))
           ])

        fig.update_layout(width=500, height=550)
        

    # Enviar tabla a streamlit
        c13.write(fig)

    #----------------------------------------------------
    #SECCIÓN 5
    st.markdown("<h3 style='text-align: center; color: green;'>🔥 Damnificados por cada tipo de incendio 🔥</h3>", unsafe_allow_html= True)

    c14, c15, c16 = st.columns((1,1,1)) # Dividir el ancho en 3 columnas de igual tamaño

    #---heridos

    # Crear la base de datos filtrando por los 4 tipos de incendio
    base2 = df[df['tipo_de_evento'].isin(['INCENDIO DE COBERTURA VEGETAL','INCENDIO FORESTAL','INCENDIO ESTRUCTURAL','INCENDIO'])]

    # crear gráfica:
    fig = px.pie(base2 , values = 'afectados', names = 'tipo_de_evento', title = '<b>% Personas afectadas<b>',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 width = 420)

    # agregar detalles a la gráfica:
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b>Tipo de incendio<b>',
        title_x = 0.5)

    c14.plotly_chart(fig)

    #----fallecidos

    # Crear la base de datos filtrando por los 4 tipos de incendio
    base2 = df[df['tipo_de_evento'].isin(['INCENDIO DE COBERTURA VEGETAL','INCENDIO FORESTAL','INCENDIO ESTRUCTURAL','INCENDIO'])]

    # crear gráfica:
    fig = px.pie(base2 , values = 'fallecidos', names = 'tipo_de_evento', title = '<b>% Personas fallecidas<b>',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 width = 420)

    # agregar detalles a la gráfica:
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b>Tipo de incendio<b>',
        title_x = 0.5)

    c15.plotly_chart(fig)

    #----afectados

    # Crear la base de datos filtrando por los 4 tipos de incendio
    base2 = df[df['tipo_de_evento'].isin(['INCENDIO DE COBERTURA VEGETAL','INCENDIO FORESTAL','INCENDIO ESTRUCTURAL','INCENDIO'])]

    # crear gráfica:
    fig = px.pie(base2 , values = 'heridos', names = 'tipo_de_evento', title = '<b>% Personas heridas<b>',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 width = 420)

    # agregar detalles a la gráfica:
    fig.update_layout(
        template = 'simple_white',
        legend_title = '<b>Tipo de incendio<b>',
        title_x = 0.5)

    c16.plotly_chart(fig)
    
    #------------------------------
    #SECCIÓN 6
    
if selected == "Viviendas":
    st.title("Viviendas")
    
    
    st.markdown("<h3 style='text-align: center; color: green;'>Eventos que causaron viviendas destruidas 🌪️</h3>", unsafe_allow_html= True)
    
    c10, c11 = st.columns((1,1))
    
    #---- Viviendas destruidas
    
    casas=df[['fecha','viviendas_destruidas']]
    casas['fecha']=casas['fecha'].dt.month
    casas=casas.groupby(['fecha'])[['viviendas_destruidas']].sum().reset_index()
    
    # Crear grafica
    fig = px.bar(casas, x = 'fecha', y='viviendas_destruidas',title = '<b>Viviendas destruidas<b>',barmode= 'group', text_auto='.2s',
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 width = 700, height=350)
    
    fig.update_layout(
        xaxis_title = 'Fecha',
        yaxis_title = 'Número viviendas',
        template = 'simple_white',
        title_x = 0.5)
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    c11.plotly_chart(fig)
    
    # Hacer un checkbox
    if st.checkbox('Obtener datos por vivienda, evento y mes', False):
        
        # Código para generar el DataFrame
        df0 = df.groupby(['tipo_de_evento','fecha','departamento'])[['viviendas_destruidas']].sum().reset_index().rename(columns={'tipo_de_evento':'evento','fecha':'mes','viviendas_destruidas':'destruidas'}).sort_values('destruidas', ascending = False)
        df0['mes'] = df0['mes'].dt.month
        # Código para convertir el DataFrame en una tabla plotly resumen
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df0.columns),
            fill_color='lightblue',
            line_color='darkslategray'),
            cells=dict(values=[df0.evento,df0.mes,df0.departamento, df0.destruidas],fill_color='white',line_color='lightgrey'))
           ])
        fig.update_layout(width=600, height=400)
    
    # Enviar tabla a streamlit
        c10.write(fig)    
        
    #---- Viviendas averiadas
    st.markdown("<h3 style='text-align: center; color: green;'>Eventos que causaron viviendas averiadas 🏡</h3>", unsafe_allow_html= True)

    c12, c13 = st.columns((1,1))
    
    casas=df[['fecha','viviendas_averiadas']]
    casas['fecha']=casas['fecha'].dt.month
    casas=casas.groupby(['fecha'])[['viviendas_averiadas']].sum().reset_index()
    
    
    # crear grafica
    fig = px.bar(casas, x = 'fecha', y='viviendas_averiadas',title = '<b>Viviendas averiadas<b>',barmode= 'group', text_auto='.2s',
                 color_discrete_sequence=px.colors.qualitative.Pastel1,
                 width = 700, height=350)

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Fecha',
        yaxis_title = 'Número viviendas',
        template = 'simple_white',
        title_x = 0.5)
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    c12.plotly_chart(fig)
    
    # Hacer un checkbox
    if st.checkbox('Obtener datos por vivienda afectada, evento y mes', False):
        
        # Código para generar el DataFrame
        df0 = df.groupby(['tipo_de_evento','fecha','departamento'])[['viviendas_averiadas']].sum().reset_index().rename(columns={'tipo_de_evento':'evento','fecha':'mes','viviendas_averiadas':'averiadas'}).sort_values('averiadas', ascending = False)
        df0['mes'] = df0['mes'].dt.month
        # Código para convertir el DataFrame en una tabla plotly resumen
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df0.columns),
            fill_color='lightpink',
            line_color='darkslategray'),
            cells=dict(values=[df0.evento,df0.mes,df0.departamento, df0.averiadas],fill_color='white',line_color='lightgrey'))
           ])
        fig.update_layout(width=600, height=400)
    
    # Enviar tabla a streamlit
        c13.write(fig)    
    
    
#------------------------------------------------------------  
    #SECCIÓN 7
    
    st.markdown("<h3 style='text-align: center; color: green;'>Relación entre las viviendas damnificadas por las inundaciones (Top 10)</h3>", unsafe_allow_html= True)
    
    # Se agrupa por evento y departamento, luegos se suman las columnas de viviendas destruidas, averiadas y afectados
    df0=df.groupby(['tipo_de_evento','departamento']).agg(
        destruidas = ('viviendas_destruidas','sum'),
        averiadas = ('viviendas_averiadas','sum'),
        afectados = ('afectados','sum')
        ).reset_index().sort_values('afectados', ascending = False).head(10)
    df0 = df0[df0['tipo_de_evento']=='INUNDACION'] # Filtrar DataFrame
    
    # definir gráfica
    fig = px.scatter(df0, x = 'destruidas', y ='averiadas', color = 'departamento',
                     width = 1300, height=450, size = 'afectados')

    # añadir atributos
    fig.update_layout(
        xaxis_title = '<b>Viviendas destruidas<b>',
        yaxis_title = '<b>Viviendas averiadas<b>',
        template = 'simple_white',
        title_x = 0.5,
        legend_title = '<b> Departamento <b>')
    st.plotly_chart(fig)
#------------------------------------------------------------ 
    #SECCIÓN 8
    
if selected == "Conclusiones":
    st.title("Conclusiones")
    
    c30,c31 = st.columns((2,1))
    
    c30.markdown("<h4 style= color: black;'> ✔️ Choco, La Guajira y Bolivar fueron los departamentos con mas personas afectadas debido a las inundaciones.</h4>", unsafe_allow_html= True)
    c30.markdown("<h4 style= color: black;'> ✔️ En el mes de noviembre (11), se presenta el mayor numero de personas afectadas por estas inundaciones, afectando la vivienda de los colombianos.</h4>", unsafe_allow_html= True)
    c30.markdown("<h4 style= color: black;'> ✔️ Los eventos que causan mas personas heridas, son accidente de transporte terrestre, incendio estructural y explosion.</h4>", unsafe_allow_html= True)
    c30.markdown("<h4 style= color: black;'> ✔️ En cuanto a los incendios, se identifica que el incendio estructural y de covertura vegetal son los que tienen mayor proporción de personas damnificadas (afectadas, fallecidas y heridas).</h4>", unsafe_allow_html= True)
    
    with c31:
        st.image("https://cdn.pixabay.com/photo/2015/09/30/08/33/flood-965092_960_720.jpg",
             width=450)