<!--
SPDX-FileCopyrightText: 2020, 2022 Impulso Gov <contato@impulsogov.org>

SPDX-License-Identifier: MIT
-->

# Análises de dados públicas em saúde

Repositório contendo as análises pontuais desenvolvidas pela Impulso Gov.


*******

## :mag_right: Índice

1. [Contexto](#contexto)
2. [Estrutura do repositório](#estrutura)
3. [Instruções para instalação](#instalacao)
4. [Executando as análises](#rodando)
5. [Contribua](#contribua)
6. [Licença](#licenca)

*******

<div id='contexto' />

## :rocket: Contexto

Um dos propósitos da Impulso Gov, enquanto organização, é transformar dados da saúde pública do Brasil em informações que ofereçam oferecer suporte de decisão aos gestores de saúde pública em todo o Brasil.

No decorrer desse trabalho, nossas analistas e engenheiras produzem diversas análises para explorar novas possibilidades de produtos e soluções, orientar nosso planejamento estratégico etc.

Este repositório reúne diversas dessas análises construídas em Python que não estão associadas a um produto da Impulso Gov em particular, e que utilizam **apenas dados públicos**.

*******

<div id='estrutura' />  

## :milky_way: Estrutura do repositório

Cada diretório dentro deste repositório contém um conjunto de análises agrupadas pelo ano de criação e o tema. Cada uma dessas pastas contém subdiretórios ou [*notebooks*](https://medium.com/data-hackers/jupyter-notebook-a-melhor-maneira-de-criar-uma-hist%C3%B3ria-com-dados-dbc2e8e3dd9a) contendo análises criadas com um propósito específico dentro daquele tema:

```plain
analises-publicas-saude
├─ 2020_AnalisesCoronacidades  \\ Relacionadas à resposta à Covid-19
│  ├─ 2020-06-02_ondacovid_twitter  \\ Evolução das mortes em municípios e estados brasileiros
│  ├─ 2020-06-09_rt_municipios_g1  \\ Ritmos de contágio por município
│  └─ 2021-03-11_vacinacao_municipios  \\ Estimativas de indivíduos em grupos prioritários
└─ 2022_AnalisesAPS  \\ Relacionadas à Atenção Primária à Saúde
   ├─ 20210615_Analise_Repasses_Financeiros_Componente_Desempenho.ipynb  \\ Repasses do programa Previne Brasil
   ├─ 202205_Atividade_Coletiva_Reunioes_Territorios.ipynb  \\ Reuniões e atividades de monitoramento territorial
   └─ 20220706_AT_Analise_Desempenho_APS_Perfil_Municipios.ipynb  \\ Relação entre desempenho e características do município
```

As pastas de primeiro nível estão identificadas com o padrão `<ano>_<TemaDasAnalises>`.

Além das análises que já se encontram no repositório, outras podem ser acrescentadas com o tempo.

*******

<div id='instalacao' /> 

## 🛠️ Instruções para instalação

Como foram criadas separadamente, cada análise pode contar com dependências e formas de instalação distintas. Verifique no arquivo `README.md` de cada subdiretório se há instruções específicas para a análise em questão.

Para executar as análises, você precisará ter instalada uma edição recente do [Python 3](https://www.python.org/downloads/) (recomenda-se do 3.7 em diante) e do [git](https://git-scm.com/downloads). 

Possivelmente você já tenha ambos instalados, mas, caso contrário, siga as instruções das páginas oficiais para fazer download e instalar ambos na sua máquina. Rode o comando a seguir em um terminal para checar se a instalação foi feita com sucesso: *(os números das versões podem variar)*

```sh
$ python3 --version
3.11.0
$ git --version
git version 2.38.1
```

Em seguida, baixe o repositório com as análises para um diretório na sua máquina e abra-o no terminal:

```sh
$ cd /diretorio/onde/deseja/baixar
$ git clone https://github.com/ImpulsoGov/analises-publicas-saude.git
$ cd analises-publicas-saude
```

*(Você também pode - e deve - acessar o subdiretorio de uma análise específica; nesse caso, substitua o último comando acima por `cd analises-publicas-saude/caminho/da/analise`)*

Como regra geral, recomenda-se instalar as dependências em um ambiente virtual do Python. Para isso, com o terminal no diretório da análise desejada, crie um novo ambiente e ative-o:

```sh
$ python3 -m venv .venv
$ source ./.venv/bin/activate
```

Se a análise tiver as dependências listadas em um arquivo `requirements.txt`, você pode instalá-las de uma vez só com o comando a partir do diretório da análise:

```sh
(.venv)$ python3 -m pip install -r requirements.txt
```

**Caso contrário**, recomenda-se instalar ao menos os pacotes `notebook` e `pandas`, que costumam ser utilizados em todas as análises: *(este passo não é necessário caso já tenha instalado as dependências a partir do arquivo `requirements.txt`)*

```sh
(.venv)$ python3 -m pip install notebook pandas
```

*******

<div id='rodando' /> 
 
## :gear: Executando as análises

Para abrir e executar as análises em um *notebook* interativo, abra um terminal no diretório com a análise e rode os seguintes comandos para ativar o ambiente virtual e inicializar o Jupyter:

```sh
$ source ./.venv/bin/activate
(.venv)$ jupyter notebook
... ...
[I 18:11:27.463 NotebookApp] Jupyter Notebook 6.5.2 is running at:
[I 18:11:27.463 NotebookApp] http://localhost:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
[I 18:11:27.463 NotebookApp]  or http://127.0.0.1:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
[I 18:11:27.463 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```

Siga um dos links impressos no terminal e aguarde até que uma nova aba seja aberta no seu navegador com o ambiente do Jupyter.

Navegue na estrutura de arquivos do diretório da análise por meio da interface do Jupyter e localize o notebook (arquivo com extensão `.ipynb`) que deseja explorar. Abra-o e utilize os comandos do Jupyter para executar a análise de maneira interativa - *veja mais informações na [documentação do usuário](https://jupyter-notebook.readthedocs.io/en/latest/user-documentation.html) (em inglês).

*******

<div id='contribua' />  

## :left_speech_bubble: Contribua

Sinta-se à vontade para contribuir em nosso projeto! [Abra uma *issue*](https://github.com/ImpulsoGov/analises-publicas-saude/issues/new/choose) ou [crie um *fork*](https://github.com/ImpulsoGov/analises-publicas-saude/fork) do projeto e envie sua contribuição como um [novo *pull request*](https://github.com/ImpulsoGov/analises-publicas-saude/compare).

*******

<div id='licenca' />  

## :registered: Licença

MIT (c) 2020, 2022 Impulso Gov \<contato@impulsogov.org\>
