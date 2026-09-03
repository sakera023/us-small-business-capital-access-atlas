"""Interactive dashboard for the U.S. Small Business Capital Access Atlas."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from capital_access_atlas import (
    CDFI_CERTIFICATION,
    CENSUS_CBP_2023,
    CENSUS_TIGER_COUNTY_2023,
    NORMALIZATION_METHODS,
    SBA_STATE_DATASET,
    build_composite_index,
    county_name_lookup,
    detect_state_column,
    leave_one_metric_out_sensitivity,
    load_cbp_county_file,
    load_cbp_state_file,
    load_cdfi_certification_workbook,
    load_county_geojson,
    load_sba_state_workbook,
    merge_cdfi_with_cbp,
    metric_quality_report,
    missing_data_stress_test,
    normalization_sensitivity_benchmark,
    numeric_metric_columns,
    prepare_state_metric,
    summarize_cbp_county_totals,
    summarize_cbp_state_totals,
    summarize_cdfi_by_state,
    summarize_county_industry_concentration,
    weight_sensitivity_benchmark,
)

REPOSITORY_URL = "https://github.com/sakera023/us-small-business-capital-access-atlas"
LIVE_URL = "https://capital-access-atlas-sakera.streamlit.app/"
PYPI_URL = "https://pypi.org/project/us-small-business-capital-access-atlas/"

CBP_METRICS = [
    "establishments",
    "employment",
    "annual_payroll_thousands",
    "q1_payroll_thousands",
]

NORMALIZATION_LABELS = {
    "Percentile ranks": "percentile",
    "Standard z-score": "zscore",
    "Winsorized z-score": "winsorized_zscore",
    "Robust median/MAD z-score": "robust_zscore",
}

st.set_page_config(
    page_title="U.S. Small Business Capital Access Atlas",
    page_icon="🗺️",
    layout="wide",
)

st.title("U.S. Small Business Capital Access Atlas")
st.caption(
    "A public, reproducible geospatial research platform for examining small-business "
    "activity, regional opportunity, and capital-support context across the United States."
)
st.info(
    "Research and educational use only. The Atlas analyzes aggregate geographic data "
    "and does not make applicant-level credit, lending, investment, or eligibility decisions."
)

link_repo, link_live, link_pypi, link_sources = st.columns(4)
with link_repo:
    st.link_button("GitHub Repository", REPOSITORY_URL, use_container_width=True)
with link_live:
    st.link_button("Public Atlas", LIVE_URL, use_container_width=True)
with link_pypi:
    st.link_button("Python Package", PYPI_URL, use_container_width=True)
with link_sources:
    st.link_button(
        "Official Census CBP",
        CENSUS_CBP_2023["landing_page"],
        use_container_width=True,
    )


@st.cache_data(ttl=3600, show_spinner=False)
def load_official_sba_data():
    return load_sba_state_workbook()


@st.cache_data(ttl=86400, show_spinner=False)
def load_official_cbp_state_data():
    raw = load_cbp_state_file()
    return summarize_cbp_state_totals(raw)


@st.cache_data(ttl=86400, show_spinner=False)
def load_official_cbp_county_data():
    raw = load_cbp_county_file()
    totals = summarize_cbp_county_totals(raw)
    concentration = summarize_county_industry_concentration(raw)
    return totals, concentration


@st.cache_data(ttl=86400, show_spinner=False)
def load_official_cdfi_data():
    metadata, raw = load_cdfi_certification_workbook()
    return metadata, summarize_cdfi_by_state(raw)


@st.cache_data(ttl=86400, show_spinner=False)
def load_official_county_boundaries(state_fips: str):
    return load_county_geojson(state_fips)


def available_state_sheets(sheets: dict[str, pd.DataFrame]) -> dict[str, str]:
    detected: dict[str, str] = {}
    for sheet_name, frame in sheets.items():
        state_column = detect_state_column(frame)
        if state_column:
            detected[sheet_name] = state_column
    return detected


def numeric_cbp_metrics(frame: pd.DataFrame) -> list[str]:
    return [column for column in CBP_METRICS if column in frame.columns]


with st.sidebar:
    st.header("Official public data")
    st.caption("Load authoritative datasets only when you need them.")

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
                st.session_state["cbp_state"] = load_official_cbp_state_data()
        except Exception as exc:
            st.error(
                "Unable to load the official Census CBP state file right now. "
                f"Source error: {exc}"
            )

    if st.button("Load Census CBP county data", use_container_width=True):
        try:
            with st.spinner(
                "Loading and summarizing the Census 2023 CBP county file..."
            ):
                (
                    st.session_state["cbp_county"],
                    st.session_state["cbp_county_concentration"],
                ) = load_official_cbp_county_data()
        except Exception as exc:
            st.error(
                "Unable to load the official Census CBP county file right now. "
                f"Source error: {exc}"
            )

    if st.button("Load Certified CDFI list", use_container_width=True):
        try:
            with st.spinner("Loading the current official Certified CDFI list..."):
                (
                    st.session_state["cdfi_metadata"],
                    st.session_state["cdfi_state"],
                ) = load_official_cdfi_data()
        except Exception as exc:
            st.error(
                "Unable to load the current Certified CDFI list right now. "
                f"Source error: {exc}"
            )

    st.divider()
    st.caption("Loaded this session")
    st.write("SBA:", "✅" if "sba_workbook" in st.session_state else "—")
    st.write("Census state:", "✅" if "cbp_state" in st.session_state else "—")
    st.write("Census county:", "✅" if "cbp_county" in st.session_state else "—")
    st.write("Certified CDFIs:", "✅" if "cdfi_state" in st.session_state else "—")


tabs = st.tabs(
    [
        "Atlas Overview",
        "SBA National Map",
        "Census State",
        "County Drill-down",
        "CDFI Capital Support",
        "State Comparison",
        "Index Lab",
        "Robustness & Quality",
        "Sources & Methodology",
    ]
)

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Official source families", "3")
    c2.metric("Geographic levels", "State + County")
    c3.metric("Public deployment", "Live")
    c4.metric("Index status", "Research prototype")

    st.subheader("Research purpose")
    st.write(
        "The Atlas studies place-based differences in entrepreneurship, business scale, "
        "employment, payroll, industry structure, and capital-support infrastructure "
        "using transparent public data."
    )

    st.subheader("Current capabilities")
    st.markdown(
        "- SBA State Small Business Statistics 2025 integration\n"
        "- Census County Business Patterns 2023 state and county integration\n"
        "- Census TIGERweb 2023 county boundary integration\n"
        "- Current Certified CDFI state geography\n"
        "- State and county choropleths, rankings, and drill-down\n"
        "- County industry-concentration diagnostics\n"
        "- Capital Access Opportunity Index Lab\n"
        "- Alternative normalization, weight, and missing-data sensitivity tests\n"
        "- Downloadable research tables and reproducible Python utilities"
    )

    st.subheader("Research boundary")
    st.write(
        "The Atlas summarizes aggregate geographic evidence. A map, CDFI organization "
        "count, or composite index does not establish causation, discrimination, policy "
        "effectiveness, service-area coverage, or individual creditworthiness."
    )

with tabs[1]:
    st.subheader("SBA State Small-Business Atlas")

    if "sba_workbook" not in st.session_state:
        st.warning("Load the official SBA state dataset from the sidebar.")
    else:
        metadata, sheets = st.session_state["sba_workbook"]
        state_sheets = available_state_sheets(sheets)

        if not state_sheets:
            st.error("No state-level worksheet could be detected in the SBA workbook.")
        else:
            sheet_name = st.selectbox(
                "SBA worksheet",
                list(state_sheets),
                key="sba_map_sheet",
            )
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)

            if not metrics:
                st.warning("No numeric state measures were detected in this worksheet.")
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
                    "Download SBA map data",
                    mapped.to_csv(index=False).encode("utf-8"),
                    file_name="sba_state_atlas_metric.csv",
                    mime="text/csv",
                )

                st.caption(
                    f"Source: {metadata['package_title']}. If multiple source rows map "
                    "to one state, values are averaged for visualization."
                )

with tabs[2]:
    st.subheader("U.S. Census County Business Patterns — State View")

    if "cbp_state" not in st.session_state:
        st.warning("Load Census CBP state data from the sidebar.")
    else:
        cbp_state = st.session_state["cbp_state"].copy()
        cbp_metrics = numeric_cbp_metrics(cbp_state)
        metric = st.selectbox("CBP state measure", cbp_metrics, key="cbp_state_metric")

        fig = px.choropleth(
            cbp_state,
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
            cbp_state.sort_values(metric, ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "Download Census CBP state totals",
            cbp_state.to_csv(index=False).encode("utf-8"),
            file_name="census_cbp_2023_state_totals.csv",
            mime="text/csv",
        )
        st.caption(
            "CBP covers establishments with paid employees. Payroll fields retain "
            "the source file's published units."
        )

with tabs[3]:
    st.subheader("County Business Structure Drill-down")

    if "cbp_county" not in st.session_state:
        st.warning(
            "Load Census CBP county data from the sidebar. The official county ZIP is "
            "larger than the state file, so the first load can take longer."
        )
    else:
        county = st.session_state["cbp_county"].copy()
        concentration = st.session_state["cbp_county_concentration"].copy()

        state_options = (
            county[["state", "state_name", "state_fips"]]
            .drop_duplicates()
            .sort_values("state_name")
        )
        selected_state_name = st.selectbox(
            "State",
            state_options["state_name"].tolist(),
            key="county_state",
        )
        state_row = state_options.loc[
            state_options["state_name"] == selected_state_name
        ].iloc[0]
        selected_state = state_row["state"]
        state_fips = state_row["state_fips"]

        county_state = county[county["state"] == selected_state].copy()
        concentration_state = concentration[
            concentration["state"] == selected_state
        ].copy()
        county_state = county_state.merge(
            concentration_state[
                ["geoid", "industry_hhi", "sector_count", "top_sector_share"]
            ],
            on="geoid",
            how="left",
        )

        try:
            geojson = load_official_county_boundaries(state_fips)
            names = county_name_lookup(geojson)
            county_state["county_name"] = county_state["geoid"].map(names)

            county_metric_options = {
                "Establishments": "establishments",
                "Employment": "employment",
                "Annual payroll (thousands)": "annual_payroll_thousands",
                "First-quarter payroll (thousands)": "q1_payroll_thousands",
                "Industry concentration (HHI)": "industry_hhi",
                "Top-sector share": "top_sector_share",
            }
            available_options = {
                label: column
                for label, column in county_metric_options.items()
                if column in county_state.columns
                and county_state[column].notna().any()
            }

            label = st.selectbox(
                "County measure",
                list(available_options),
                key="county_metric",
            )
            metric = available_options[label]

            fig = px.choropleth(
                county_state,
                geojson=geojson,
                locations="geoid",
                featureidkey="properties.GEOID",
                color=metric,
                hover_name="county_name",
                hover_data={
                    "geoid": True,
                    "establishments": ":,.0f",
                    "employment": ":,.0f",
                    "industry_hhi": ":,.0f",
                    "top_sector_share": ":.1%",
                },
                title=f"{selected_state_name} Counties — {label}",
            )
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r": 0, "t": 55, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                county_state.sort_values(metric, ascending=False),
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "Download selected-state county table",
                county_state.to_csv(index=False).encode("utf-8"),
                file_name=f"cbp_2023_{selected_state.lower()}_counties.csv",
                mime="text/csv",
            )
        except Exception as exc:
            st.error(f"County boundaries could not be loaded right now: {exc}")

        st.caption(
            "County boundaries use the Census TIGERweb 2023 generalized county layer. "
            "Industry HHI is calculated from high-level CBP sector establishment shares "
            "on a 0–10,000 scale."
        )

with tabs[4]:
    st.subheader("Certified CDFI Capital-Support Geography")

    if "cdfi_state" not in st.session_state:
        st.warning("Load the current Certified CDFI list from the sidebar.")
    else:
        cdfi_state = st.session_state["cdfi_state"].copy()
        metadata = st.session_state["cdfi_metadata"]

        total_cdfis = int(cdfi_state["certified_cdfis"].sum())
        states_covered = int(cdfi_state["state"].nunique())
        c1, c2 = st.columns(2)
        c1.metric("Certified organizations represented", f"{total_cdfis:,}")
        c2.metric("States / DC represented", states_covered)

        map_frame = cdfi_state
        cdfi_metric_options = {
            "Certified CDFI organizations": "certified_cdfis",
        }

        if "cbp_state" in st.session_state:
            map_frame = merge_cdfi_with_cbp(
                cdfi_state,
                st.session_state["cbp_state"],
            )
            cdfi_metric_options[
                "Certified CDFIs per 10,000 CBP establishments"
            ] = "cdfis_per_10k_establishments"

        metric_label = st.selectbox(
            "Capital-support measure",
            list(cdfi_metric_options),
            key="cdfi_metric",
        )
        metric = cdfi_metric_options[metric_label]

        fig = px.choropleth(
            map_frame,
            locations="state",
            locationmode="USA-states",
            color=metric,
            scope="usa",
            hover_name="state_name",
            title=f"Certified CDFI Geography — {metric_label}",
        )
        fig.update_layout(margin={"r": 0, "t": 55, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            map_frame.sort_values(metric, ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "Download CDFI state summary",
            map_frame.to_csv(index=False).encode("utf-8"),
            file_name="certified_cdfi_state_summary.csv",
            mime="text/csv",
        )

        st.warning(
            "Certified CDFI counts describe organization locations in the official "
            "certification list. They are not a direct measure of lending volume, "
            "branch presence, target-market coverage, or service-area access."
        )
        st.caption(
            f"Source: {metadata['publisher']} — {metadata['label']}. "
            "The workbook link is discovered from the official certification page "
            "with a documented fallback."
        )

with tabs[5]:
    st.subheader("State Comparison")

    source = st.radio(
        "Comparison source",
        ["SBA", "Census CBP", "Certified CDFIs"],
        horizontal=True,
        key="comparison_source_choice",
    )
    comparison_source = pd.DataFrame()
    value_column = ""
    label = ""

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
                    selected_metric = st.selectbox(
                        "Measure",
                        metrics,
                        key="comparison_sba_metric",
                    )
                    comparison_source = prepare_state_metric(
                        frame,
                        selected_metric,
                        state_column,
                    )
                    value_column = "value"
                    label = selected_metric

    elif source == "Census CBP":
        if "cbp_state" not in st.session_state:
            st.info("Load Census CBP state data from the sidebar.")
        else:
            comparison_source = st.session_state["cbp_state"].copy()
            options = numeric_cbp_metrics(comparison_source)
            selected_metric = st.selectbox(
                "Measure",
                options,
                key="comparison_cbp_metric",
            )
            value_column = selected_metric
            label = selected_metric.replace("_", " ").title()

    else:
        if "cdfi_state" not in st.session_state:
            st.info("Load the Certified CDFI list from the sidebar.")
        else:
            comparison_source = st.session_state["cdfi_state"].copy()
            value_column = "certified_cdfis"
            label = "Certified CDFI organizations"

    if not comparison_source.empty and value_column:
        state_names = comparison_source["state_name"].dropna().tolist()
        selected_states = st.multiselect(
            "Select states",
            state_names,
            default=state_names[: min(5, len(state_names))],
            key="comparison_states",
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

with tabs[6]:
    st.subheader("Capital Access Opportunity Index Lab")
    st.write(
        "Build an exploratory composite from official SBA state measures and test how "
        "the ranking changes under alternative normalization, weighting, and missing-data "
        "assumptions."
    )

    if "sba_workbook" not in st.session_state:
        st.warning("Load SBA data from the sidebar to use the Index Lab.")
    else:
        _, sheets = st.session_state["sba_workbook"]
        state_sheets = available_state_sheets(sheets)

        if state_sheets:
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
                key="index_metrics",
            )

            normalization_label = st.selectbox(
                "Normalization",
                list(NORMALIZATION_LABELS),
                key="index_normalization",
            )
            normalization = NORMALIZATION_LABELS[normalization_label]

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
                        normalization=normalization,
                    )

                    fig = px.choropleth(
                        index_frame,
                        locations="state",
                        locationmode="USA-states",
                        color="capital_access_index",
                        scope="usa",
                        title=(
                            "Exploratory Capital Access Opportunity Index — "
                            f"{normalization_label}"
                        ),
                        labels={"capital_access_index": "Index score"},
                    )
                    fig.update_layout(margin={"r": 0, "t": 55, "l": 0, "b": 0})
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(index_frame, use_container_width=True, hide_index=True)

                    if len(selected_metrics) >= 2:
                        st.subheader("Robustness diagnostics")

                        omission = leave_one_metric_out_sensitivity(
                            frame,
                            state_column=state_column,
                            metric_weights=weights,
                            inverse_metrics=inverse,
                            normalization=normalization,
                        )
                        st.markdown("**Leave one metric out**")
                        st.dataframe(omission, use_container_width=True, hide_index=True)

                        normalization_test = normalization_sensitivity_benchmark(
                            frame,
                            state_column=state_column,
                            metric_weights=weights,
                            inverse_metrics=inverse,
                            methods=NORMALIZATION_METHODS,
                        )
                        st.markdown("**Alternative normalization methods**")
                        st.dataframe(
                            normalization_test,
                            use_container_width=True,
                            hide_index=True,
                        )

                        weight_test = weight_sensitivity_benchmark(
                            frame,
                            state_column=state_column,
                            metric_weights=weights,
                            inverse_metrics=inverse,
                            normalization=normalization,
                        )
                        st.markdown("**One-component weight emphasis**")
                        st.dataframe(weight_test, use_container_width=True, hide_index=True)

                        missing_test = missing_data_stress_test(
                            frame,
                            state_column=state_column,
                            metric_weights=weights,
                            inverse_metrics=inverse,
                            normalization=normalization,
                            missing_rates=(0.05, 0.10, 0.20),
                            repeats=10,
                            seed=42,
                        )
                        st.markdown("**Missing-data stress test**")
                        st.dataframe(
                            missing_test,
                            use_container_width=True,
                            hide_index=True,
                        )

                    st.warning(
                        "The Index Lab remains exploratory. Rankings can change with "
                        "indicator choice, source year, normalization, weights, and missingness."
                    )

with tabs[7]:
    st.subheader("Data Quality and Validation")

    if "sba_workbook" in st.session_state:
        st.markdown("### SBA worksheet quality")
        _, sheets = st.session_state["sba_workbook"]
        state_sheets = available_state_sheets(sheets)
        if state_sheets:
            sheet_name = st.selectbox(
                "SBA worksheet",
                list(state_sheets),
                key="quality_sba_sheet",
            )
            frame = sheets[sheet_name]
            state_column = state_sheets[sheet_name]
            metrics = numeric_metric_columns(frame, state_column)
            selected = st.multiselect(
                "SBA metrics",
                metrics,
                default=metrics[: min(6, len(metrics))],
                key="quality_sba_metrics",
            )
            if selected:
                quality = metric_quality_report(frame, selected)
                st.dataframe(quality, use_container_width=True, hide_index=True)

    if "cbp_state" in st.session_state:
        st.markdown("### Census CBP state coverage")
        cbp_state = st.session_state["cbp_state"]
        st.metric("States / DC represented", int(cbp_state["state"].nunique()))
        st.dataframe(
            metric_quality_report(
                cbp_state,
                numeric_cbp_metrics(cbp_state),
            ),
            use_container_width=True,
            hide_index=True,
        )

    if "cbp_county" in st.session_state:
        st.markdown("### Census CBP county coverage")
        cbp_county = st.session_state["cbp_county"]
        c1, c2 = st.columns(2)
        c1.metric("County/county-equivalent rows", f"{len(cbp_county):,}")
        c2.metric("Unique states / DC", int(cbp_county["state"].nunique()))
        st.dataframe(
            metric_quality_report(
                cbp_county,
                numeric_cbp_metrics(cbp_county),
            ),
            use_container_width=True,
            hide_index=True,
        )

    if (
        "sba_workbook" not in st.session_state
        and "cbp_state" not in st.session_state
        and "cbp_county" not in st.session_state
    ):
        st.info("Load a public dataset from the sidebar to inspect data quality.")

with tabs[8]:
    st.subheader("Public Data Provenance")
    st.markdown(
        f"**SBA:** {SBA_STATE_DATASET['label']}  \n"
        f"Publisher: {SBA_STATE_DATASET['publisher']}  \n"
        f"Source: {SBA_STATE_DATASET['landing_page']}  \n\n"
        f"**Census CBP:** {CENSUS_CBP_2023['label']}  \n"
        f"Publisher: {CENSUS_CBP_2023['publisher']}  \n"
        f"Source: {CENSUS_CBP_2023['landing_page']}  \n\n"
        f"**County boundaries:** {CENSUS_TIGER_COUNTY_2023['label']}  \n"
        f"Publisher: {CENSUS_TIGER_COUNTY_2023['publisher']}  \n"
        f"Source: {CENSUS_TIGER_COUNTY_2023['layer_url']}  \n\n"
        f"**Certified CDFIs:** {CDFI_CERTIFICATION['label']}  \n"
        f"Publisher: {CDFI_CERTIFICATION['publisher']}  \n"
        f"Source: {CDFI_CERTIFICATION['landing_page']}"
    )

    st.subheader("Methodological principles")
    st.markdown(
        "1. **Public-data provenance:** every integrated dataset has a named publisher.\n"
        "2. **Geographic transparency:** state/county identifiers and vintage are retained.\n"
        "3. **Component visibility:** composite scores remain inspectable.\n"
        "4. **Robustness testing:** normalization, weights, omission, and missingness matter.\n"
        "5. **No applicant underwriting:** this is a place-based research platform.\n"
        "6. **No causal overclaiming:** geographic association is not proof of causation.\n"
        "7. **External validation remains external:** independent review and outside use "
        "are documented only when they genuinely occur."
    )

    st.caption(
        "See the GitHub documentation for data governance, validation, case studies, "
        "citation guidance, external-review materials, and adoption standards."
    )
