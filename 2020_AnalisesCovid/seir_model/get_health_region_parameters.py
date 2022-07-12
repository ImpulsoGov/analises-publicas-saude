import pandas as pd
from pathlib import Path
import numpy as np

# from endpoints.helpers import allow_local


def gen_fatality_ratio(pop, place_id, config):
    # Add fatality ratio
    config["br"]["seir_parameters"]["ifr_by_age_perc"] = {
        "from_0_to_9": 0.00002,
        "from_10_to_19": 0.00006,
        "from_20_to_29": 0.0003,
        "from_30_to_39": 0.0008,
        "from_40_to_49": 0.0015,
        "from_50_to_59": 0.006,
        "from_60_to_69": 0.022,
        "from_70_to_79": 0.051,
        "from_80_to_older": 0.093,
    }

    return (
        pop.drop(columns=[col for col in pop.columns if "_id" in col])
        .apply(lambda row: row / row["total"], axis=1)
        .drop(columns=["total"])
        .dot(pd.Series(config["br"]["seir_parameters"]["ifr_by_age_perc"]))
    )


def gen_infection_proportion(df, pop, place_id, config):

    # Get total perc of hospitalized weighted by age
    df["hospitalized_by_age_perc"] = (
        pop.drop(columns=[col for col in pop.columns if "_id" in col])
        .apply(lambda row: row / row["total"], axis=1)
        .drop(columns=["total"])
        .dot(pd.Series(config["br"]["seir_parameters"]["hospitalized_by_age_perc"]))
    )

    i3_perc = config["br"]["seir_parameters"]["i3_percentage"]
    i2_perc = config["br"]["seir_parameters"]["i2_percentage"]

    # Get total perc of I2 (severe) & I3 (critical) hospitalized weighted by age
    df["i2_percentage"] = i2_perc * df["hospitalized_by_age_perc"] / (i2_perc + i3_perc)
    df["i3_percentage"] = i3_perc * df["hospitalized_by_age_perc"] / (i2_perc + i3_perc)
    df["i1_percentage"] = 1 - df["i2_percentage"] - df["i3_percentage"]

    return df


def gen_stratified_parameters(config, place_id):
    # Get stratified pop data
    pop = (
        pd.read_csv(
            Path(
                "br_health_region_tabnet_age_dist_2019_treated.csv"
            ).resolve()
        )
        .assign(
            state_num_id=lambda df: df["health_region_id"].apply(
                lambda x: int(str(x)[:2])
            )
        )
        .groupby(place_id)
        .sum()
    )

    df = pd.DataFrame()
    df = gen_infection_proportion(df, pop, place_id, config)
    df["fatality_ratio"] = gen_fatality_ratio(pop, place_id, config)

    return df


# @allow_local
def now(config):
    return gen_stratified_parameters(config, "health_region_id")


TESTS = {
    "df is not pd.DataFrame": lambda df: isinstance(df, pd.DataFrame),
    "dataframe has null data": lambda df: all(df.isnull().any() == False),
}
