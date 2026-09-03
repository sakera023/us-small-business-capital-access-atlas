"""Interactive public-data dashboard for the U.S. Small Business Capital Access Atlas."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from capital_access_atlas import (
    SBA_STATE_DATASET,
    build_composite_index,
    detect_state_column,
    load_sba_state_workbook,
    prepare_state_metric,
)
from capital_access_atlas.geography import numeric_metric_columns

st.set_page_config(
    page_title="U.S. Small Business Capital Access Atlas",
    page_icon="🗺️",
    layout="wide",
)

st.title("U.S. Small Business Capital Access Atlas")
st.caption(
    "Open-source geospatial research on small-business activity, regional opportunity, "
    "and capital-access conditions using authoritative U.S. public data."
)
st.info(
    "This Atlas analyzes aggregate geographic data. It does not make applicant-level "
    "credit, lending, investment, or eligibility decisions."
)

link_repo, link_sba = st.columns(2)
with link_repo:
    st.link_button(
        "GitHub Repository",
        "https://github.com/sakera023/us-small-business-capital-access-atlas",
        use_container_width=True,
    )
with link_sba:
    st.link_button(
        "Official SBA Source",
        SBA_STATE_DATASET["landing_page"],
        use_container_width=True,
    )


@st.cache_data(ttl=3600, show_spinner=False)
def load_official_sba_data():
    return load_sba_state_workbook()


def _available_state_sheets(sheets: dict[str, pd.DataFrame]) -> dict[str, str]:
    detected: dict[str, str] = {}
    for sheet_name, frame in sheets.items():
        state_column = detect_state_column(frame)
        if state_column:
            detected[sheet_name] = state_column
    return detected


tabs = st.tabs(
    [
        "Atlas Overview",
        "National Map",
        "State Comparison",
        "Index Lab",
        "Data Sources",
        "Methodology",
    ]
)

with tabs[0]:
    c1, c2, c3 = st.columns(3)
    c1.metric("Current official source", "SBA")
    c2.metric("Geographic focus", "U.S. states")
    c3.metric("Index status", "Research prototype")

    st.subheader("Research purpose")
    st.write(
        "The Atlas is designed to identify and communicate place-based differences in "
        "small-business activity and capital-access context. It emphasizes transparent "
        "public data, reproducible transformations, and geographic comparison."
    )

    st.subheader("What is integrated now")
    st.markdown(
        "- SBA State Small Business Statistics 2025\n"
        "- Verified official SBA workbook retrieval\n"
        "- Automatic state and numeric-field detection\n"
        "- Interactive state choropleths and rankings\n"
        "- A transparent user-configurable composite-index laboratory"
    )

    st.subheader("Planned national data layers")
    st.markdown(
        "- U.S. Census County Business Patterns\n"
        "- U.S. Census Annual Business Survey\n"
        "- CDFI Fund institution and investment geography\n"
        "- Bureau of Labor Statistics labor-market indicators\n"
        "- Bureau of Economic Analysis regional economic indicators"
    )

with st.sidebar:
    st.header("Official public data")
    st.caption(SBA_STATE_DATASET["description"])

    if st.button("Load SBA state dataset", type="primary", use_container_width=True):
        try:
            with st.spinner("Loading the current official SBA workbook..."):
                st.session_state["sba_workbook"] = load_official_sba_data()
        except Exception as exc:
            st.error(
            "Unable to load the official SBA workbook right now. "
            f"Source error: {exc}"
        )

    if "sba_workbook" in st.session_state:
        metadata, sheets = st.session_state["sba_workbook"]
        state_sheets = _available_state_sheets(sheets)
        st.success("Official SBA data loaded.")
        st.caption(
            f"Catalog update: {metadata.get('last_modified') or 'not reported'}"
        )
    else:
        metadata, sheets, state_sheets = None, None, {}

if "sba_workbook" not in st.session_state:
    with tabs[1]:
        st.warning("Load the official SBA state dataset from the sidebar to activate maps.")
    with tabs[2]:
        st.warning("Load the official SBA state dataset from the sidebar to compare states.")
    with tabs[3]:
        st.warning("Load the official SBA state dataset from the sidebar to build an index.")
else:
    metadata, sheets = st.session_state["sba_workbook"]
    state_sheets = _available_state_sheets(sheets)

    if not state_sheets:
        with tabs[1]:
            st.error("No state-level worksheet could be detected in the current workbook.")
        with tabs[2]:
            st.error("No state-level worksheet could be detected in the current workbook.")
        with tabs[3]:
            st.error("No state-level worksheet could be detected in the current workbook.")
    else:
        with tabs[1]:
            st.subheader("National State-Level Map")
            sheet_name = st.selectbox(
                "Worksheet",
                list(state_sheets),
                key="map_sheet",
            )
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)

            if not metrics:
                st.warning("No numeric state-level measures were detected in this worksheet.")
            else:
                metric = st.selectbox("Measure", metrics, key="map_metric")
                mapped = prepare_state_metric(frame, metric, state_column)

                fig = px.choropleth(
                    mapped,
                    locations="state",
                    locationmode="USA-states",
                    color="value",
                    scope="usa",
                    hover_name="state_name",
                    title=f"{metric} — U.S. State Atlas",
                    labels={"value": metric},
                )
                fig.update_layout(margin={"r": 0, "t": 55, "l": 0, "b": 0})
                st.plotly_chart(fig, use_container_width=True)

                st.caption(
                    "Map values come from the selected official SBA worksheet. "
                    "When more than one row maps to a state, values are averaged for "
                    "visualization and should be checked against the source table."
                )

                st.subheader("State ranking")
                st.dataframe(mapped, use_container_width=True, hide_index=True)
                st.download_button(
                    "Download mapped state data as CSV",
                    mapped.to_csv(index=False).encode("utf-8"),
                    file_name="atlas_state_metric.csv",
                    mime="text/csv",
                )

        with tabs[2]:
            st.subheader("State Comparison")
            sheet_name = st.selectbox(
                "Worksheet",
                list(state_sheets),
                key="compare_sheet",
            )
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)

            if not metrics:
                st.warning("No numeric comparison measures were detected.")
            else:
                metric = st.selectbox(
                    "Comparison measure",
                    metrics,
                    key="compare_metric",
                )
                mapped = prepare_state_metric(frame, metric, state_column)
                available_states = mapped["state_name"].tolist()
                default_states = available_states[: min(5, len(available_states))]
                selected_states = st.multiselect(
                    "Select states",
                    available_states,
                    default=default_states,
                )

                comparison = mapped[mapped["state_name"].isin(selected_states)].copy()
                if comparison.empty:
                    st.info("Select at least one state.")
                else:
                    fig = px.bar(
                        comparison.sort_values("value"),
                        x="value",
                        y="state_name",
                        orientation="h",
                        title=f"Selected State Comparison — {metric}",
                        labels={"state_name": "State", "value": metric},
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(
                        comparison.sort_values("value", ascending=False),
                        use_container_width=True,
                        hide_index=True,
                    )

        with tabs[3]:
            st.subheader("Capital Access Opportunity Index Lab")
            st.write(
                "Build a transparent exploratory composite from numeric measures in a "
                "selected official worksheet. This is a research laboratory—not an "
                "official index or lending score."
            )

            sheet_name = st.selectbox(
                "Worksheet",
                list(state_sheets),
                key="index_sheet",
            )
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)

            selected_metrics = st.multiselect(
                "Choose component measures",
                metrics,
                default=metrics[: min(3, len(metrics))],
            )

            if selected_metrics:
                weights: dict[str, float] = {}
                weight_columns = st.columns(min(3, len(selected_metrics)))
                for index, metric in enumerate(selected_metrics):
                    with weight_columns[index % len(weight_columns)]:
                        weights[metric] = st.number_input(
                            f"Weight: {metric}",
                            min_value=0.0,
                            max_value=10.0,
                            value=1.0,
                            step=0.25,
                            key=f"weight::{metric}",
                        )

                inverse = set(
                    st.multiselect(
                        "Measures where lower values should produce a higher score",
                        selected_metrics,
                    )
                )

                if sum(weights.values()) <= 0:
                    st.warning("At least one component weight must be greater than zero.")
                else:
                    index_frame = build_composite_index(
                        frame,
                        state_column=state_column,
                        metric_weights=weights,
                        inverse_metrics=inverse,
                    )

                    fig = px.choropleth(
                        index_frame,
                        locations="state",
                        locationmode="USA-states",
                        color="capital_access_index",
                        scope="usa",
                        title="Exploratory Capital Access Opportunity Index",
                        labels={"capital_access_index": "Index score"},
                    )
                    fig.update_layout(margin={"r": 0, "t": 55, "l": 0, "b": 0})
                    st.plotly_chart(fig, use_container_width=True)

                    st.dataframe(
                        index_frame,
                        use_container_width=True,
                        hide_index=True,
                    )
                    st.warning(
                        "This score is calculated only from the measures and weights you "
                        "selected. It has not been externally validated and must not be "
                        "interpreted as an official ranking or a measure of discrimination."
                    )
            else:
                st.info("Select one or more numeric measures to build an exploratory index.")

with tabs[4]:
    st.subheader("Public Data Provenance")
    st.markdown(
        f"**Current integrated source:** {SBA_STATE_DATASET['label']}  \n"
        f"**Publisher:** {SBA_STATE_DATASET['publisher']}  \n"
        f"**Official landing page:** {SBA_STATE_DATASET['landing_page']}"
    )

    if metadata:
        st.markdown(
            f"**Resolved dataset:** {metadata['package_title']}  \n"
            f"**Catalog last modified:** {metadata['last_modified'] or 'Not reported'}  \n"
            f"**License:** {metadata['license_title']}  \n"
            f"**Resolved resource:** {metadata['resource_name']}"
        )

    st.write(
        "Future layers will be added only with documented source provenance, geographic "
        "identifiers, vintage/year, transformation steps, and known limitations."
    )

with tabs[5]:
    st.subheader("Methodological Principles")
    st.markdown(
        "1. **Public data first:** prioritize authoritative U.S. government sources.\n"
        "2. **Geographic transparency:** retain state/county identifiers and source years.\n"
        "3. **Component visibility:** never publish a composite score without its inputs.\n"
        "4. **Sensitivity analysis:** test how weighting and transformations affect rankings.\n"
        "5. **No applicant underwriting:** the Atlas is a place-based research platform.\n"
        "6. **No causal overclaiming:** geographic association is not proof of causation."
    )
