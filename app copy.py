import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
import base64
from flask_cors import CORS

# Carregar as planilhas
file_path = 'C:\\Users\\william.sousa\\OneDrive - Bocayuva Advogados\\Documentos\\GitHub\\Dash_tv_boca\\mnt\\data\\Structured_DADOS.xlsx'
df_marketing = pd.read_excel(file_path, sheet_name='Sheet1')

file_path_agenda = 'C:\\Users\\william.sousa\\OneDrive - Bocayuva Advogados\\Documentos\\GitHub\\Dash_tv_boca\\mnt\\data\\Agenda.xlsx'
df_agenda = pd.read_excel(file_path_agenda)

file_path_glpi = 'C:\\Users\\william.sousa\\OneDrive - Bocayuva Advogados\\Documentos\\GitHub\\Dash_tv_boca\\mnt\\data\\glpi_updated.csv'
df_glpi = pd.read_csv(file_path_glpi)

file_path_comercial = 'C:\\Users\\william.sousa\\OneDrive - Bocayuva Advogados\\Documentos\\GitHub\\Dash_tv_boca\\mnt\\data\\Comercial.xlsx'
df_comercial = pd.read_excel(file_path_comercial)

file_path_rh = 'C:\\Users\\william.sousa\\OneDrive - Bocayuva Advogados\\Documentos\\GitHub\\Dash_tv_boca\\mnt\\data\\RH.xlsx'
df_rh = pd.read_excel(file_path_rh)

file_path_gestao_operacional = 'C:\\Users\\william.sousa\\OneDrive - Bocayuva Advogados\\Documentos\\GitHub\\Dash_tv_boca\\mnt\\data\\Gestao_Operacional.xlsx'
df_gestao_operacional = pd.read_excel(file_path_gestao_operacional)

# Dados do time de atendimento
total_atendimentos = df_agenda[df_agenda['Título'].str.contains("Atendimento", case=False, na=False)].shape[0]
atendimentos_whatsapp = df_agenda[df_agenda['Título'].str.contains("WhatsApp", case=False, na=False)].shape[0]
organizacao_pastas = df_agenda[df_agenda['Título'].str.contains("Organização de pasta", case=False, na=False)].shape[0]

meta_atendimentos = 50
meta_whatsapp = 400
meta_organizacao = 10

# Filtrar os dados para excluir Rafaella e Petrine dos dados jurídicos
df_agenda_juridico = df_agenda[~df_agenda['Responsável'].isin(['RAFAELA ALVES DE PAIVA', 'PETRINE CRISTINA PINTOR', 'Katiane Lustosa Rocha', 'Gabriel Cardoso'])]

# Dados do time jurídico
advogados = [adv for adv in df_agenda_juridico['Responsável'].unique() if adv != 'FINANCEIRO BOCAYUVA']
dados_advogados = {adv: {'Despachos': 0, 'NPS': 0} for adv in advogados}

for adv in advogados:
    dados_advogados[adv]['Despachos'] = df_agenda_juridico[(df_agenda_juridico['Responsável'] == adv) & 
                                                   (df_agenda_juridico['Título'].str.contains("Time Jurídico – Despacho", case=False, na=False))].shape[0]
    dados_advogados[adv]['NPS'] = df_agenda_juridico[(df_agenda_juridico['Responsável'] == adv) & 
                                             (df_agenda_juridico['Título'].str.contains("Time Jurídico – Cliente – Envio de NPS", case=False, na=False))].shape[0]

meta_despacho = 5
meta_nps = 5

# Dados do time de marketing
meta_instagram = 12
meta_facebook = 8
meta_linkedin = 2
meta_briefing = 1 / 3  # 1 por trimestre, equivalente a 1/3 por mês

# Dados do time comercial
meta_contatos = 150
meta_contratos = 10
meta_links_nps_diarios = 5
meta_nps_mensal = 94
meta_relatorios = 1

