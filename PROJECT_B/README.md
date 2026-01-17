# PROJECT B - We-Commerce Analytics
## Análise e Mineração de Dados Web

**Instituição:** ISEL (Instituto Superior de Engenharia de Lisboa)  
**Disciplina:** AMD - Análise e Mineração de Dados  
**Ano Letivo:** 2025/2026  
**Grupo:** G03 - SoftKnow Consulting

---

## 📋 Visão Geral

Este projeto realiza análise completa de dados de web analytics da plataforma We-Commerce, explorando padrões de navegação e comportamento de visitantes através de técnicas de mineração de dados.

**Dataset:** 415.863 eventos de Janeiro 2012  
**Técnicas:** Association Rules Mining, Data Filtering, Basket Analysis  
**Ferramentas:** Python, Orange Data Mining, PostgreSQL

---

## 🔧 Pré-requisitos

### Software Necessário

| Software | Versão Mínima | Instalação |
|----------|---------------|------------|
| PostgreSQL | 12+ | `sudo apt-get install postgresql` |
| Python | 3.8+ | `sudo apt-get install python3 python3-pip` |
| Orange3 | 3.30+ | `pip3 install Orange3` |
| Bibliotecas Python | - | `pip3 install numpy pandas matplotlib` |

### Verificação Rápida

```bash
# Verificar instalações
psql --version
python3 --version
python3 -c "import Orange; print('Orange OK')"
```

---

## 🚀 Guia de Execução

### Exercícios 1 e 2: Análise Documental

**Tipo:** Análise teórica (não requer execução)

Estes exercícios analisam o processo de recolha de dados e estatísticas exploratórias. As respostas estão documentadas no relatório LaTeX.

**Localização:** `report_latex/report_project_b.tex` (Secções 1 e 2)

---

### Exercício 3: Distribuição Agregada

**Tipo:** SQL Views (não requer execução de script, sendo opcional)

Este exercício cria vistas SQL para análise agregada dos dados. As vistas já estão definidas na base de dados após o setup inicial.

**Visualização:** Abrir PostgreSQL e consultar as vistas criadas ou usar python script já fornecido, como está abaixo.

```bash
cd PROJECT_B/scripts
python3 exercise3_generate_aggregated_view.py
```

---

### Exercício 4: Filtragem de Dados

**Script:** `scripts/exercise4_filter_data.py`

Filtra visitantes com 5-30 sessões para análise focada.

```bash
cd PROJECT_B/scripts
python3 exercise4_filter_data.py
```

**Saída esperada:**
- `transactions_filtered.txt` - Lista de visitantes filtrados
- Tempo de execução: ~3 segundos

---

### Exercício 5: Exportação de Transações

**Script:** `scripts/exercise5_export_transactions.py`

Exporta transações filtradas para formato CSV.

```bash
cd PROJECT_B/scripts
python3 exercise5_export_transactions.py
```

**Saída esperada:**
- `transactions_export.csv` - Dados exportados
- Tempo de execução: ~2 segundos

---

### Exercício 6: Transformação para Basket

**Script:** `scripts/exercise6_basket_transform.py`

Converte dados para formato basket do Orange.

```bash
cd PROJECT_B/scripts
python3 exercise6_basket_transform.py
```

**Saída esperada:**
- `transactions_basket.basket` - Formato Orange
- `transactions_basket.tab` - Formato tabular
- Tempo de execução: ~2 segundos

---

### Exercício 7: Mineração de Regras de Associação

**Script:** `scripts/exercise7_association_rules.py`

Descobre regras de associação usando FP-Growth algorithm.

#### Execução Básica (Support por Contagem)

```bash
cd PROJECT_B/scripts
python3 exercise7_association_rules.py
```

#### Execução com Support Percentual

```bash
python3 exercise7_association_rules.py --percentage
# ou
python3 exercise7_association_rules.py -p
```

#### Personalizar Número Máximo de Regras

```bash
python3 exercise7_association_rules.py 15 --percentage
```

**Saídas geradas:**

Com support por contagem:
- `figures/figure_1_rules_count.png` - Q1: Produtos para manter juntos
- `figures/figure_2_rules_count.png` - Q2: Produtos raros mas correlacionados
- `figures/figure_3_rules_count.png` - Q3: Produtos mais visitados
- `results/results_config_*_count.txt` - Regras em texto

Com support percentual:
- `figures/figure_1_rules_percent.png`
- `figures/figure_2_rules_percent.png`
- `figures/figure_3_rules_percent.png`
- `results/results_config_*_percent.txt`

**Tempo de execução:** ~2-3 segundos

---

### Exercício 8: Relatório Gráfico com Orange

**Tipo:** Workflow visual no Orange Data Mining

#### Abrir o Workflow

```bash
cd PROJECT_B
orange-canvas association_rules_workflow.ows
```

#### Workflow Configurado

```
File → Frequent Itemsets → Association Rules → Visualizações
```

**Parâmetros configurados:**
- Support: 0.5% (≈15 transações)
- Confidence: 20%

#### Visualizações Geradas

O workflow permite exportar:
- `frequent_items.png` - Itemsets frequentes
- `association_rules.png` - Tabela de regras
- `scatter_plot.png` - Support vs Confidence

