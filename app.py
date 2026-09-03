"""Interactive dashboard for the U.S. Small Business Capital Access Atlas."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from capital_access_atlas import (
    CENSUS_CBP_2023,
    SBA_STATE_DATASET,
    build_composite_index,
    detect_state_column,
    leave_one_metric_out_sensitivity,
    load_cbp_state_file,
    load_sba_state_workbook,
    metric_quality_report,
    numeric_metric_columns,
    prepare_state_metric,
    summarize_cbp_state_totals,
)

REPOSITORY_URL = "https://github.com/sakera023/us-small-business-capital-access-atlas"
LIVE_URL = "https://capital-access-atlas-sakera.streamlit.app/"

st.set_page_config(
    page_title="U.S. Small Business Capital Access Atlas",
    page_icon="🗺️",
    layout="wide",
)

st.title("U.S. Small Business Capital Access Atlas")
st.caption(
    "A public, reproducible geospatial research platform for examining small-business "
    "activity, regional opportunity, and capital-access context across the United States."
)
st.info(
    "Research and educational use only. The Atlas analyzes aggregate geographic data "
    "and does not make applicant-level credit, lending, investment, or eligibility decisions."
)

link_repo, link_live, link_sba, link_census = st.columns(4)
with link_repo:
    st.link_button("GitHub Repository", REPOSITORY_URL, use_container_width=True)
with link_live:
    st.link_button("Public Atlas", LIVE_URL, use_container_width=True)
with link_sba:
    st.link_button(
        "Official SBA Source",
        SBA_STATE_DATASET["landing_page"],
        use_container_width=True,
    )
with link_census:
    st.link_button(
        "Official Census CBP",
        CENSUS_CBP_2023["landing_page"],
        use_container_width=True,
    )


@st.cache_data(ttl=3600, show_spinner=False)
def load_official_sba_data():
    return load_sba_state_workbook()


@st.cache_data(ttl=86400, show_spinner=False)
def load_official_cbp_data():
    raw = load_cbp_state_file()
    return summarize_cbp_state_totals(raw)


def available_state_sheets(sheets: dict[str, pd.DataFrame]) -> dict[str, str]:
    detected: dict[str, str] = {}
    for sheet_name, frame in sheets.items():
        state_column = detect_state_column(frame)
        if state_column:
            detected[sheet_name] = state_column
    return detected


with st.sidebar:
    st.header("Official public data")
    st.caption("Load one or both authoritative public datasets.")

    if st.button("Load SBA state dataset", type="primary", use_container_width=True):
        try:
            with st.spinner("Loading the official SBA workbook..."):
                st.session_state["sba_workbook"] = load_official_sba_data()
        except Exception as exc:
            st.error(
                "Unable to load the official SBA workbook right now. "
                f"Source error: {exc}"
            )

    if st.button("Load Census CBP state data", use_container_width=True):
        try:
            with st.spinner("Loading the Census 2023 CBP state file..."):
                st.session_state["cbp_state"] = load_official_cbp_data()
        except Exception as exc:
            st.error(
                "Unable to load the official Census CBP state file right now. "
                f"Source error: {exc}"
            )

    if "sba_workbook" in st.session_state:
        metadata, sheets = st.session_state["sba_workbook"]
        st.success("SBA data loaded")
        st.caption(f"SBA vintage/update: {metadata.get('last_modified') or 'not reported'}")

    if "cbp_state" in st.session_state:
        st.success("Census CBP data loaded")
        st.caption(f"Census vintage: {CENSUS_CBP_2023['vintage']}")

tabs = st.tabs(
    [
        "Atlas Overview",
        "SBA National Map",
        "Census CBP",
        "State Comparison",
        "Index Lab",
        "Data Quality",
        "Sources & Methodology",
    ]
)

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Official sources integrated", "2")
    c2.metric("Geographic focus", "U.S. states")
    c3.metric("Public deployment", "Live")
    c4.metric("Index status", "Research prototype")

    st.subheader("Research purpose")
    st.write(
        "The Atlas studies place-based differences in entrepreneurship, business scale, "
        "employment, payroll, and capital-support context using transparent public data. "
        "The goal is to make geographic evidence easier to inspect, reproduce, and extend."
    )

    st.subheader("Current capabilities")
    st.markdown(
        "- Official SBA State Small Business Statistics 2025 integration\n"
        "- Official U.S. Census County Business Patterns 2023 state-file integration\n"
        "- Interactive U.S. state choropleths and rankings\n"
        "- Multi-state comparison workflows\n"
        "- Downloadable map-ready tables\n"
        "- Exploratory Capital Access Opportunity Index Lab\n"
        "- Data-quality and leave-one-metric-out sensitivity diagnostics\n"
        "- Tested Python research utilities and automated CI"
    )

    st.subheader("Research boundary")
    st.write(
        "Maps and composite scores summarize selected aggregate indicators. They do not "
        "establish causation, discrimination, legal conclusions, or individual creditworthiness."
    )

with tabs[1]:
    st.subheader("SBA State Small-Business Atlas")

    if "sba_workbook" not in st.session_state:
        st.warning("Load the official SBA state dataset from the sidebar to activate this tab.")
    else:
        metadata, sheets = st.session_state["sba_workbook"]
        state_sheets = available_state_sheets(sheets)

        if not state_sheets:
            st.error("No state-level worksheet could be detected in the current SBA workbook.")
        else:
            sheet_name = st.selectbox("SBA worksheet", list(state_sheets), key="sba_map_sheet")
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)

            if not metrics:
                st.warning("No numeric state-level measures were detected in this worksheet.")
            else:
                metric = st.selectbox("SBA measure", metrics, key="sba_map_metric")
                mapped = prepare_state_metric(frame, metric, state_column)

                fig = px.choropleth(
                    mapped,
                    locations="state",
                    locationmode="USA-states",
                    color="value",
                    scope="usa",
                    hover_name="state_name",
                    title=f"SBA State Atlas — {metric}",
                    labels={"value": metric},
                )
                fig.update_layout(margin={"r": 0, "t": 55, "l": 0, "b": 0})
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(mapped, use_container_width=True, hide_index=True)
                st.download_button(
                    "Download SBA map data as CSV",
                    mapped.to_csv(index=False).encode("utf-8"),
                    file_name="sba_state_atlas_metric.csv",
                    mime="text/csv",
                )
                st.caption(
                    "Values are derived from the selected official SBA worksheet. "
                    "If multiple source rows map to a state, values are averaged for visualization."
                )

with tabs[2]:
    st.subheader("U.S. Census County Business Patterns — State View")

    if "cbp_state" not in st.session_state:
        st.warning("Load the Census CBP state data from the sidebar to activate this tab.")
    else:
        cbp = st.session_state["cbp_state"].copy()
        cbp_metrics = [
            column
            for column in [
                "establishments",
                "employment",
                "annual_payroll_thousands",
                "q1_payroll_thousands",
            ]
            if column in cbp.columns
        ]

        metric = st.selectbox("CBP measure", cbp_metrics, key="cbp_metric")
        fig = px.choropleth(
            cbp,
            locations="state",
            locationmode="USA-states",
            color=metric,
            scope="usa",
            hover_name="state_name",
            hover_data={metric: ":,.0f"},
            title=f"Census CBP 2023 — {metric.replace('_', ' ').title()}",
        )
        fig.update_layout(margin={"r": 0, "t": 55, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            cbp.sort_values(metric, ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "Download Census CBP state totals as CSV",
            cbp.to_csv(index=False).encode("utf-8"),
            file_name="census_cbp_2023_state_totals.csv",
            mime="text/csv",
        )
        st.caption(
            "CBP measures summarize establishments with paid employees. "
            "Payroll fields are reported in the source file's published units."
        )

with tabs[3]:
    st.subheader("State Comparison")

    source = st.radio(
        "Comparison source",
        ["SBA", "Census CBP"],
        horizontal=True,
    )

    if source == "SBA":
        if "sba_workbook" not in st.session_state:
            st.info("Load SBA data from the sidebar.")
        else:
            _, sheets = st.session_state["sba_workbook"]
            state_sheets = available_state_sheets(sheets)
            if state_sheets:
                sheet_name = st.selectbox(
                    "SBA worksheet",
                    list(state_sheets),
                    key="comparison_sba_sheet",
                )
                frame = sheets[sheet_name]
                state_column = state_sheets[sheet_name]
                metrics = numeric_metric_columns(frame, state_column)
                if metrics:
                    metric = st.selectbox(
                        "Measure",
                        metrics,
                        key="comparison_sba_metric",
                    )
                    comparison_source = prepare_state_metric(frame, metric, state_column)
                    value_column = "value"
                    label = metric
                else:
                    comparison_source = pd.DataFrame()
            else:
                comparison_source = pd.DataFrame()
    else:
        if "cbp_state" not in st.session_state:
            st.info("Load Census CBP data from the sidebar.")
            comparison_source = pd.DataFrame()
        else:
            comparison_source = st.session_state["cbp_state"].copy()
            options = [
                column
                for column in [
                    "establishments",
                    "employment",
                    "annual_payroll_thousands",
                    "q1_payroll_thousands",
                ]
                if column in comparison_source.columns
            ]
            metric = st.selectbox("Measure", options, key="comparison_cbp_metric")
            value_column = metric
            label = metric.replace("_", " ").title()

    if "comparison_source" in locals() and not comparison_source.empty:
        state_names = comparison_source["state_name"].dropna().tolist()
        selected_states = st.multiselect(
            "Select states",
            state_names,
            default=state_names[: min(5, len(state_names))],
        )
        comparison = comparison_source[
            comparison_source["state_name"].isin(selected_states)
        ].copy()

        if not comparison.empty:
            fig = px.bar(
                comparison.sort_values(value_column),
                x=value_column,
                y="state_name",
                orientation="h",
                title=f"Selected State Comparison — {label}",
                labels={value_column: label, "state_name": "State"},
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(
                comparison.sort_values(value_column, ascending=False),
                use_container_width=True,
                hide_index=True,
            )

with tabs[4]:
    st.subheader("Capital Access Opportunity Index Lab")
    st.write(
        "Build an exploratory composite from numeric measures in an official SBA "
        "worksheet. The score is transparent and configurable, but it is not an "
        "official index or lending score."
    )

    if "sba_workbook" not in st.session_state:
        st.warning("Load SBA data from the sidebar to use the Index Lab.")
    else:
        _, sheets = st.session_state["sba_workbook"]
        state_sheets = available_state_sheets(sheets)

        if state_sheets:
            sheet_name = st.selectbox("Worksheet", list(state_sheets), key="index_sheet")
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)

            selected_metrics = st.multiselect(
                "Choose component measures",
                metrics,
                default=metrics[: min(3, len(metrics))],
                key="index_metrics",
            )

            if selected_metrics:
                weights: dict[str, float] = {}
                weight_columns = st.columns(min(3, len(selected_metrics)))
                for index, metric_name in enumerate(selected_metrics):
                    with weight_columns[index % len(weight_columns)]:
                        weights[metric_name] = st.number_input(
                            f"Weight: {metric_name}",
                            min_value=0.0,
                            max_value=10.0,
                            value=1.0,
                            step=0.25,
                            key=f"weight::{metric_name}",
                        )

                inverse = set(
                    st.multiselect(
                        "Measures where lower values should produce a higher score",
                        selected_metrics,
                        key="inverse_metrics",
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
                    st.dataframe(index_frame, use_container_width=True, hide_index=True)

                    if len(selected_metrics) >= 2:
                        sensitivity = leave_one_metric_out_sensitivity(
                            frame,
                            state_column=state_column,
                            metric_weights=weights,
                            inverse_metrics=inverse,
                        )
                        st.subheader("Leave-one-metric-out sensitivity")
                        st.dataframe(sensitivity, use_container_width=True, hide_index=True)

                    st.warning(
                        "Index results depend on source measures, transformations, missingness, "
                        "and weights. They should be interpreted as exploratory research outputs."
                    )

with tabs[5]:
    st.subheader("Data Quality Diagnostics")

    if "sba_workbook" not in st.session_state:
        st.warning("Load SBA data from the sidebar to inspect worksheet quality.")
    else:
        _, sheets = st.session_state["sba_workbook"]
        state_sheets = available_state_sheets(sheets)
        if state_sheets:
            sheet_name = st.selectbox(
                "Worksheet",
                list(state_sheets),
                key="quality_sheet",
            )
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)

            selected = st.multiselect(
                "Metrics to inspect",
                metrics,
                default=metrics[: min(6, len(metrics))],
                key="quality_metrics",
            )
            if selected:
                quality = metric_quality_report(frame, selected)
                st.dataframe(quality, use_container_width=True, hide_index=True)
                st.download_button(
                    "Download data-quality report",
                    quality.to_csv(index=False).encode("utf-8"),
                    file_name="atlas_data_quality_report.csv",
                    mime="text/csv",
                )

    if "cbp_state" in st.session_state:
        st.subheader("Census CBP state coverage")
        cbp = st.session_state["cbp_state"]
        st.metric("States / DC represented", int(cbp["state"].nunique()))
        st.dataframe(
            metric_quality_report(
                cbp,
                [
                    column
                    for column in [
                        "establishments",
                        "employment",
                        "annual_payroll_thousands",
                        "q1_payroll_thousands",
                    ]
                    if column in cbp.columns
                ],
            ),
            use_container_width=True,
            hide_index=True,
        )

with tabs[6]:
    st.subheader("Public Data Provenance")
    st.markdown(
        f"**SBA:** {SBA_STATE_DATASET['label']}  \n"
        f"Publisher: {SBA_STATE_DATASET['publisher']}  \n"
        f"Source: {SBA_STATE_DATASET['landing_page']}  \n\n"
        f"**Census:** {CENSUS_CBP_2023['label']}  \n"
        f"Publisher: {CENSUS_CBP_2023['publisher']}  \n"
        f"Source: {CENSUS_CBP_2023['landing_page']}"
    )

    st.subheader("Methodological principles")
    st.markdown(
        "1. **Public-data provenance:** every integrated dataset has a named "
        "publisher and source.\n"
        "2. **Geographic transparency:** state/county identifiers and vintage are retained.\n"
        "3. **Component visibility:** composite scores remain inspectable.\n"
        "4. **Sensitivity analysis:** rankings should be tested against metric removal "
        "and weighting.\n"
        "5. **No applicant underwriting:** this is a place-based research platform.\n"
        "6. **No causal overclaiming:** geographic association is not proof of causation."
    )

    st.caption(
        "See the repository documentation for source notes, index methodology, validation, "
        "case studies, citation guidance, and contribution standards."
    )
