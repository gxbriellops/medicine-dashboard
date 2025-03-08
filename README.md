# Dashboard de Profissionais Médicos

Um painel interativo para auxiliar na escolha de profissionais médicos, construído com Dash e Plotly.

![Dashboard Preview](https://github.com/gxbriellops/medicine-dashboard/blob/main/Grava%C3%A7%C3%A3o-de-Tela-2025-03-08-154523.gif)

## Descrição

Esta aplicação web fornece uma interface interativa para explorar e analisar dados de profissionais médicos. Os usuários podem filtrar por especialização, cidade, disponibilidade de telemedicina e faixa de preço para encontrar o profissional ideal para suas necessidades.

## Funcionalidades

- **Estatísticas Principais (KPIs)**: Total de profissionais, preço médio, percentual com telemedicina e média de avaliações.
- **Filtros Interativos**: Filtros por especialização, cidade, disponibilidade de telemedicina e faixa de preço.
- **Visualizações Gráficas**:
  - Distribuição de profissionais por especialização
  - Proporção de profissionais que oferecem telemedicina
  - Distribuição de preços por consulta
  - Evolução das avaliações ao longo do tempo
- **Tabela Detalhada**: Visualização tabulada dos profissionais com ordenação e paginação.
- **Busca por Texto**: Permite buscar profissionais por nome, cidade ou especialização.

## Tecnologias Utilizadas

- **Dash**: Framework para criação de aplicações web analíticas em Python
- **Plotly**: Biblioteca para criação de gráficos interativos
- **Pandas**: Manipulação e análise de dados
- **Gunicorn**: Servidor WSGI HTTP para implementação em produção

## Requisitos

```
dash==2.14.2
dash-core-components==2.0.0
dash-html-components==2.0.0
dash-table==5.0.0
pandas==2.1.1
plotly==5.18.0
numpy==1.26.2
gunicorn==21.2.0
```

## Instalação e Execução

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/dashboard-medicos.git
   cd dashboard-medicos
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação localmente:
   ```bash
   python app.py
   ```

5. Acesse a aplicação em seu navegador:
   ```
   http://127.0.0.1:8050/
   ```

## Estrutura do Projeto

```
dashboard-medicos/
│
├── app.py               # Código principal da aplicação Dash
├── df_cleaned.csv       # Conjunto de dados dos profissionais (não incluído no repositório)
├── Procfile             # Configuração para deploy (Heroku, etc.)
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo
```

## Deploy

O projeto está configurado para deploy em plataformas como Heroku. O arquivo `Procfile` já está configurado para usar o Gunicorn como servidor:

```
web: gunicorn app:server
```

## Fonte de Dados

Os dados utilizados neste dashboard são de profissionais médicos com informações como nome, especialização, cidade, avaliações, preço e disponibilidade de telemedicina. O conjunto de dados está atualizado até 2022.

## Desenvolvimento Futuro

Possíveis melhorias para o projeto:

- Implementação de filtros avançados
- Adicionar mapa de distribuição geográfica dos profissionais
- Integração com sistemas de agendamento online
- Comparação direta entre profissionais selecionados
- Versão mobile otimizada

## Licença

[MIT](https://choosealicense.com/licenses/mit/)

## Contato

Para dúvidas ou sugestões, entre em contato através de [seu-email@exemplo.com](mailto:seu-email@exemplo.com)
