# Grandes Números Instuticionais

## Descrição

Esse notebook em python contém as extrações e transformações feitas em dados abertos do IBGE e da ANS para se calcular os grandes números institucionais da ImpulsoGov.

## Dependências

As únicas dependências desse notebook são o módulo ``pandas``, para manipulação dos dados, e ``requests``, para baixar diretamente os dados de beneficiários dos planos de saúde.

## Fontes de dados

Os dados utilizados aqui vêm de duas fontes:

- **Beneficiários de planos de saúde**: dados disponibilizados no [TabNet](https://www.ans.gov.br/anstabnet/cgi-bin/dh?dados/tabnet_02.def) pela Agência Nacional de Saúde Suplementar. Podem ser baixados diretamente pela interface ou através de uma request, como é feito nesse notebook. 

- **População estimada, por unidade da federação**: disponíveis no [Sistema IBGE de Recuperação Automática](https://sidra.ibge.gov.br/tabela/6579) (SIDRA)

- **População estimada, por município**: disponíveis no [TabNet](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?ibge/cnv/popsvs2024br.def). Os dados de estimativas populacionais por município também estão disponíveis no SIDRA, no entanto, foram baixados do tabnet pois o arquivo contém também o código IBGE do município.

