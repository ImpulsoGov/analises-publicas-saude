import pandas as pd
import yaml 
import requests
import numpy as np

def get_config(url):
    return yaml.load(requests.get(url).text, Loader=yaml.FullLoader)

def get_cases_series(df, place_id, min_days):
    # get total daily cases for place
    df = (
        df[[place_id, "last_updated", "daily_cases"]]
        .groupby([place_id, "last_updated"])["daily_cases"]
        .sum()
        .reset_index()
    )

    # get cases mavg
    df = (
        df.groupby([place_id])
        .rolling(7, window_period=7, on="last_updated")["daily_cases"]
        .mean()
        .dropna()
        .round(0)
    )

    # more than 14 days
    v = df.reset_index()[place_id].value_counts()
    return df[df.index.isin(v[v > min_days].index, level=0)]

def get_infectious_period_cases(df, window_period, cases_params, place_id):

    # Soma casos diários dos últimos dias de progressão da doença
    daily_active_cases = (
        df.set_index("last_updated")
        .groupby(place_id)["daily_cases"]
        .rolling(min_periods=1, window=window_period)
        .sum()
        .reset_index()
    )
    df = df.merge(
        daily_active_cases, on=[place_id, "last_updated"], suffixes=("", "_sum")
    ).rename(columns=cases_params["rename"])

    return df


def _get_growth(group):
    if group["diff_5_days"].values == 5:
        return "crescendo"
    elif group["diff_14_days"].values == -14:
        return "decrescendo"
    else:
        return "estabilizando"


def get_mavg_indicators(df, col, place_id, weighted=True):

    df = df.sort_values([place_id, "last_updated"])

    if weighted:
        divide = df["population"] / 10 ** 5
    else:
        divide = 1

    # Cria coluna mavg
    df_mavg = df.assign(
        mavg=lambda df: df.groupby(place_id)
        .rolling(7, window_period=7, on="last_updated")[col]
        .mean()
        .round(1)
        .reset_index(drop=True)
    )

    df_mavg = df_mavg.assign(mavg_100k=lambda df: df["mavg"] / divide).reset_index(drop=True)

    # Cria colunas auxiliares para tendencia
    df_mavg = (
        df_mavg.assign(
            diff=lambda df: np.sign(df.groupby(place_id)["mavg_100k"].diff())
        )
        .assign(
            diff_5_days=lambda df: df.groupby(place_id)
            .rolling(5, window_period=5, on="last_updated")["diff"]
            .sum()
            .reset_index(drop=True)
        )
        .assign(
            diff_14_days=lambda df: df.groupby(place_id)
            .rolling(14, window_period=14, on="last_updated")["diff"]
            .sum()
            .reset_index(drop=True)
        )
    )

    # Calcula tendência
    df_mavg = df_mavg.assign(
        growth=lambda df: df.groupby([place_id, "last_updated"])
        .apply(_get_growth)
        .reset_index(drop=True)
    )

    return df.merge(
        df_mavg[["mavg", "mavg_100k", "growth", place_id, "last_updated"]],
        on=[place_id, "last_updated"],
    ).rename(
        columns={
            "mavg": col + "_mavg",
            "mavg_100k": col + "_mavg_100k",
            "growth": col + "_growth",
        }
    )