import pandas as pd

RAW_DATA_DIR = "data/raw_data"
agg_inscription = pd.read_csv(f"{RAW_DATA_DIR}/agg_inscription.csv")
btc_fee_size = pd.read_csv(f"{RAW_DATA_DIR}/btc_fee_size.csv")
daily_btcusd = pd.read_csv(f"{RAW_DATA_DIR}/daily_btcusd.csv")
inscription_df = pd.read_csv(f"{RAW_DATA_DIR}/inscription_by_category.csv")

# Merge the dataframes on the 'DATE' column
df = pd.merge(agg_inscription, btc_fee_size, on="DATE")
df = pd.merge(df, daily_btcusd, on="DATE")
df.loc[:, "Ord_Daily_fees_USD"] = df.Ord_Daily_fees * df.Price
df.loc[:, "Ord_Total_fees_USD"] = df.Ord_Total_fees * df.Price
df.loc[:, "btc_Daily_fees_USD"] = df.btc_Daily_fee * df.Price
df["Ord_Daily_fees_vSize"] = df["Ord_Daily_fees"] / df["Ord_vSize_Usage"] * 100000000
df["Ord_Daily_fees_vSize_USD"] = df["Ord_Daily_fees_USD"] / df["Ord_vSize_Usage"]
df["btc_Daily_fees_vSize"] = df["btc_Daily_fee"] / df["btc_vSize_Usage"] * 100000000
df["btc_Daily_fees_vSize_USD"] = df["btc_Daily_fees_USD"] / df["btc_vSize_Usage"]


inscription_df = inscription_df.merge(
    df.loc[:, ["DATE", "Price"]], left_on="DATE", right_on="DATE"
)
inscription_df = inscription_df.merge(
    df.loc[:, ["DATE", "btc_Daily_fee"]], left_on="DATE", right_on="DATE"
)
inscription_df.loc[:, "Ord_Daily_fees_USD"] = (
    inscription_df.Ord_Daily_fees * inscription_df.Price
)
inscription_df.loc[:, "Ord_Daily_fees_USD_byte"] = (
    inscription_df.Ord_Daily_fees_USD / inscription_df.Ord_Size
)
inscription_df.loc[:, "Ord_Daily_fees_USD_vbyte"] = (
    inscription_df.Ord_Daily_fees_USD / inscription_df.Ord_vSize
)
inscription_df.loc[:, "Ord_Daily_fees_byte"] = (
    inscription_df.Ord_Daily_fees / inscription_df.Ord_Size * 100000000
)
inscription_df.loc[:, "Ord_Daily_fees_vbyte"] = (
    inscription_df.Ord_Daily_fees / inscription_df.Ord_vSize * 100000000
)
inscription_df.loc[:, "Ord_Daily_fees_byte_Per_Inscription"] = (
    inscription_df.Ord_Daily_fees_byte / inscription_df.Inscriptions
)
inscription_df.loc[:, "Ord_Daily_fees_vbyte_Per_Inscription"] = (
    inscription_df.Ord_Daily_fees_vbyte / inscription_df.Inscriptions
)
inscription_df.loc[:, "Ord_Daily_fees_USD_vbyte_Per_Inscription"] = (
    inscription_df.Ord_Daily_fees_USD_vbyte / inscription_df.Inscriptions
)
inscription_df.loc[:, "Ord_Daily_fees_USD_byte_Per_Inscription"] = (
    inscription_df.Ord_Daily_fees_USD_byte / inscription_df.Inscriptions
)
inscription_df.loc[:, "Ord_Size_Per_Inscription"] = (
    inscription_df.Ord_Size / inscription_df.Inscriptions
)
inscription_df.loc[:, "Ord_vSize_Per_Inscription"] = (
    inscription_df.Ord_vSize / inscription_df.Inscriptions
)
# Graph params
rangeselector_param = dict(
    buttons=[
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all"),
    ]
)
tickformatstops_param = [
    dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
    dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
    dict(dtickrange=[60000, 3600000], value="%H:%M m"),
    dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
    dict(dtickrange=[86400000, 604800000], value="%y-%b-%e"),
    dict(dtickrange=[604800000, "M1"], value="%b %Y"),
    dict(dtickrange=["M1", "M12"], value="%b %Y"),
    dict(dtickrange=["M12", None], value="%Y"),
]
mime_category_order = {
    "MIME_types": [
        "text",
        "image",
        "application",
        "model",
        "video",
        "audio",
        "other",
    ]
}


# df.to_csv("data/clean_data/df.csv")
# inscription_df.to_csv("data/clean_data/inscription_df.csv")
####################################################################################################
# Custom functions
####################################################################################################
def custom_legend_name(figure, new_names: list):
    for i, new_name in enumerate(new_names):
        figure.data[i].name = new_name


def default_update_xaxes(figure):
    figure.update_xaxes(
        title_text="Date",
        rangeslider_visible=True,
        rangeselector=rangeselector_param,
        tickformatstops=tickformatstops_param,
    )
