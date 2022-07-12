import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

indicators_cols = {
    "v1": {
        "rt_10days_ago_most_likely": "rt_classification",
        "dday_beds_best": "dday_classification",
        "notification_rate": "subnotification_classification"
    },
    "v2": {
        "rt_most_likely": "control_classification",
        "dday_icu_beds": "capacity_classification",
        "notification_rate": "trust_classification",
        "daily_cases_mavg_100k": "situation_classification"
    },
    "v2_review_rt": {
        "rt_most_likely": "control_classification",
        "dday_icu_beds": "capacity_classification",
        "notification_rate": "trust_classification",
        "daily_cases_mavg_100k": "situation_classification"
    }
    
}

def gen_classification_table(df, sample, version):
    cols = indicators_cols[version].values()
    return df[df["city_id"].isin(sample)][cols].apply(pd.Series.value_counts)

def gen_indicators_table(df, sample, version):
    cols = indicators_cols[version].keys()
    return df[df["city_id"].isin(sample)][cols].describe()

def gen_summary(df, version, colors, config, cities=False):
    """
    Plota a distribuição dos indicadores de classificação da versão do Farol.
    """
    
    plt.rcParams['figure.figsize']=(10,10)
    
    if df.dtypes["overall_alert"] != str:
        df["overall_alert"] = df["overall_alert"].map(config["br"]["farolcovid"]["categories"])
    
    # remove health_region rts
    if version == "v2" and cities == True:
        df = df[df["rt_place_type"] != "health_region_id"]   
        
    cols = list(indicators_cols[version].keys()) + ["overall_alert"]
    print(df["overall_alert"].value_counts())
    return sns.pairplot(df[cols].dropna(), 
                        diag_kind="hist", 
                        hue="overall_alert", 
                        palette=colors)