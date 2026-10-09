import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Resultado de Obras | Controladoria', page_icon='🏗️', layout='wide')
st.title('🏗️ Painel Gerencial | Resultado de Obras')
st.caption('Simulação com dados fictícios de oito contratos de pavimentação urbana. Valores em R$.')

@st.cache_data
def gerar_dados():
    dados = [
        ('OBR-001','Av. das Nações',12000,450000,390000,0.90,0.88),
        ('OBR-002','Rua das Flores',8500,320000,295000,1.00,1.00),
        ('OBR-003','Av. Industrial',16000,720000,750000,1.00,1.00),
        ('OBR-004','Rua Primavera',10500,410000,335000,0.85,0.82),
        ('OBR-005','Av. Central',19000,890000,650000,0.75,0.72),
        ('OBR-006','Rua do Comércio',7200,280000,265000,0.95,0.92),
        ('OBR-007','Av. Brasil',14500,640000,490000,0.80,0.78),
        ('OBR-008','Rua dos Ipês',9300,370000,305000,0.90,0.87),
    ]
    df = pd.DataFrame(dados,columns=['ID','Obra','Área (m²)','Receita contratada','Custo orçado','Avanço físico','Avanço financeiro'])
    # Simulação: custo incorrido varia em relação ao orçamento proporcional à execução física.
    fatores = [1.05,0.98,1.12,0.96,1.08,1.02,0.93,1.10]
    
    df['Custo realizado'] = (
        df['Custo orçado'] * df['Avanço físico'] * pd.Series(fatores)
    ).round(2)

    df['Receita reconhecida (simulada)'] = (
        df['Receita contratada'] * df['Avanço financeiro']
    ).round(2)

    df['Custo previsto até a etapa'] = (
        df['Custo orçado'] * df['Avanço físico']
    )

    df['Desvio de custo (R$)'] = (
        df['Custo realizado'] - df['Custo previsto até a etapa']
    )

    df['Desvio de custo (%)'] = (
        df['Desvio de custo (R$)'] / df['Custo previsto até a etapa']
    )

    df['Desvio de custo (%)'] = df['Desvio de custo (R$)']/df['Custo previsto até a etapa']
    df['Resultado'] = df['Receita reconhecida (simulada)']-df['Custo realizado']
    df['Margem (%)'] = df['Resultado']/df['Receita reconhecida (simulada)']
    df['Custo por m² executado'] = df['Custo realizado']/(df['Área (m²)']*df['Avanço físico'])
    df['Status'] = df.apply(lambda x: 'Prejuízo' if x['Resultado']<0 else ('Acima do orçamento' if x['Desvio de custo (%)']>0.05 else 'Dentro do limite'),axis=1)
    return df

def brl(v): return f'R$ {v:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
def pct(v): return f'{v:.1%}'.replace('.',',')

df = gerar_dados()
st.sidebar.header('Filtros')
selecionadas = st.sidebar.multiselect('Selecione as obras',df['Obra'].tolist(),default=df['Obra'].tolist())
base = df[df['Obra'].isin(selecionadas)].copy()
if base.empty:
    st.warning('Selecione pelo menos uma obra para visualizar os resultados.')
    st.stop()

receita = base['Receita reconhecida (simulada)'].sum()
custo = base['Custo realizado'].sum()
resultado = receita-custo
cols = st.columns(4)
cols[0].metric('Receita reconhecida (simulada)',brl(receita))
cols[1].metric('Custo realizado',brl(custo))
cols[2].metric('Resultado',brl(resultado))
cols[3].metric('Margem consolidada',pct(resultado/receita) if receita else 'N/D')

aba1,aba2,aba3 = st.tabs(['Visão geral','Análise de custos','Base de dados'])
with aba1:
    st.subheader('Resultado por obra')
    fig=px.bar(base,x='Obra',y='Resultado',color='Status',color_discrete_map={'Prejuízo':'#d65b58','Acima do orçamento':'#e7a23b','Dentro do limite':'#23877e'},text_auto='.2s')
    fig.update_layout(xaxis_title='',yaxis_title='Resultado (R$)')
    st.plotly_chart(fig,use_container_width=True)
    st.subheader('Receita reconhecida x custo realizado')
    comparacao=base.melt(id_vars='Obra',value_vars=['Receita reconhecida (simulada)','Custo realizado'],var_name='Indicador',value_name='Valor (R$)')
    st.plotly_chart(px.bar(comparacao,x='Obra',y='Valor (R$)',color='Indicador',barmode='group'),use_container_width=True)
with aba2:
    st.subheader('Desvio de custo proporcional à execução')
    st.caption('Desvio positivo indica gasto superior ao orçamento proporcional ao avanço físico. Limite de alerta: 5%.')
    fig=px.bar(base,x='Obra',y='Desvio de custo (%)',color='Status',color_discrete_map={'Prejuízo':'#d65b58','Acima do orçamento':'#e7a23b','Dentro do limite':'#23877e'})
    fig.add_hline(y=0.05,line_dash='dash',annotation_text='Limite 5%')
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(base[['Obra','Avanço físico','Custo orçado','Custo previsto até a etapa','Custo realizado','Desvio de custo (R$)','Desvio de custo (%)','Custo por m² executado','Status']],hide_index=True,use_container_width=True)
with aba3:
    st.dataframe(base,hide_index=True,use_container_width=True)
    st.download_button('📥 Baixar dados em CSV',data=base.to_csv(index=False,sep=';',decimal=',').encode('utf-8-sig'),file_name='resultado_obras_ficticias.csv',mime='text/csv')

st.info('Nota metodológica: receita reconhecida, avanço financeiro e custos são simulações didáticas, não representam escrituração contábil nem aplicação automática do CPC 47. Resultado = receita reconhecida simulada − custo realizado, antes de despesas indiretas não alocadas, tributos e resultado financeiro.')