# Calcular totais do time comercial
total_contatos = df_comercial[df_comercial['Atividade'] == 'Contato'].shape[0]
total_contratos = df_comercial[df_comercial['Atividade'] == 'Contrato'].shape[0]
total_links_nps_diarios = df_comercial[df_comercial['Atividade'] == 'Link NPS Diário'].shape[0]
total_nps_mensal = df_comercial[df_comercial['Atividade'] == 'NPS Mensal'].shape[0]
total_relatorios = df_comercial[df_comercial['Atividade'] == 'Relatório'].shape[0]

# Dados do time de RH
meta_treinamento = 1
meta_avaliacao_cultura = 1 / 12  # 1 por ano, equivalente a 1/12 por mês
meta_integracao = 1 / 12  # 1 por ano, equivalente a 1/12 por mês

total_treinamentos = df_rh[df_rh['Atividade'].str.contains('Treinamento', case=False, na=False)].shape[0]
total_avaliacao_cultura = df_rh[df_rh['Atividade'].str.contains('Avaliação de Cultura', case=False, na=False)].shape[0]
total_integracao = df_rh[df_rh['Atividade'].str.contains('Ação de Integração', case=False, na=False)].shape[0]

# Dados do time de Gestão Operacional
meta_treinamento_gestao = 1
meta_one_one = 1 / 3  # 1 a cada 3 meses, equivalente a 1/3 por mês
meta_weekly = 4  # 1 por semana
meta_relatorio_desempenho = 1 / 3  # 1 a cada 3 meses, equivalente a 1/3 por mês

total_treinamentos_gestao = df_gestao_operacional[df_gestao_operacional['Atividade'].str.contains('Treinamento Gerenciamento Empresarial', case=False, na=False)].shape[0]
total_one_one = df_gestao_operacional[df_gestao_operacional['Atividade'].str.contains('One:One', case=False, na=False)].shape[0]
total_weekly = df_gestao_operacional[df_gestao_operacional['Atividade'].str.contains('Weekly', case=False, na=False)].shape[0]
total_relatorio_desempenho = df_gestao_operacional[df_gestao_operacional['Atividade'].str.contains('Relatório de Desempenho', case=False, na=False)].shape[0]

# Função para determinar a cor das barras
def determine_color(value, meta):
    return '#2ca02c' if value >= meta else '#ccb179'

# Função para adicionar check se meta foi atingida
def add_check(value, meta, name):
    check = "✔" if value >= meta else ""
    return f"{name}: {value} {check}"

# Codificar a imagem em base64 (se necessário)
image_filename = 'C:\\Users\\william.sousa\\OneDrive - Bocayuva Advogados\\Documentos\\GitHub\\Dash_tv_boca\\img\\logo.jpg'  # Substitua pelo caminho da sua imagem
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

# Criar uma lista de datas com espaçamento para marketing
x_values_marketing = []
for i in range(len(df_marketing)):
    x_values_marketing.extend([f"{df_marketing['Mês'][i]} - Instagram", f"{df_marketing['Mês'][i]} - Facebook", f"{df_marketing['Mês'][i]} - LinkedIn", f"{df_marketing['Mês'][i]} - Briefings", ''])
x_values_marketing = x_values_marketing[:-1]

# Calcular o percentual de chamados fechados dentro do SLA
sla = {
    'Alto': 2,
    'Médio': 5,
    'Baixo': 10
}

df_glpi['Dentro_SLA'] = df_glpi.apply(
    lambda row: (pd.to_datetime(row['Última atualização']) - pd.to_datetime(row['Data de abertura'])).days <= sla.get(row['Prioridade'], 10),
    axis=1
)
percentual_dentro_sla_glpi = df_glpi['Dentro_SLA'].mean() * 100

# Criar o aplicativo Dash
app = dash.Dash(__name__)
server = app.server
CORS(server)  # Habilitar CORS

