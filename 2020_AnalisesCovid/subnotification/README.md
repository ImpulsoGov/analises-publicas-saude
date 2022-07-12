# Estimando subnotificação de casos

Metodologia e implementação do Tiago e Kevin (ICMC-USP), com base nos parâmetros de [Verity, Robert et al. (2020)](https://www.thelancet.com/pdfs/journals/laninf/PIIS1473-3099(20)30243-7.pdf). 

### Como funciona?
Simulação de X experimentos com uma binomial negativa para estimar quantos casos resultaram no número observado de óbitos (n) dado uma probabilidade (p) do caso chegar a óbito. Essa probabilidade é calculada a partir ponderação da taxa de letalidade e população por faixa etária do município.

### O que queremos resolver?

- Melhorar subnotificação a nível local: hoje usamos somente uma taxa de mortalidade geral no ajuste dos casos
- Resolver problema de sobrehospitalização inicial do modelo - em parte pode ser a subnotificação, mas também os parâmetros de % de casos severos/graves inicial utilizados

### O que fazer?

- Cálculo da subnotificação por regionais (450 regionais de saúde): resultados com diferentes janelas e limitações
- Cálculo da subnotificação para municípios (quantos?): critérios de viabilidade, resultados e limitações
- Integração do novo cálculo no FarolCovid

### Estrutura do repo

    ├── README.md                         <- este arquivo
    ├── data
    │   ├── output                        <- Dados de resultados do modelo
    │   └── treated                       <- Dados já tratados para entrada do modelo
    ├── calculate_subnotification.ipynb   <- Notebook para implementação
    ├── icmc                              <- Código de referência do Tiago e Kevin
    ├── scripts                           <- Códigos de tratamento e integração do modelo

### Reuniões

Anotações: https://docs.google.com/document/d/1OeSqTOds4e7it5tLBCF8k4ht54YIedYrojex64h4N9c/edit#
