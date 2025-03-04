import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import numpy as np

# Configuração inicial do app
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])  # Adiciona CSS externo para melhor controle do grid
server = app.server

# Carregar dados
def load_data():
    df = pd.read_csv('df_cleaned.csv')
    df['newest_review_date'] = pd.to_datetime(df['newest_review_date'], format='%Y', errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Ensure price is numeric
    df['specialization'] = df['specialization'].astype(str).fillna('')
    df['city1'] = df['city1'].astype(str).fillna('')
    return df

df = load_data()

# Definir paleta de cores para consistência
COLOR_PALETTE = {
    'primary': '#3498db',  # Azul médio - cor principal
    'secondary': '#2ecc71',  # Verde - cor secundária
    'accent': '#e74c3c',  # Vermelho - destaque
    'neutral': '#95a5a6',  # Cinza - fundo neutro
    'light': '#ecf0f1',  # Cinza claro - fundo secundário
    'dark': '#2c3e50',  # Azul escuro - texto e detalhes
    'highlight': '#f39c12',  # Laranja - para destaque de informações importantes
}

# Definir estilos consistentes
styles = {
    'header': {
        'backgroundColor': COLOR_PALETTE['light'],
        'padding': '20px',
        'borderBottom': f'1px solid {COLOR_PALETTE["neutral"]}',
        'marginBottom': '20px',
    },
    'title': {
        'color': COLOR_PALETTE['dark'],
        'fontSize': '32px',
        'fontWeight': 'bold',
        'marginBottom': '5px',
    },
    'subtitle': {
        'color': COLOR_PALETTE['dark'],
        'fontSize': '18px',
        'marginBottom': '20px',
    },
    'container': {
        'padding': '15px',
        'borderRadius': '5px',
        'backgroundColor': 'white',
        'boxShadow': '0px 0px 5px rgba(0,0,0,0.1)',
        'marginBottom': '20px',
    },
    'card': {
        'padding': '15px',
        'borderRadius': '5px',
        'backgroundColor': 'white',
        'boxShadow': '0px 0px 5px rgba(0,0,0,0.1)',
        'height': '100%',
    },
    'section_title': {
        'color': COLOR_PALETTE['dark'],
        'fontSize': '20px',
        'fontWeight': 'bold',
        'marginBottom': '15px',
        'borderBottom': f'1px solid {COLOR_PALETTE["light"]}',
        'paddingBottom': '5px',
    }
}

# Layout do aplicativo
app.layout = html.Div([
    # Cabeçalho
    html.Div([
        html.H1("Dashboard de Profissionais Médicos", style=styles['title']),
        html.P("Análise interativa para auxiliar na escolha de profissionais médicos", style=styles['subtitle']),
    ], style=styles['header']),
    
    # Estatísticas Principais (KPIs) - Agora no topo
    html.Div([
        html.H3("Estatísticas Principais", style=styles['section_title']),
        
        html.Div([
            # KPI - Total de Médicos
            html.Div([
                html.Div([
                    html.H4("Total de Profissionais", style={'margin': '0', 'fontWeight': 'normal', 'fontSize': '16px'}),
                    html.H2(id="kpi-total-doctors", style={'margin': '5px 0', 'color': COLOR_PALETTE['primary'], 'fontSize': '36px'}),
                ], style=styles['card']),
            ], className="three columns"),
            
            # KPI - Preço Médio
            html.Div([
                html.Div([
                    html.H4("Preço Médio", style={'margin': '0', 'fontWeight': 'normal', 'fontSize': '16px'}),
                    html.H2(id="kpi-avg-price", style={'margin': '5px 0', 'color': COLOR_PALETTE['secondary'], 'fontSize': '36px'}),
                ], style=styles['card']),
            ], className="three columns"),
            
            # KPI - % com Telemedicina
            html.Div([
                html.Div([
                    html.H4("% com Telemedicina", style={'margin': '0', 'fontWeight': 'normal', 'fontSize': '16px'}),
                    html.H2(id="kpi-telemedicine-pct", style={'margin': '5px 0', 'color': COLOR_PALETTE['highlight'], 'fontSize': '36px'}),
                ], style=styles['card']),
            ], className="three columns"),
            
            # KPI - Avaliações Médias
            html.Div([
                html.Div([
                    html.H4("Média de Avaliações", style={'margin': '0', 'fontWeight': 'normal', 'fontSize': '16px'}),
                    html.H2(id="kpi-avg-reviews", style={'margin': '5px 0', 'color': COLOR_PALETTE['accent'], 'fontSize': '36px'}),
                ], style=styles['card']),
            ], className="three columns"),
        ], className="row"),
    ], style={**styles['container'], 'marginBottom': '20px'}),
    
    # Painel de controle (filtros) - Agora abaixo dos KPIs
    html.Div([
        html.H3("Filtros", style=styles['section_title']),
        
        html.Div([
            # Primeira linha de filtros
            html.Div([
                # Filtro de Especialização
                html.Div([
                    html.Label("Especialização"),
                    dcc.Dropdown(
                        id='specialization-filter',
                        options=[{'label': 'Todas', 'value': 'all'}] + 
                                [{'label': spec, 'value': spec} for spec in sorted(df['specialization'].unique())],
                        value='all',
                        clearable=False
                    ),
                ], className="three columns"),
                
                # Filtro de Cidade
                html.Div([
                    html.Label("Cidade"),
                    dcc.Dropdown(
                        id='city-filter',
                        options=[{'label': 'Todas', 'value': 'all'}] +
                                [{'label': city, 'value': city} for city in sorted(df['city1'].unique())],
                        value='all',
                        clearable=False
                    ),
                ], className="three columns"),
                
                # Filtro de Telemedicina
                html.Div([
                    html.Label("Telemedicina"),
                    dcc.Dropdown(
                        id='telemedicine-filter',
                        options=[
                            {'label': 'Todos', 'value': 'all'},
                            {'label': 'Disponível', 'value': 1},
                            {'label': 'Não disponível', 'value': 0}
                        ],
                        value='all',
                        clearable=False
                    ),
                ], className="three columns"),
                
                # Botão para Limpar Filtros
                html.Div([
                    html.Button('Limpar Filtros', id='clear-filters-button', n_clicks=0, 
                               style={'backgroundColor': COLOR_PALETTE['primary'], 'color': 'white',
                                     'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px',
                                     'cursor': 'pointer', 'marginTop': '25px', 'width': '100%'})
                ], className="three columns"),
            ], className="row"),
            
            # Segunda linha de filtros
            html.Div([
                # Filtro de Preço
                html.Div([
                    html.Label("Faixa de Preço"),
                    dcc.RangeSlider(
                        id='price-filter',
                        min=int(df['price'].min()),
                        max=int(df['price'].max()),
                        step=50,
                        marks={i: f'R${i}' for i in range(0, int(df['price'].max()) + 1, 100)},
                        value=[int(df['price'].min()), int(df['price'].max())]
                    ),
                ], className="twelve columns"),
            ], className="row", style={'marginTop': '20px'}),
            
            # Campo de busca
            html.Div([
                html.Label("Buscar por nome, cidade ou especialização:"),
                dcc.Input(
                    id='search-input',
                    type='text',
                    placeholder='Digite para buscar...',
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '4px', 'border': '1px solid #ddd'}
                ),
            ], className="twelve columns", style={'marginTop': '20px'}),
            
        ], style={'padding': '5px'}),
    ], style={**styles['container'], 'marginBottom': '20px'}),
    
    # Seção de Gráficos reorganizados em duas colunas (2x2)
    html.Div([
        # Coluna 1
        html.Div([
            # Gráfico de barras - distribuição por especialização
            html.Div([
                html.H3("Distribuição por Especialização", style=styles['section_title']),
                dcc.Graph(id='specialization-chart', config={'displayModeBar': False}, style={'height': '300px'}),
            ], style={**styles['container'], 'marginBottom': '20px', 'height': '350px'}),
            
            # Gráfico de barras - participação em telemedicina
            html.Div([
                html.H3("Profissionais com Telemedicina", style=styles['section_title']),
                dcc.Graph(id='telemedicine-chart', config={'displayModeBar': False}, style={'height': '300px'}),
            ], style={**styles['container'], 'height': '350px'}),
        ], className="six columns"),
        
        # Coluna 2
        html.Div([
            # Gráfico de distribuição de preços
            html.Div([
                html.H3("Distribuição de Preços por Consulta", style=styles['section_title']),
                dcc.Graph(id='price-distribution-chart', config={'displayModeBar': False}, style={'height': '300px'}),
            ], style={**styles['container'], 'marginBottom': '20px', 'height': '350px'}),
            
            # Gráfico de evolução das avaliações
            html.Div([
                html.H3("Evolução das Avaliações", style=styles['section_title']),
                dcc.Graph(id='reviews-evolution-chart', config={'displayModeBar': False}, style={'height': '300px'}),
            ], style={**styles['container'], 'height': '350px'}),
        ], className="six columns"),
    ], className="row"),
    
    # Tabela de Profissionais
    html.Div([
        html.H3("Detalhes dos Profissionais", style=styles['section_title']),
        
        # Tabela de dados
        dash_table.DataTable(
            id='doctors-table',
            columns=[
                {"name": "Nome", "id": "name"},
                {"name": "Cidade", "id": "city1"},
                {"name": "Especialização", "id": "specialization"},
                {"name": "Avaliações", "id": "reviews"},
                {"name": "Preço (R$)", "id": "price"},
                {"name": "Telemedicina", "id": "telemedicine_text"},
            ],
            style_header={
                'backgroundColor': COLOR_PALETTE['light'],
                'fontWeight': 'bold',
                'textAlign': 'left'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontFamily': 'Arial',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            page_size=10,
            filter_action="none",
            sort_action="native",
            sort_mode="multi",
            page_action="native"
        ),
    ], style=styles['container']),
    
    # Rodapé
    html.Div([
        html.P("Dashboard criado para auxiliar na escolha de profissionais médicos. Dados de 2022.", 
              style={'textAlign': 'center', 'color': COLOR_PALETTE['neutral']}),
    ], style={'marginTop': '30px', 'marginBottom': '20px'})
    
], style={'fontFamily': 'Arial, sans-serif', 'margin': '0', 'backgroundColor': '#f5f5f5', 'maxWidth': '1200px', 'margin': '0 auto', 'padding': '0 15px'})

# Callbacks

# Callback para atualizar todos os componentes baseados nos filtros
@app.callback(
    [
        Output('kpi-total-doctors', 'children'),
        Output('kpi-avg-price', 'children'),
        Output('kpi-telemedicine-pct', 'children'),
        Output('kpi-avg-reviews', 'children'),
        Output('specialization-chart', 'figure'),
        Output('telemedicine-chart', 'figure'),
        Output('price-distribution-chart', 'figure'),
        Output('reviews-evolution-chart', 'figure'),
        Output('doctors-table', 'data')
    ],
    [
        Input('specialization-filter', 'value'),
        Input('city-filter', 'value'),
        Input('telemedicine-filter', 'value'),
        Input('price-filter', 'value'),
        Input('search-input', 'value')
    ]
)
def update_dashboard(specialization, city, telemedicine, price_range, search_term):
    # Aplicar filtros
    filtered_df = df.copy()
    
    # Filtro de especialização
    if specialization != 'all':
        filtered_df = filtered_df[filtered_df['specialization'] == specialization]
    
    # Filtro de cidade
    if city != 'all':
        filtered_df = filtered_df[filtered_df['city1'] == city]
    
    # Filtro de telemedicina
    if telemedicine != 'all':
        filtered_df = filtered_df[filtered_df['telemedicine'] == telemedicine]
    
    # Filtro de preço
    filtered_df = filtered_df[(filtered_df['price'] >= price_range[0]) & 
                              (filtered_df['price'] <= price_range[1])]
    
    # Filtro de busca
    if search_term:
        search_term = search_term.lower()
        search_filter = (
            filtered_df['name'].str.lower().str.contains(search_term) |
            filtered_df['city1'].str.lower().str.contains(search_term) |
            filtered_df['specialization'].str.lower().str.contains(search_term)
        )
        filtered_df = filtered_df[search_filter]
    
    # Se não houver dados após filtros
    if filtered_df.empty:
        # Criar gráficos vazios
        empty_bar = px.bar(
            x=['Sem dados'],
            y=[0],
            labels={'x': '', 'y': 'Contagem'},
            title="Sem dados disponíveis para os filtros selecionados"
        )
        
        return (
            "0",  # KPI - Total
            "R$ 0",  # KPI - Preço Médio
            "0%",  # KPI - % Telemedicina
            "0",  # KPI - Média Avaliações
            empty_bar,  # Gráfico de especialização
            empty_bar,  # Gráfico de telemedicina
            empty_bar,  # Gráfico de preços
            empty_bar,  # Gráfico de evolução de avaliações
            []  # Tabela vazia
        )
    
    # Calcular KPIs
    total_doctors = len(filtered_df)
    avg_price = f"R$ {filtered_df['price'].mean():.2f}"
    telemedicine_pct = f"{(filtered_df['telemedicine'].sum() / total_doctors * 100):.1f}%"
    avg_reviews = f"{filtered_df['reviews'].mean():.1f}"
    
    # Gráfico de Distribuição por Especialização
    spec_counts = filtered_df['specialization'].value_counts().reset_index()
    spec_counts.columns = ['specialization', 'count']
    spec_counts = spec_counts.sort_values('count', ascending=False).head(10)  # Reduzido para 10 para caber melhor
    
    specialization_fig = px.bar(
        spec_counts,
        x='count',
        y='specialization',
        orientation='h',
        labels={'count': 'Número de Profissionais', 'specialization': 'Especialização'},
        color='count',
        color_continuous_scale=px.colors.sequential.Blues,
        text='count'
    )
    
    specialization_fig.update_layout(
        plot_bgcolor='white',
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    
    specialization_fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Profissionais: %{x}'
    )
    
    # Gráfico de Participação em Telemedicina
    telemedicine_counts = filtered_df['telemedicine'].map({1: 'Disponível', 0: 'Não disponível'}).value_counts().reset_index()
    telemedicine_counts.columns = ['status', 'count']
    
    telemedicine_fig = px.pie(
        telemedicine_counts,
        values='count',
        names='status',
        color='status',
        color_discrete_map={
            'Disponível': COLOR_PALETTE['secondary'],
            'Não disponível': COLOR_PALETTE['neutral']
        },
        hole=0.4
    )
    
    telemedicine_fig.update_layout(
        legend_title="Telemedicina",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    
    telemedicine_fig.update_traces(
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Profissionais: %{value} (%{percent})'
    )
    
    # Gráfico de Distribuição de Preços
    price_fig = px.histogram(
        filtered_df,
        x='price',
        nbins=20,
        labels={'price': 'Preço da Consulta (R$)', 'count': 'Número de Profissionais'},
        color_discrete_sequence=[COLOR_PALETTE['primary']]
    )
    
    price_fig.update_layout(
        plot_bgcolor='white',
        bargap=0.1,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    
    price_fig.update_traces(
        hovertemplate='Preço: R$%{x}<br>Profissionais: %{y}'
    )
    
    # Adicionar boxplot sobreposto ao histograma
    price_box = go.Box(
        x=filtered_df['price'],
        name='Distribuição',
        marker_color=COLOR_PALETTE['accent'],
        boxpoints='outliers',
        line=dict(width=2),
        fillcolor='rgba(0,0,0,0)',
        y0=0
    )
    
    price_fig.add_trace(price_box)
    
    # Gráfico de Evolução das Avaliações
    # Agrupando por data e especialização para o gráfico de evolução
    reviews_evolution = filtered_df.groupby(['newest_review_date']).agg(
        total_reviews=('reviews', 'sum'),
        avg_reviews=('reviews', 'mean'),
        count=('reviews', 'count')
    ).reset_index()
    
    reviews_evolution = reviews_evolution.sort_values('newest_review_date')
    
    reviews_fig = go.Figure()
    
    reviews_fig.add_trace(go.Scatter(
        x=reviews_evolution['newest_review_date'],
        y=reviews_evolution['avg_reviews'],
        mode='lines+markers',
        name='Média de Avaliações',
        line=dict(color=COLOR_PALETTE['highlight'], width=3),
        hovertemplate='Data: %{x|%Y}<br>Média de Avaliações: %{y:.1f}'
    ))
    
    reviews_fig.update_layout(
        xaxis_title='Data da Avaliação mais Recente',
        yaxis_title='Média de Avaliações',
        plot_bgcolor='white',
        hovermode='x unified',
        margin=dict(l=10, r=10, t=10, b=10),
    )
    
    # Preparar dados para a tabela
    table_df = filtered_df[['name', 'city1', 'specialization', 'reviews', 'price', 'telemedicine']].copy()
    table_df['telemedicine_text'] = table_df['telemedicine'].map({1: 'Sim', 0: 'Não'})
    table_data = table_df.to_dict('records')
    
    return (
        f"{total_doctors:,}".replace(',', '.'),  # KPI - Total
        avg_price,  # KPI - Preço Médio
        telemedicine_pct,  # KPI - % Telemedicina
        avg_reviews,  # KPI - Média Avaliações
        specialization_fig,  # Gráfico de especialização
        telemedicine_fig,  # Gráfico de telemedicina
        price_fig,  # Gráfico de preços
        reviews_fig,  # Gráfico de evolução de avaliações
        table_data  # Tabela de médicos
    )

# Callback para limpar todos os filtros
@app.callback(
    [
        Output('specialization-filter', 'value'),
        Output('city-filter', 'value'),
        Output('telemedicine-filter', 'value'),
        Output('price-filter', 'value'),
        Output('search-input', 'value')
    ],
    Input('clear-filters-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    if n_clicks > 0:
        return (
            'all',  # Especialização
            'all',  # Cidade
            'all',  # Telemedicina
            [int(df['price'].min()), int(df['price'].max())],  # Preço
            ''  # Busca
        )
    raise PreventUpdate

# Execução do app
if __name__ == '__main__':
    app.run_server(debug=True)