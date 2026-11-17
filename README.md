# Projeto de Extensão — NexoContábil
## Tema
Painel demonstrativo para acompanhamento de lançamentos de boletos condominiais, com dados simulados.

## Objetivo
Demonstrar como o tratamento de dados e a visualização podem apoiar a leitura de indicadores de gestão condominial. Este protótipo não substitui sistemas contábeis nem utiliza dados reais de clientes.

## Requisitos atendidos no protótipo
- Dataset simulado com 250 linhas e mais de 4 colunas.
- Tratamento de dados com pandas.
- Dashboard Plotly com 4 visualizações: barras, linha, pizza e ranking.
- 4 KPIs: quantidade de registros, taxa paga, taxa atrasada e valor médio.
- Arquitetura documentada: ingestão → tratamento → armazenamento → visualização.
- Estrutura pronta para versionamento com Git.

## Como executar
1. Instale Python 3.10 ou superior.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute o tratamento: `python src/tratamento_dados.py`
5. Abra `dashboard/index.html` no navegador. Os gráficos Plotly carregam a biblioteca pela internet (CDN).

## Estrutura
- `dados/lancamentos_condominiais_simulados.csv`: base original simulada.
- `dados/lancamentos_tratados.csv`: base após tratamento.
- `src/tratamento_dados.py`: script de limpeza e padronização.
- `dashboard/index.html`: painel consolidado.
- `dashboard/grafico_*.html`: gráficos individuais.
- `evidencias/arquitetura_projeto.png`: diagrama da arquitetura.
- `Relatorio_Projeto_Extensao.docx`: relatório preenchido com proposta e metodologia.

## Git
Execute:
```bash
git init
git add .
git commit -m "Versão inicial do projeto de extensão NexoContábil"
```
Para publicar, crie um repositório no GitHub e siga as instruções de envio do próprio GitHub. O link só deve ser inserido no relatório depois que o repositório for criado.

## Limitações e ética
Os dados são inteiramente simulados. A taxa de pagamentos representa proporção de registros, não necessariamente taxa financeira de recebimento. Validar indicadores com a parte interessada antes de qualquer uso real.
