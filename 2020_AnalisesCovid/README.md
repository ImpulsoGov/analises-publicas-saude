# Análises internas e testes

Ambiente para rascunhos, estudos/bench de novos cálculos e análises internas :)

## Ambiente virtual de análise - por quê usar?

Para separar os pacotes do seu computador dos que vão ser utilizados aqui - e evitar problemas de compatibilidade de versão -, use o ambiente de análise! 

Os pacotes padrão do ambiente de análise (para Python) estão em `requirements.txt` -  caso precise de outros, adicione nesse arquivo.

### Criando seu ambiente

```bash
# Instala pacote (via pip/Python)
$ pip3 install virtualenv
# Cria e ativa o ambiente
$ virtualenv .internal_analysis && . .internal_analysis/bin/activate
# Instala pacotes
(.internal_analysis)$ pip3 install -r requirements.txt
# Instala R (Ubuntu)
(.internal_analysis)$ sudo apt update && sudo apt install r-base;
```

## Jupyter

### Rodando Python no Jupyter

```bash
# Configura o kernel do Python no Jupyter
(.internal_analysis)$ python3 -m ipykernel install --user --name=internal_analysis
# Abre o Jupyter no navegador
(.internal_analysis)$ jupyter notebook
```

### Rodando R no Jupyter

```bash
# Instala kernel do R
(.internal_analysis)$ R
> install.packages('IRkernel')
> IRkernel::installspec()
> q()
# Abre o Jupyter no navegador
(.internal_analysis)$ jupyter notebook
```
Uma vez no Jupyter no seu navegador, escolha o kernel "R" quando criar um novo notebook :)

*Mais infos do IRKernel: https://irkernel.github.io/installation/*

### Usando [nbextensions ♥️](https://github.com/ipython-contrib/jupyter_contrib_nbextensions) para facilitar a vida

O pacote *nbextensions* permite o uso de uma série de personalizações no seu Jupyter, incluindo a criação de índice (*Table of Contents*) automático na primeira célula, opção de colapsar seções para facilitar andar pelo  código, etc. Vale a pena ver todas em: https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions.html

```bash
# Instala o pacote
$ jupyter contrib nbextension install --user
# Abre o Jupyter no navegador
$ jupyter notebook
```
Uma vez no Jupyter no seu navegador, vai aparecer uma nova aba chamada "Nbextensions" - entre, use e abuse.