import streamlit as st


def Stat_Card(data, bg_color="#111827", title="Metric"):

    st.markdown(
        """
        <style>
        .metric-card {
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #2d2d2d;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.18);
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }

        .metric-card:hover {
            border-color: #3b82f6;
            transform: translateY(-2px);
        }

        .metric-title {
            color: #9ca3af;
            font-size: 0.9rem;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }

        .metric-value {
            color: #f3f4f6;
            font-size: 1.6rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card" style="background-color:{bg_color};">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{data}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
