#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import re

cols = {
    "city": {"old": "Município", 
             "new": ["city_id", "city_name"]},
    "health_region": {"old": "Região de Saúde (CIR)",
                      "new": ["health_region_id", "health_region_name"]},
}
def padronize_age_range(df, subset_, place_type):
    df_ = df[subset_].copy()
    
    for col in df.columns:
        if re.search("from_",col):
            df[col] = pd.to_numeric(df[col])
    
    df_["from_0_to_9"] = df["from_0_to_4"] + df["from_5_to_9"]
    df_["from_10_to_19"] = df["from_10_to_14"] + df["from_15_to_19"]
    df_["from_20_to_29"] = df["from_20_to_24"] + df["from_25_to_29"]
    df_["from_30_to_39"] = df["from_30_to_34"] + df["from_35_to_39"]
    df_["from_40_to_49"] = df["from_40_to_44"] + df["from_45_to_49"]
    df_["from_50_to_59"] = df["from_50_to_54"] + df["from_55_to_59"]
    df_["from_60_to_69"] = df["from_60_to_64"] + df["from_65_to_69"]
    df_["from_70_to_79"] = df["from_70_to_74"] + df["from_75_to_79"]
    df_["from_80_to_older"] = df["from_80_to_older"].astype(int)
    
    df_ = df_.set_index(subset_[0])
    
    filename = f"data/treated/br_{place_type}_tabnet_age_dist_2019_treated.csv"
    print(f"Writing: {filename}")
    df_.to_csv(filename)
    print("Done!")
    return
  
def treat_data(df, place_type="city"):
    
    # Get ID and city name
    df[cols[place_type]["new"]] = df[cols[place_type]["old"]].str.split(" ", 1, expand=True)
    del df[cols[place_type]["old"]]
    
    # Set ID as index
    df[cols[place_type]["new"][0]] = df[cols[place_type]["new"][0]].astype(int)
    df = df.set_index(cols[place_type]["new"][0], drop=True)

    # Treat columns
    for col in df.columns:
        if "anos" in col:
            age = re.findall("\d+", col)
            if "mais" in col:
                age.append("older")
            df = df.rename(columns={col: "from_"+age[0]+"_to_"+age[1]})
    
    df.columns = df.columns.str.lower()
    df = df.reindex(sorted(df.columns), axis=1)

    # Drop old municipality codes
    if place_type == "city":
        df = df[df["city_name"].str.contains("Município ignorado") == False]
    
    df = df.reset_index()
    id_ = place_type+"_id"
    name_ = place_type+"_name"
    padronize_age_range(df,[id_,name_,'total'],place_type)


if __name__ == "__main__":
    
    city = pd.read_csv('data/raw/br_city_tabnet_age_dist_2019_raw.csv', engine='python',
                      sep=";", encoding="latin-1", skiprows=3, skipfooter=6)
    
    health_region = pd.read_csv('data/raw/br_health_region_tabnet_age_dist_2019_raw.csv', engine='python',
                       sep=";", encoding="latin-1", skiprows=3, skipfooter=5)
    
    treat_data(city, "city")
    treat_data(health_region, "health_region")
       