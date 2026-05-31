import streamlit as st
import pandas as pd
from datetime import date, timedelta
from streamlit_echarts import st_echarts
from DB import get_connection
from .Stat_Card import Stat_Card


def Dashboard():
    st.subheader("User Payment Dashboard")  # Page title

    # ========================================== LOAD DATA ==========================================

    @st.cache_data
    def load_data(from_date, to_date):

        conn = get_connection()  # Get connection from DB

        # Execute the SP to get data
        query = """
            EXEC GetAllUserPayments
                @FromDate = ?,
                @ToDate = ?
        """

        df = pd.read_sql(query, conn, params=[from_date, to_date])

        return df

    # ========================================== FILTERS ==========================================

    filter_col1, filter_col2 = st.columns(2)  # This will give two column

    default_from_date = date.today() - timedelta(
        days=7
    )  # Default from date is set to 7 days before

    with filter_col1:
        from_date = st.date_input("From Date", value=default_from_date)

    with filter_col2:
        to_date = st.date_input("To Date", value=date.today())

    # ========================================== MAIN ==========================================

    try:

        df = load_data(from_date, to_date)  # Function call

        if df.empty:
            st.warning("No data found for selected date range.")
            return

        # ========================================== DATA CLEANING ==========================================

        df["PaidAmount"] = (
            pd.to_numeric(df["PaidAmount"], errors="coerce")
            .fillna(0)
            .astype(float)  # Parsing the PaidAmount data to numeric value
        )

        # ========================================== METRICS ============================================

        total_users = len(df)
        total_payment = df["PaidAmount"].sum()
        avg_payment = df["PaidAmount"].mean().round(2)

        # ---------- CARDS ----------
        col1, col2, col3 = st.columns(3)

        with col1:
            Stat_Card(total_users, "#064e3b", "Total Users")

        with col2:
            Stat_Card(total_payment, "#451a03", "Total Payment")

        with col3:
            Stat_Card(avg_payment, "#450a0a", "Average Payment")

        # ======================================== GROUP DATA ============================================

        bar_df = df.groupby(["UserId", "UserName"], as_index=False)["PaidAmount"].sum()

        # ============================================ BAR CHART =================================================

        colors = [
            "#60a5fa",
            "#34d399",
            "#fbbf24",
            "#f87171",
            "#a78bfa",
            "#22d3ee",
            "#fb7185",
            "#4ade80",
        ]

        # PREPARE BAR DATA
        bar_data = []

        for i, (_, row) in enumerate(bar_df.iterrows()):

            bar_data.append(
                {
                    "value": round(row["PaidAmount"], 2),
                    "name": row["UserName"],
                    "userid": row["UserId"],
                    "itemStyle": {
                        "color": colors[i % len(colors)],
                        "borderRadius": [4, 4, 0, 0],
                    },
                }
            )

        # BAR CHART OPTION
        bar_option = {
            "backgroundColor": "#111827",
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
            },
            "xAxis": {
                "type": "category",
                "data": bar_df["UserName"].tolist(),
                "axisLabel": {
                    "color": "#ffffff",
                    "rotate": 40,
                },
                "axisLine": {
                    "lineStyle": {"color": "#6b7280"},
                },
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"color": "#ffffff"},
                "splitLine": {
                    "lineStyle": {"color": "#374151"},
                },
            },
            "series": [
                {
                    "data": bar_data,
                    "type": "bar",
                    "barWidth": "50%",
                    "label": {
                        "show": True,
                        "position": "top",
                        "color": "#ffffff",
                        "formatter": "₹ {c}",
                    },
                    "animationDuration": 2000,
                    "animationEasing": "elasticOut",
                }
            ],
        }

        # ============================ LINE CHART ============================

        line_option = {
            "backgroundColor": "#111827",
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "data": bar_df["UserName"].tolist(),
                "axisLabel": {"color": "#ffffff", "rotate": 40},
                "axisLine": {"lineStyle": {"color": "#6b7280"}},
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"color": "#ffffff"},
                "splitLine": {"lineStyle": {"color": "#374151"}},
            },
            "series": [
                {
                    "data": [
                        {
                            "value": value,
                            "itemStyle": {
                                "color": colors[i % len(colors)],
                                "borderColor": "#ffffff",
                                "borderWidth": 2,
                            },
                        }
                        for i, value in enumerate(
                            bar_df["PaidAmount"].round(2).tolist()
                        )
                    ],
                    "type": "line",
                    "smooth": True,
                    "symbol": "circle",
                    "symbolSize": 12,
                    "lineStyle": {
                        "width": 4,
                        "color": "#60a5fa",
                    },
                    "areaStyle": {
                        "opacity": 0.15,
                        "color": "#60a5fa",
                    },
                    "label": {
                        "show": True,
                        "position": "top",
                        "color": "#ffffff",
                        "formatter": "₹ {c}",
                    },
                    "animationDuration": 2500,
                    "animationEasing": "cubicOut",
                }
            ],
        }

        # ============================ DISPLAY CHARTS ============================

        # CLICK EVENT
        events = {"click": """
            function(params) {

                return {
                    name: params.data.name,
                    userid: params.data.userid
                }

            }
            """}

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### User Payment Chart")

            clicked_data = st_echarts(
                options=bar_option,
                events=events,
                height="400px",
                key="bar_chart",
            )

        # SAFE CHECK
        if (
            clicked_data
            and isinstance(clicked_data, dict)
            and clicked_data.get("chart_event")
        ):

            clicked = clicked_data["chart_event"]

            if clicked:  # extra safety

                st.session_state["selected_user"] = clicked.get("name")
                st.session_state["selected_userid"] = clicked.get("userid")

                st.switch_page("pages/UserPayment.py")

        with col2:
            st.markdown("##### User Payment Trend")

            st_echarts(
                options=line_option,
                height="400px",
            )

        st.divider()

        # ============================ TABLE ============================

        st.subheader("User Wise Payment Data")

        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 2, 1])

        with col1:
            search_text = st.text_input("Search User", placeholder="Enter user name...")

        filtered_df = df.copy()

        if search_text:
            filtered_df = filtered_df[
                filtered_df["UserName"]
                .astype(str)
                .str.lower()
                .str.contains(search_text.lower(), na=False)
            ]

        filtered_df = filtered_df.reset_index(drop=True)

        # ================= ROW SELECTABLE TABLE =================
        event = st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            selection_mode="single-row",
            on_select="rerun",
        )

        # ================= GET SELECTED ROW =================
        selected_rows = event.selection.rows if event and event.selection else []

        selected_row = None

        if selected_rows:
            selected_index = selected_rows[0]
            selected_row = filtered_df.iloc[selected_index]

        # ================= VIEW BUTTON =================
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 2, 1])

        with col1:
            st.info("Select an user to view the details")

        with col5:
            if selected_row is not None:
                if st.button("View User", use_container_width=True):
                    st.session_state["selected_user"] = selected_row["UserName"]
                    st.session_state["selected_userid"] = selected_row["UserId"]

                    st.switch_page("pages/UserPayment.py")
            else:
                st.button("View User", use_container_width=True, disabled=True)

    except Exception as e:
        st.error(f"Error: {e}")
