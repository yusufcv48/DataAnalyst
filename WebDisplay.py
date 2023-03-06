from Source import *
import streamlit as st

def disp_stock(data):
    chart = data
    for i in chart:
        chart_open = chart[i]["data"].set_index(["time"]).copy().open
        chart_open.name = "Open"
        chart_outlier = chart[i]["outlier"]
        chart_outlier.name = "Outliers"
        display_data = pd.concat([chart_open, chart_outlier], axis=1)
        st.subheader(i)
        st.line_chart(display_data)
        st.write(display_data)

def disp_corr():
    CORR = find_corr()
    st.subheader("CORELATION")
    st.write(CORR["data"])
    st.write(CORR["corr"])

get_all_stock_outlier()
disp_stock(DATA)
disp_corr()