# Layout do aplicativo
app.layout = html.Div(
    style={'backgroundColor': '#071b33', 'padding': '10px', 'font-family': 'Arial, sans-serif', 'color': '#ffffff'},
    children=[
        html.Div(
            children=[
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image),
                    style={'height': '80px', 'width': 'auto', 'display': 'block', 'margin': '0 auto'}
                ),
                html.H1(
                    children='Dashboard de Indicadores',
                    style={'textAlign': 'center', 'color': '#ccb179'}
                ),
                dcc.Tabs(id='tabs', value='tab-1', children=[
                    dcc.Tab(label='Atendimento', value='tab-1', style={'backgroundColor': '#ccb179', 'color': '#141e33'}),
                    dcc.Tab(label='Jurídico', value='tab-2', style={'backgroundColor': '#ccb179', 'color': '#141e33'}),
                    dcc.Tab(label='Marketing', value='tab-3', style={'backgroundColor': '#ccb179', 'color': '#141e33'}),
                    dcc.Tab(label='Tecnologia', value='tab-4', style={'backgroundColor': '#ccb179', 'color': '#141e33'}),
                    dcc.Tab(label='Comercial', value='tab-5', style={'backgroundColor': '#ccb179', 'color': '#141e33'}),
                    dcc.Tab(label='RH', value='tab-6', style={'backgroundColor': '#ccb179', 'color': '#141e33'}),
                    dcc.Tab(label='Gestão Operacional', value='tab-7', style={'backgroundColor': '#ccb179', 'color': '#141e33'}),
                ]),
                html.Div(id='tabs-content'),
                dcc.Interval(
                    id='interval-component',
                    interval=30*1000,  # 30 segundos
                    n_intervals=0
                )
            ],
            style={'margin-bottom': '20px'}
        )
    ]
)