**Como exportar:**
1. Abrir cada widget de visualização
2. Clicar em "Save Image" ou usar screenshot
3. Salvar na pasta `report_latex/figures/`

---

### Exercício 9: Pipeline Automatizado

**Resumo:** Todos os Exercícios 4, 5, 6 e 7 foram implementados em scripts Python executáveis de forma independente ou através de pipeline automatizado.

**Execução manual dos scripts:** Ver instruções nos exercícios 4-7 acima.

---

## 📁 Estrutura de Ficheiros

```
PROJECT_B/
├── README.md                          # Este ficheiro
├── z_dataset_JAN_updated.csv         # Dataset principal
├── transactions_basket.basket         # Dados em formato basket
├── association_rules_workflow.ows     # Workflow Orange (Ex. 8)
│
├── scripts/                           # Scripts executáveis
│   ├── exercise4_filter_data.py
│   ├── exercise5_export_transactions.py
│   ├── exercise6_basket_transform.py
│   ├── exercise7_association_rules.py
│   └── exercise9_automate_pipeline.py
│
├── figures/                           # Gráficos gerados (Ex. 7)
│   ├── figure_1_rules_count.png
│   ├── figure_2_rules_count.png
│   ├── figure_3_rules_count.png
│   ├── figure_1_rules_percent.png
│   ├── figure_2_rules_percent.png
│   └── figure_3_rules_percent.png
│
├── results/                           # Resultados textuais (Ex. 7)
│   ├── results_config_1_count.txt
│   ├── results_config_2_count.txt
│   ├── results_config_3_count.txt
│   ├── results_config_1_percent.txt
│   ├── results_config_2_percent.txt
│   └── results_config_3_percent.txt
│
└── report_latex/                      # Relatório final
    ├── report_project_b.tex
    ├── report_project_b.pdf
    └── figures/                       # Figuras para relatório
        ├── figure_1_rules_count.png
        ├── figure_2_rules_count.png
        ├── figure_3_rules_count.png
        ├── frequent_items.png
        ├── association_rules.png
        └── scatter_plot.png
```

---

## 📊 Resultados Esperados

### Exercício 4 - Filtragem
- **Visitantes filtrados:** ~3.048
- **Critério:** 5-30 sessões por visitante

### Exercício 5 - Exportação
- **Registos exportados:** ~10.000-15.000 transações
- **Formato:** CSV com colunas: cookie_id, session_id, product_guid, timestamp

### Exercício 6 - Basket Transform
- **Transações:** 3.048
- **Produtos únicos:** ~1.942
- **Formato:** Orange .basket + .tab

### Exercício 7 - Association Rules

#### Configuração 1: Produtos para manter juntos
- **Regras:** 7-10 regras
- **Confiança:** 40-100%
- **Suporte:** 0.5-1.0%

#### Configuração 2: Produtos raros mas correlacionados
- **Regras:** 10-15 regras
- **Confiança:** 70-100%
- **Suporte:** 0.2-0.4%

#### Configuração 3: Produtos mais visitados
- **Regras:** 7-10 regras
- **Confiança:** 0.05-5%
- **Suporte:** 0.7-1.3%

### Exercício 8 - Orange Workflow
- **Visualizações:** 3 imagens PNG
- **Itemsets frequentes:** ~50-100
- **Regras geradas:** ~20-30

---

## 🔍 Troubleshooting

### Erro: "Cannot connect to PostgreSQL"

```bash
# Verificar se PostgreSQL está a correr
sudo systemctl status postgresql
sudo systemctl start postgresql

# Verificar credenciais
psql -U seu_usuario -d db_project_b -c "SELECT 1;"
```

### Erro: "Module Orange not found"

```bash
# Reinstalar Orange3
pip3 install --upgrade Orange3

# Verificar instalação
python3 -c "import Orange; print(Orange.__version__)"
```

### Erro: "File not found: transactions_basket.basket"

```bash
# Executar Exercício 6 primeiro
cd PROJECT_B/scripts
python3 exercise6_basket_transform.py

# Verificar criação
ls -lh ../transactions_basket.basket
```

### Figuras não são geradas no Exercício 7

```bash
# Verificar matplotlib
pip3 install --upgrade matplotlib

# Verificar permissões de escrita
mkdir -p figures
chmod 755 figures
```

---

## 📚 Documentação Adicional

### Relatório Completo

O relatório completo em LaTeX está disponível em:
- **Fonte:** `report_latex/report_project_b.tex`
- **PDF compilado:** `report_latex/report_project_b.pdf`

### Compilar Relatório

```bash
cd report_latex
pdflatex report_project_b.tex
pdflatex report_project_b.tex  # Segunda vez para referências
```

### Scripts Auxiliares

Localização: `scripts_linux/`

Scripts shell para operações específicas do sistema (se necessários).

---

## 👥 Autores

**Grupo G03 - SoftKnow Consulting**

- Florin Sofinet (A46608)
- Diogo Guerra (A49149)
- Nuno Silva (A53976)

---

## 📄 Licença

Este projeto é desenvolvido para fins académicos no âmbito da disciplina AMD do ISEL.

---

**Última atualização:** Janeiro 2026
