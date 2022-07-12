#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import hashlib
import re

import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def percentualcol(df):
    """
    Percentual de preenchimento das colunas
    
    Attributes
    ----------
    df: DataFrame
        Conjunto de dados de interesse
    
    Returns
    -------
    Series
        Percentual de preenchimento de cada coluna do conjunto de dados
    
    """
    return (100* df.count() / len(df)).sort_values(ascending = False)

def percentualisna(df, column):
    """
    Percentual de NA em uma coluna
    
    Attributes
    ----------
    columns: Series
        Coluna de dados de interesse
    
    Returns
    -------
    Series
        Percentual de NA de uma coluna do conjunto de dados
    
    """
    return 100* df[column].isna().sum()/len(df[column]) 

def touppercase(df):
    """
    Aplica caixa alta em todo um df
    
    Attributes
    ----------
    df: DataFrame
        Conjunto de dados de interesse
    
    Returns
    --------
    DataFrame
        O conjunto de dados inicial com todos os caracteres em caixa alta
    """
    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(lambda x: x.str.upper())
    
    return df 

def normalizestrings(df):
    """
    Retira os acentos das palavras e troca espaços múltiplos por um só
    
    Attributes
    ----------
    df: DataFrame
        Conjunto de dados de interesse
    
    Returns
    -------
    DataFrame
        O conjunto de dados inicial com todos os caracteres sem acentuação, espaços múltiplos e espaços remanescentes no final
    """
    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(lambda x: x.astype(str).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8') if x.dtype == object else x)
    df[cols] = df[cols].apply(lambda x: x.astype(str).str.replace(' +', ' ') if x.dtype == object else x)
    df[cols] = df[cols].apply(lambda x: x.astype(str).str.strip() if x.dtype == object else x)
    
    return df

def normalizecpf(column):
    """
    Retira pontuação em na coluna com CPF
    
    Attributes
    ----------
    column: Series
        Coluna de dados de interesse
    
    Returns
    -------
    Series 
        A coluna inicial com sem pontuação
    """
    CPF_PAT = '[^0-9]'
    cpfs = [re.sub(CPF_PAT,'',str(d)) if re.search(CPF_PAT,str(d)) else d for d in column]
    
    return cpfs

def normalizedata(column, formato):
    """
    Normaliza a data para o formato %Y/%m/%d
    
    Attributes
    ----------
    column: Series
        Coluna de dados de interesse
       
    Returns
    -------
    Series 
        A coluna inicial com o formato YYYY/MM/DD
    """
    column = pd.to_datetime(column, format = formato)
    column = column.dt.strftime('%Y/%m/%d')
    
    return column

def normalizetipoidade(column,dict_tipos):
    """
    Normaliza o tipo de idade para DIAS, MESES, ANOS
    
    Attributes
    ----------
    column: Series
        Coluna de dados de interesse
    tipos: dict
        Dicionário com mapeamento entre o tipo de idade antigo e o novo
    Returns
    -------
    Series  
        A coluna inicial com o formato YYYY/MM/DD
    """
    column = column.map(dict_tipos)
    return column

def setanonasc(dt_nasc):
    """
    Adiciona ao dataframe uma coluna com o ano de nascimento
    
    Attributes
    ----------    
    dt_nasc: Series
        Coluna de dados com datas de nascimento
        
    Returns
    -------
    Series 
       Coluna com os anos de dt_nasc
    """
    ano_nasc = (pd.DatetimeIndex(dt_nasc).year).astype('Int32') 
    return ano_nasc


def addidadeatualizada(column):
    """
    Adiciona a idade levando em consideração o dia de hoje
    
    Attributes
    ---------- 
    df: DataFrame
        Conjunto de dados de interesse
    column: Series
        Coluna de dados com datas de nascimento no formato YYYY/MM/DD
        
    Returns
    -------
    Series 
       Conjunto de dados com coluna de idade atualizada
    """
    
    now = pd.to_datetime('today').year
    idade_atualizada = (now - pd.DatetimeIndex(pd.to_datetime(column, format = '%Y/%m/%d')).year)
    return idade_atualizada


def removeduplicatas(df, column_date,subset_):
    """
    Remove pacientes de múltiplas entradas preservando a última data de entrada
    
    Attributes
    ---------- 
    df: DataFrame
        Conjunto de dados de interesse
    column_date: Serie
        Coluna de dados com as datas de entrada
    subset_ : List
        Lista com nome das colunas para ser comparadas para definição de duplicatas
    
    Returns
    -------
    Series 
       Conjunto de dados com coluna de idade atualizada
    """
    
    df_drop = df.sort_values(by=column_date, ascending=False)

    df_drop = df_drop.drop_duplicates(subset = subset_,keep = 'first') 
    return df_drop
 
def percentualduplicatas(df,df_drop, df_duplicate, subset_):
    """
    Indica o percentual de duplicatas dos dados
    
    Attributes
    ---------- 
    df: DataFrame
        Conjunto de dados de interesse
    df_drop: DataFrame
        Conjunto de dados sem duplicatas
    df_duplicate: DataFrame
        Conjunto de dados apenas de duplicatas
    subset_ : List
        Lista com nome das colunas para ser comparadas para definição de duplicatas
    
    Returns
    -------
    Int 
       Percentual de duplicatas que estavam presentes no df inicial.
    """
    n_duplicadas = len(df_duplicate[subset_[0]])
    n_unicas = len(df_duplicate.drop_duplicates(subset = subset_))
    n_df = len(df)
    n_df_drop = len(df_drop)
    if((n_df - n_duplicadas + n_unicas) == n_df_drop):
        return (100 *(1 - n_df_drop/n_df))
    else:
        return None

def anonimizadados(df,column_paciente,column_idade,subset_):
    """
    Anonimiza os dados: gera um hash levando em consideração o nome do paciente e a idade
    
    Attributes
    ---------- 
    df: DataFrame
        Conjunto de dados de interesse
    column_paciente: Series
        Coluna com os nomes dos pacientes
    column_idade: Series
        Coluna com idade dos pacientes
    subset_ : List
        Lista com nome das colunas para anonimizar
    
    Returns
    -------
    DataFrame 
       Conjunto de dados inicial anonimizado e com um id
    """
    
    df['nome_idade'] = df[column_paciente] + df[column_idade].apply(str)
    
    df[subset_] = np.nan
    df['id'] = [hashlib.md5(bytes(val,encoding='utf8')).hexdigest() for val in df['nome_idade']]
    df.drop('nome_idade', axis=1, inplace=True)
    
    return df
