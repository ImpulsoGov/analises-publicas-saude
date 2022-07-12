import pandas as pd
from pathlib import Path
import numpy as np

def _calculate_recovered(df, params):

    confirmed_adjusted = int(df[["confirmed_cases"]].sum() / df["notification_rate"])

    if confirmed_adjusted == 0:  # dont have any cases yet
        params["population_params"]["R"] = 0
        return params

    params["population_params"]["R"] = (
        confirmed_adjusted
        - params["population_params"]["I"]
        - params["population_params"]["D"]
    )

    if params["population_params"]["R"] < 0:
        params["population_params"]["R"] = (
            confirmed_adjusted - params["population_params"]["D"]
        )

    return params

def main(row, place_id, config, place_specific_params):
    """
    row: pd.Series
        Series with population, active_cases, deaths
    """

    # based on Alison Hill: 40% asymptomatic
    symtomatic = [
        int(
            row["active_cases"]
            * config["br"]["seir_parameters"]["asymptomatic_proportion"]
        )
        if not np.isnan(row["active_cases"])
        else 1
    ][0]

    params = {
        "population_params": {
            "N": int(row["population"]),
            "I": symtomatic,
            "D": [int(row["deaths"]) if not np.isnan(row["deaths"]) else 0][0],
        },
        "place_specific_params": {
            "fatality_ratio": place_specific_params["fatality_ratio"].loc[int(row.name)],
            "i1_percentage": place_specific_params["i1_percentage"].loc[int(row.name)],
            "i2_percentage": place_specific_params["i2_percentage"].loc[int(row.name)],
            "i3_percentage": place_specific_params["i3_percentage"].loc[int(row.name)],
        },
        "n_beds": row["number_beds"]
        * config["br"]["simulacovid"]["resources_available_proportion"],
        "n_icu_beds": row["number_icu_beds"],
        "R0": {
            "best": row["rt_most_likely"],  # só usamos o "best" neste caso
            "worst": row["rt_high_95"],
        },
    }
    
    return _calculate_recovered(row, params)
    