@app.callback(
    dash.dependencies.Output('tabs', 'value'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def switch_tabs(n):
    if n % 7 == 0:
        return 'tab-1'
    elif n % 7 == 1:
        return 'tab-2'
    elif n % 7 == 2:
        return 'tab-3'
    elif n % 7 == 3:
        return 'tab-4'
    elif n % 7 == 4:
        return 'tab-5'
    elif n % 7 == 5:
        return 'tab-6'
    else:
        return 'tab-7'

@app.callback(
    dash.dependencies.Output('tabs-content', 'children'),
    [dash.dependencies.Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Metas: 50 atendimentos por mês, 400 atendimentos por WhatsApp por mês, organizar 10 pastas no mês.', style={'color': '#ccb179'}),
            dcc.Graph(
                id='atendimentos-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=['Atendimentos', 'WhatsApp', 'Organização de Pastas'],
                            y=[total_atendimentos, atendimentos_whatsapp, organizacao_pastas],
                            name='Indicadores',
                            marker=dict(color=[
                                determine_color(total_atendimentos, meta_atendimentos),
                                determine_color(atendimentos_whatsapp, meta_whatsapp),
                                determine_color(organizacao_pastas, meta_organizacao)
                            ]),
                            text=[
                                add_check(total_atendimentos, meta_atendimentos, 'Atendimentos'),
                                add_check(atendimentos_whatsapp, meta_whatsapp, 'WhatsApp'),
                                add_check(organizacao_pastas, meta_organizacao, 'Organização de Pastas')
                            ],
                            textposition='inside'
                        ),
                        go.Scatter(
                            x=['Atendimentos', 'WhatsApp', 'Organização de Pastas'],
                            y=[meta_atendimentos, meta_whatsapp, meta_organizacao],
                            name='Metas',
                            mode='lines+markers',
                            line=dict(color='#141e33', dash='dash'),
                            marker=dict(color='#ccb179')
                        )
                    ],
                    'layout': go.Layout(
                        title='Indicadores do Time de Atendimento',
                        titlefont=dict(size=18, color='#ccb179'),
                        xaxis=dict(title='Indicadores', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        yaxis=dict(title='Quantidade', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        showlegend=True,
                        legend=dict(font=dict(color='#ccb179')),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Metas: 5 despachos por mês para cada advogado, 5 envios de NPS por mês.', style={'color': '#ccb179'}),
            dcc.Graph(
                id='despachos-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=[adv for adv in advogados],
                            y=[dados_advogados[adv]['Despachos'] for adv in advogados],
                            name='Despachos',
                            marker=dict(color=[determine_color(dados_advogados[adv]['Despachos'], meta_despacho) for adv in advogados]),
                            text=[add_check(dados_advogados[adv]['Despachos'], meta_despacho, adv) for adv in advogados],
                            textposition='inside'
                        ),
                        go.Scatter(
                            x=[adv for adv in advogados],
                            y=[meta_despacho] * len(advogados),
                            name='Metas',
                            mode='lines',
                            line=dict(color='#141e33', dash='dash')
                        )
                    ],
                    'layout': go.Layout(
                        title='Despachos do Time Jurídico por Advogado',
                        titlefont=dict(size=18, color='#ccb179'),
                        xaxis=dict(title='Advogados', titlefont=dict(color='#ccb179'), tickangle=-30, tickfont=dict(color='#ccb179')),
                        yaxis=dict(title='Quantidade', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        showlegend=True,
                        legend=dict(font=dict(color='#ccb179')),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            ),
            dcc.Graph(
                id='nps-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=[adv for adv in advogados],
                            y=[dados_advogados[adv]['NPS'] for adv in advogados],
                            name='NPS',
                            marker=dict(color=[determine_color(dados_advogados[adv]['NPS'], meta_nps) for adv in advogados]),
                            text=[add_check(dados_advogados[adv]['NPS'], meta_nps, adv) for adv in advogados],
                            textposition='inside'
                        ),
                        go.Scatter(
                            x=[adv for adv in advogados],
                            y=[meta_nps] * len(advogados),
                            name='Metas NPS',
                            mode='lines',
                            line=dict(color='#141e33', dash='dash')
                        )
                    ],
                    'layout': go.Layout(
                        title='Envios de NPS do Time Jurídico por Advogado',
                        titlefont=dict(size=18, color='#ccb179'),
                        xaxis=dict(title='Advogados', titlefont=dict(color='#ccb179'), tickangle=-30, tickfont=dict(color='#ccb179')),
                        yaxis=dict(title='Quantidade', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        showlegend=True,
                        legend=dict(font=dict(color='#ccb179')),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Metas: 12 posts no Instagram por mês, 8 posts no Facebook por mês, 2 posts no LinkedIn por mês, 1 briefing por trimestre.', style={'color': '#ccb179'}),
            dcc.Graph(
                id='marketing-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=x_values_marketing[::4],
                            y=df_marketing['Instagram'],
                            name='Instagram',
                            marker=dict(color=[determine_color(x, meta_instagram) for x in df_marketing['Instagram']]),
                            text=[add_check(x, meta_instagram, 'Instagram') for x in df_marketing['Instagram']],
                            textposition='inside'
                        ),
                        go.Bar(
                            x=x_values_marketing[1::4],
                            y=df_marketing['Facebook'],
                            name='Facebook',
                            marker=dict(color=[determine_color(x, meta_facebook) for x in df_marketing['Facebook']]),
                            text=[add_check(x, meta_facebook, 'Facebook') for x in df_marketing['Facebook']],
                            textposition='inside'
                        ),
                        go.Bar(
                            x=x_values_marketing[2::4],
                            y=df_marketing['LinkedIn'],
                            name='LinkedIn',
                            marker=dict(color=[determine_color(x, meta_linkedin) for x in df_marketing['LinkedIn']]),
                            text=[add_check(x, meta_linkedin, 'LinkedIn') for x in df_marketing['LinkedIn']],
                            textposition='inside'
                        ),
                        go.Bar(
                            x=x_values_marketing[3::4],
                            y=df_marketing['Briefings'],
                            name='Briefings',
                            marker=dict(color=[determine_color(x, meta_briefing) for x in df_marketing['Briefings']]),
                            text=[add_check(x, meta_briefing, 'Briefings') for x in df_marketing['Briefings']],
                            textposition='inside'
                        ),
                    ],
                    'layout': go.Layout(
                        title='Indicadores de Posts e Briefings de Marketing',
                        titlefont=dict(size=18, color='#ccb179'),
                        xaxis=dict(title='Mês', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        yaxis=dict(title='Quantidade', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        showlegend=True,
                        legend=dict(font=dict(color='#ccb179')),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        bargap=0.2,  # Ajuste o valor para controlar o espaçamento entre as barras
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            )
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Meta: 80% dos chamados fechados dentro do SLA.', style={'color': '#ccb179'}),
            dcc.Graph(
                id='sla-pie-chart',
                figure={
                    'data': [
                        go.Pie(
                            labels=['Dentro do SLA', 'Fora do SLA'],
                            values=[percentual_dentro_sla_glpi, 100 - percentual_dentro_sla_glpi],
                            marker=dict(colors=['#2ca02c', '#d62728']),
                            textinfo='label+percent',
                            hole=.3
                        )
                    ],
                    'layout': go.Layout(
                        title='Percentual de Chamados Fechados Dentro do SLA - Tecnologia',
                        titlefont=dict(size=18, color='#ccb179'),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        font=dict(color='#ccb179'),
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            )
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Metas: 150 contatos por mês, 10 contratos por mês, enviar 5 links de NPS por dia, fechar 94 NPS no mês, entregar 1 relatório da área por mês.', style={'color': '#ccb179'}),
            dcc.Graph(
                id='comercial-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=['Contatos', 'Contratos', 'Links de NPS Diários', 'NPS Mensal', 'Relatórios'],
                            y=[total_contatos, total_contratos, total_links_nps_diarios, total_nps_mensal, total_relatorios],
                            name='Indicadores',
                            marker=dict(color=[
                                determine_color(total_contatos, meta_contatos),
                                determine_color(total_contratos, meta_contratos),
                                determine_color(total_links_nps_diarios, meta_links_nps_diarios),
                                determine_color(total_nps_mensal, meta_nps_mensal),
                                determine_color(total_relatorios, meta_relatorios)
                            ]),
                            text=[
                                add_check(total_contatos, meta_contatos, 'Contatos'),
                                add_check(total_contratos, meta_contratos, 'Contratos'),
                                add_check(total_links_nps_diarios, meta_links_nps_diarios, 'Links de NPS Diários'),
                                add_check(total_nps_mensal, meta_nps_mensal, 'NPS Mensal'),
                                add_check(total_relatorios, meta_relatorios, 'Relatórios')
                            ],
                            textposition='inside'
                        ),
                        go.Scatter(
                            x=['Contatos', 'Contratos', 'Links de NPS Diários', 'NPS Mensal', 'Relatórios'],
                            y=[meta_contatos, meta_contratos, meta_links_nps_diarios, meta_nps_mensal, meta_relatorios],
                            name='Metas',
                            mode='lines+markers',
                            line=dict(color='#141e33', dash='dash'),
                            marker=dict(color='#ccb179')
                        )
                    ],
                    'layout': go.Layout(
                        title='Indicadores do Time Comercial',
                        titlefont=dict(size=18, color='#ccb179'),
                        xaxis=dict(title='Indicadores', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        yaxis=dict(title='Quantidade', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        showlegend=True,
                        legend=dict(font=dict(color='#ccb179')),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            )
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.H3('Metas: 1 treinamento interno ou externo ao mês, 1 avaliação de cultura ao ano, 1 ação de integração ao ano.', style={'color': '#ccb179'}),
            dcc.Graph(
                id='rh-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=['Treinamentos', 'Avaliação de Cultura', 'Ação de Integração'],
                            y=[total_treinamentos, total_avaliacao_cultura, total_integracao],
                            name='Indicadores',
                            marker=dict(color=[
                                determine_color(total_treinamentos, meta_treinamento),
                                determine_color(total_avaliacao_cultura, meta_avaliacao_cultura),
                                determine_color(total_integracao, meta_integracao)
                            ]),
                            text=[
                                add_check(total_treinamentos, meta_treinamento, 'Treinamentos'),
                                add_check(total_avaliacao_cultura, meta_avaliacao_cultura, 'Avaliação de Cultura'),
                                add_check(total_integracao, meta_integracao, 'Ação de Integração')
                            ],
                            textposition='inside'
                        ),
                        go.Scatter(
                            x=['Treinamentos', 'Avaliação de Cultura', 'Ação de Integração'],
                            y=[meta_treinamento, meta_avaliacao_cultura, meta_integracao],
                            name='Metas',
                            mode='lines+markers',
                            line=dict(color='#141e33', dash='dash'),
                            marker=dict(color='#ccb179')
                        )
                    ],
                    'layout': go.Layout(
                        title='Indicadores do Time de RH',
                        titlefont=dict(size=18, color='#ccb179'),
                        xaxis=dict(title='Indicadores', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        yaxis=dict(title='Quantidade', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        showlegend=True,
                        legend=dict(font=dict(color='#ccb179')),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            )
        ])
    elif tab == 'tab-7':
        return html.Div([
            html.H3('Metas: 1 treinamento ao mês de gerenciamento empresarial, 1 one:one a cada 3 meses, 1 weekly por semana, 1 relatório de desempenho da equipe a cada 3 meses.', style={'color': '#ccb179'}),
            dcc.Graph(
                id='gestao-operacional-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=['Treinamento Gerenciamento Empresarial', 'One:One', 'Weekly', 'Relatório de Desempenho'],
                            y=[total_treinamentos_gestao, total_one_one, total_weekly, total_relatorio_desempenho],
                            name='Indicadores',
                            marker=dict(color=[
                                determine_color(total_treinamentos_gestao, meta_treinamento_gestao),
                                determine_color(total_one_one, meta_one_one),
                                determine_color(total_weekly, meta_weekly),
                                determine_color(total_relatorio_desempenho, meta_relatorio_desempenho)
                            ]),
                            text=[
                                add_check(total_treinamentos_gestao, meta_treinamento_gestao, 'Treinamento Gerenciamento Empresarial'),
                                add_check(total_one_one, meta_one_one, 'One:One'),
                                add_check(total_weekly, meta_weekly, 'Weekly'),
                                add_check(total_relatorio_desempenho, meta_relatorio_desempenho, 'Relatório de Desempenho')
                            ],
                            textposition='inside'
                        ),
                        go.Scatter(
                            x=['Treinamento Gerenciamento Empresarial', 'One:One', 'Weekly', 'Relatório de Desempenho'],
                            y=[meta_treinamento_gestao, meta_one_one, meta_weekly, meta_relatorio_desempenho],
                            name='Metas',
                            mode='lines+markers',
                            line=dict(color='#141e33', dash='dash'),
                            marker=dict(color='#ccb179')
                        )
                    ],
                    'layout': go.Layout(
                        title='Indicadores do Time de Gestão Operacional',
                        titlefont=dict(size=18, color='#ccb179'),
                        xaxis=dict(title='Indicadores', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        yaxis=dict(title='Quantidade', titlefont=dict(color='#ccb179'), tickfont=dict(color='#ccb179')),
                        showlegend=True,
                        legend=dict(font=dict(color='#ccb179')),
                        plot_bgcolor='#141e33',
                        paper_bgcolor='#141e33',
                        height=400  # Altura ajustada do gráfico
                    )
                },
                style={'height': '400px'}  # Altura do gráfico no layout
            )
        ])

if __name__ == '__main__':
    app.run_server(host='192.168.100.129', port=8050, debug=True)
