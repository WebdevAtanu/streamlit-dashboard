import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
from DB import get_connection

# Session State Data from Dashboard
username = st.session_state.get("selected_user")
paidamt = st.session_state.get("PaidAmount")
userid = st.session_state.get("selected_userid")

st.subheader(f"Date Wise Payments of - {username}")


# Load data with caching to optimize performance
@st.cache_data
def load_data(userId):

    conn = get_connection()

    query = """
        EXEC GetPaymentByUser
            @UserId = ?
    """

    df = pd.read_sql(query, conn, params=[userId])

    return df


try:

    # LOAD DATA
    df = load_data(userid)

    # CONVERT AMOUNT
    df["Amount"] = (
        pd.to_numeric(df["PaidAmount"], errors="coerce").fillna(0).astype(float)
    )

    # GROUP DATA
    pie_df = df.groupby("PaymentDate", as_index=False)["Amount"].sum()

    # CONVERT DATE TO STRING
    pie_df["PaymentDate"] = pie_df["PaymentDate"].astype(str)

    # ECHARTS DATA
    pie_data = [
        {
            "value": row["Amount"],
            "name": row["PaymentDate"],
        }
        for _, row in pie_df.iterrows()
    ]

    # ECHART OPTION
    option = {
        "backgroundColor": "#111827",
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center", "textStyle": {"color": "#ffffff"}},
        "series": [
            {
                "name": "Payments",
                "type": "pie",
                "radius": ["10%", "40%"],
                "avoidLabelOverlap": False,
                "padAngle": 2,
                "itemStyle": {
                    "borderRadius": 6,
                    "borderColor": "#111827",
                    "borderWidth": 2,
                },
                "label": {"show": True, "color": "#ffffff", "formatter": "{b}\n{d}%"},
                "emphasis": {
                    "label": {"show": True, "fontSize": 18, "fontWeight": "bold"}
                },
                "labelLine": {"show": True},
                "animation": True,
                "animationDuration": 2000,
                "animationEasing": "cubicOut",
                "animationDelay": 100,
                "data": pie_data,
            }
        ],
    }

    # DISPLAY ECHART
    st_echarts(
        options=option,
        height="400px",
    )

    st.divider()

    # DATA TABLE
    st.dataframe(df, use_container_width=True)

except Exception as e:

    st.error(f"Error: {e}")
