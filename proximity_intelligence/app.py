"""
BEYOND-SOS
Person 2 - Proximity & PAC Intelligence
Clean Review Prototype
"""

import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st


# ============================================================
# IMPORT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from simulation.radar_simulator import RadarSimulator
from features.proximity_features import ProximityFeatureExtractor
from ego_motion.ego_motion import EgoMotionCompensator
from behavior.behavior_analyzer import BehaviourAnalyzer
from pac.pac_analyzer import PACAnalyzer
from pac.physiology_simulator import PhysiologySimulator


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="BEYOND-SOS | Proximity Simulator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CLEAN LIGHT UI
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #f7f8fc;
}

[data-testid="stHeader"] {
    background: #f7f8fc;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e7e9f2;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label {
    color: #182033 !important;
}


/* HERO */

.hero {
    background:
        linear-gradient(
            110deg,
            #ffffff 0%,
            #f4f1ff 55%,
            #eef8ff 100%
        );

    border: 1px solid #e5e7ef;
    border-radius: 22px;

    padding: 28px 32px;

    margin-bottom: 24px;

    box-shadow:
        0 8px 30px rgba(40,45,80,0.05);
}

.hero-kicker {
    color: #6d5bd0;

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 1.5px;
}

.hero-title {
    color: #172033;

    font-size: 36px;
    font-weight: 850;

    margin-top: 7px;
}

.hero-subtitle {
    color: #667085;

    font-size: 15px;

    line-height: 1.6;

    max-width: 780px;

    margin-top: 6px;
}

.badge {
    display: inline-block;

    margin-top: 15px;

    padding: 6px 11px;

    border-radius: 999px;

    background: #edf8f2;

    color: #18794e;

    font-size: 11px;

    font-weight: 800;
}


/* SECTION */

.section-title {
    color: #172033;

    font-size: 20px;

    font-weight: 850;

    margin-top: 24px;

    margin-bottom: 12px;
}


/* SCENE */

.scene {
    background: #ffffff;

    border: 1px solid #e7e9f2;

    border-radius: 20px;

    padding: 26px;

    box-shadow:
        0 5px 20px rgba(30,40,70,0.04);
}

.scene-name {
    text-align: center;

    color: #6d5bd0;

    font-size: 12px;

    font-weight: 850;

    letter-spacing: 1.2px;
}

.scene-row {
    display: flex;

    align-items: center;

    justify-content: center;

    gap: 24px;

    margin: 34px 0 25px;
}

.person-circle {
    width: 72px;
    height: 72px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 29px;
}

.wearer {
    background: #eeeafd;

    border: 2px solid #8b7de0;
}

.target {
    background: #e9f7fb;

    border: 2px solid #57a9c7;
}

.person-label {
    text-align: center;

    color: #667085;

    font-size: 11px;

    font-weight: 800;

    margin-top: 7px;
}

.distance-line {
    width: 250px;

    height: 2px;

    background: #d2d7e0;

    position: relative;
}

.distance {
    position: absolute;

    width: 100%;

    text-align: center;

    top: -30px;

    color: #172033;

    font-size: 16px;

    font-weight: 850;
}

.motion {
    position: absolute;

    width: 100%;

    text-align: center;

    top: 9px;

    color: #667085;

    font-size: 13px;

    font-weight: 650;
}

.scene-summary {
    text-align: center;

    color: #344054;

    font-size: 15px;

    font-weight: 700;
}


/* RESULT CARDS */

.result-card {
    background: #ffffff;

    border: 1px solid #e7e9f2;

    border-radius: 19px;

    padding: 24px;

    min-height: 205px;

    box-shadow:
        0 5px 20px rgba(30,40,70,0.04);
}

.result-label {
    color: #667085;

    font-size: 11px;

    font-weight: 850;

    letter-spacing: 1px;
}

.result-value {
    color: #172033;

    font-size: 42px;

    font-weight: 850;

    margin-top: 8px;
}

.result-max {
    color: #98a2b3;

    font-size: 17px;
}

.result-status {
    color: #6d5bd0;

    font-size: 14px;

    font-weight: 850;

    margin-top: 2px;
}

.result-description {
    color: #667085;

    font-size: 13px;

    line-height: 1.6;

    margin-top: 15px;
}


/* EXPLANATION */

.explanation {
    background: #ffffff;

    border: 1px solid #e7e9f2;

    border-left: 5px solid #7566d5;

    border-radius: 16px;

    padding: 19px 21px;

    color: #344054;

    font-size: 14px;

    line-height: 1.7;
}


/* METRICS */

div[data-testid="stMetric"] {
    background: #ffffff;

    border: 1px solid #e7e9f2;

    border-radius: 16px;

    padding: 15px;

    box-shadow:
        0 4px 16px rgba(30,40,70,0.035);
}


/* BUTTON */

.stButton > button {
    background: #6d5bd0;

    color: white;

    border: none;

    border-radius: 12px;

    min-height: 44px;

    font-weight: 750;
}

.stButton > button:hover {
    background: #5c4bc2;

    color: white;
}


/* DISCLAIMER */

.disclaimer {
    margin-top: 22px;

    padding: 14px 17px;

    background: #fffaf0;

    border: 1px solid #f1dfb8;

    border-radius: 14px;

    color: #725b2b;

    font-size: 12px;

    line-height: 1.6;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAMES
# ============================================================

DISPLAY_NAMES = {
    "normal_passing": "Normal Passing",
    "rapid_approach": "Rapid Approach",
    "sustained_proximity": "Sustained Proximity",
    "standing_nearby": "Standing Nearby",
    "retreat_reapproach": "Retreat & Re-approach",
    "ego_motion_control": "Ego-motion Control",
}


SCENARIO_DESCRIPTIONS = {

    "normal_passing":
        "A person passes the wearer and then moves away.",

    "rapid_approach":
        "A person moves quickly toward the wearer.",

    "sustained_proximity":
        "A person remains close for an extended period.",

    "standing_nearby":
        "A person stays nearby with very little movement.",

    "retreat_reapproach":
        "A person moves away and then approaches again.",

    "ego_motion_control":
        "The wearer walks toward a stationary person — a false-alarm control.",
}


# ============================================================
# BACKEND
# ============================================================

simulator = RadarSimulator(
    sample_interval=1.0
)

extractor = ProximityFeatureExtractor(
    nearby_threshold=2.5,
    motion_threshold=0.15,
)

compensator = EgoMotionCompensator(
    motion_threshold=0.15
)

behaviour_analyzer = BehaviourAnalyzer(
    nearby_threshold=2.5,
    persistence_threshold=5.0,
    rapid_approach_threshold=0.6,
)

pac_analyzer = PACAnalyzer(
    max_response_lag=5.0,
    minimum_approach_speed=0.30,
    minimum_physiological_residual=0.25,
)

physiology_simulator = PhysiologySimulator()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🛡️ Simulation"
)

st.sidebar.caption(
    "Choose a situation and see how "
    "BEYOND-SOS interprets it."
)


scenario_keys = (
    simulator.available_scenarios()
)


selected_scenario = (
    st.sidebar.selectbox(
        "Situation",
        scenario_keys,

        format_func=lambda item:
            DISPLAY_NAMES.get(
                item,
                item.replace(
                    "_",
                    " "
                ).title(),
            ),
    )
)


st.sidebar.info(
    SCENARIO_DESCRIPTIONS[
        selected_scenario
    ]
)


presets = (
    simulator.available_presets(
        selected_scenario
    )
)


selected_preset = (
    st.sidebar.selectbox(
        "Preset",
        presets,

        format_func=lambda item:
            item.replace(
                "_",
                " "
            ).title(),
    )
)


run_button = (
    st.sidebar.button(
        "▶ Run simulation",
        use_container_width=True,
    )
)


st.sidebar.markdown("---")

st.sidebar.caption(
    "Current stage: simulated sensor streams. "
    "Real radar, IMU and physiological sensors "
    "will replace these inputs during hardware integration."
)


# ============================================================
# RUN PIPELINE
# ============================================================

if (
    run_button
    or "pipeline_result"
    not in st.session_state

    or st.session_state.get(
        "scenario"
    ) != selected_scenario

    or st.session_state.get(
        "preset"
    ) != selected_preset
):

    readings = simulator.generate(
        scenario_name=selected_scenario,
        preset_name=selected_preset,
    )


    features = extractor.extract(
        readings
    )


    ego_results = (
        compensator.process(
            readings,
            features,
        )
    )


    behaviour_result = (
        behaviour_analyzer.analyze(
            selected_scenario,
            features,
            ego_results,
        )
    )


    duration = (
        int(
            readings[-1].timestamp
        )
        + 5
    )


    if (
        selected_scenario
        == "rapid_approach"
    ):

        physiological_samples = (
            physiology_simulator
            .approach_response(
                duration=duration,
                response_start=2,
                peak_residual=0.85,
            )
        )

    else:

        physiological_samples = (
            physiology_simulator
            .neutral_response(
                duration=duration,
            )
        )


    pac_result = (
        pac_analyzer.analyze(
            ego_results,
            physiological_samples,
        )
    )


    st.session_state[
        "pipeline_result"
    ] = True

    st.session_state[
        "scenario"
    ] = selected_scenario

    st.session_state[
        "preset"
    ] = selected_preset

    st.session_state[
        "readings"
    ] = readings

    st.session_state[
        "features"
    ] = features

    st.session_state[
        "ego_results"
    ] = ego_results

    st.session_state[
        "behaviour_result"
    ] = behaviour_result

    st.session_state[
        "physiology_samples"
    ] = physiological_samples

    st.session_state[
        "pac_result"
    ] = pac_result


# ============================================================
# LOAD RESULTS
# ============================================================

readings = (
    st.session_state[
        "readings"
    ]
)

features = (
    st.session_state[
        "features"
    ]
)

ego_results = (
    st.session_state[
        "ego_results"
    ]
)

behaviour_result = (
    st.session_state[
        "behaviour_result"
    ]
)

physiology_samples = (
    st.session_state[
        "physiology_samples"
    ]
)

pac_result = (
    st.session_state[
        "pac_result"
    ]
)

active_scenario = (
    st.session_state[
        "scenario"
    ]
)

display_scenario = (
    DISPLAY_NAMES[
        active_scenario
    ]
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero"><div class="hero-kicker">BEYOND-SOS · PERSON 2 PROTOTYPE</div><div class="hero-title">Proximity Intelligence Simulator</div><div class="hero-subtitle">See how the system interprets movement around the wearer — and how it avoids treating every close person or every radar change as danger.</div><div class="badge">● SIMULATED SENSOR STREAMS</div></div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIMPLE SCENE
# ============================================================

last_ego = ego_results[-1]

final_distance = (
    readings[-1].distance
)


if (
    behaviour_result
    .repeated_approach
):

    motion_text = (
        "↔ moves away, then returns"
    )

    summary = (
        "Repeated approach pattern detected"
    )


elif (
    behaviour_result
    .persistent_nearby
):

    motion_text = (
        "● remains nearby"
    )

    summary = (
        "Person remains close for an extended time"
    )


elif (
    behaviour_result
    .maximum_corrected_approach_speed
    >= 0.6
):

    motion_text = (
        "← approaching wearer"
    )

    summary = (
        "Person is approaching the wearer"
    )


elif (
    last_ego.corrected_motion
    == "TARGET STATIONARY"
):

    motion_text = (
        "● stationary"
    )

    summary = (
        "Person is stationary after "
        "correcting for wearer movement"
    )


elif (
    "RETREAT"
    in last_ego.corrected_motion
):

    motion_text = (
        "→ moving away"
    )

    summary = (
        "Person is moving away"
    )


else:

    motion_text = "—"

    summary = (
        "No strong approach behaviour detected"
    )


st.markdown(
    '<div class="section-title">'
    '1. What is happening?'
    '</div>',
    unsafe_allow_html=True,
)


scene_html = (
    '<div class="scene">'
    f'<div class="scene-name">{display_scenario.upper()}</div>'
    '<div class="scene-row">'

    '<div>'
    '<div class="person-circle target">●</div>'
    '<div class="person-label">OTHER PERSON</div>'
    '</div>'

    '<div class="distance-line">'
    f'<div class="distance">{final_distance:.2f} m</div>'
    f'<div class="motion">{motion_text}</div>'
    '</div>'

    '<div>'
    '<div class="person-circle wearer">🛡️</div>'
    '<div class="person-label">WEARER</div>'
    '</div>'

    '</div>'

    f'<div class="scene-summary">{summary}</div>'

    '</div>'
)

st.markdown(
    scene_html,
    unsafe_allow_html=True,
)


# ============================================================
# SIMPLE OBSERVATIONS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '2. What did the system notice?'
    '</div>',
    unsafe_allow_html=True,
)


m1, m2, m3, m4 = (
    st.columns(4)
)


m1.metric(
    "Closest distance",
    (
        f"{behaviour_result.minimum_distance:.2f} m"
    ),
)


m2.metric(
    "Approach speed",
    (
        f"{behaviour_result.maximum_corrected_approach_speed:.2f} m/s"
    ),
)


m3.metric(
    "Stayed nearby",
    (
        f"{behaviour_result.maximum_nearby_duration:.1f} s"
    ),
)


m4.metric(
    "Approach events",
    (
        behaviour_result.approach_count
    ),
)


# ============================================================
# MAIN RESULTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '3. What evidence did it produce?'
    '</div>',
    unsafe_allow_html=True,
)


reasons = []


if (
    behaviour_result
    .distance_evidence
    > 0
):

    reasons.append(
        "close distance"
    )


if (
    behaviour_result
    .approach_evidence
    > 0
):

    reasons.append(
        "approach motion"
    )


if (
    behaviour_result
    .persistence_evidence
    > 0
):

    reasons.append(
        "staying nearby"
    )


if (
    behaviour_result
    .reapproach_evidence
    > 0
):

    reasons.append(
        "repeated approach"
    )


if reasons:

    proximity_text = (
        "Evidence came from "
        + ", ".join(reasons)
        + "."
    )

else:

    proximity_text = (
        "No strong proximity behaviour "
        "contributed evidence."
    )


if pac_result.coupling_detected:

    pac_status = (
        "✓ Temporal link detected"
    )

    if (
        pac_result.response_lag
        is not None
    ):

        pac_description = (
            "A simulated body response "
            "followed the approach by "
            f"{pac_result.response_lag:.1f} seconds."
        )

    else:

        pac_description = (
            "A simulated body response "
            "was temporally associated "
            "with the approach."
        )

else:

    pac_status = (
        "No temporal link detected"
    )

    if (
        active_scenario
        == "ego_motion_control"
    ):

        pac_description = (
            "The apparent approach disappears "
            "after correcting for the wearer's "
            "own movement."
        )

    else:

        pac_description = (
            "No meaningful approach-linked "
            "body response was found."
        )


left, right = (
    st.columns(2)
)


with left:

    risk_html = (
        '<div class="result-card">'
        '<div class="result-label">PROXIMITY EVIDENCE</div>'

        f'<div class="result-value">'
        f'{behaviour_result.proximity_risk_score:.2f} '
        '<span class="result-max">/ 3.00</span>'
        '</div>'

        f'<div class="result-status">'
        f'{behaviour_result.evidence_level}'
        '</div>'

        f'<div class="result-description">'
        f'{proximity_text}'
        '<br><br>'
        'This is a proximity contribution, '
        'not a danger probability.'
        '</div>'

        '</div>'
    )

    st.markdown(
        risk_html,
        unsafe_allow_html=True,
    )


with right:

    pac_html = (
        '<div class="result-card">'
        '<div class="result-label">'
        'PROXIMITY + BODY RESPONSE'
        '</div>'

        f'<div class="result-value">'
        f'{pac_result.pac_evidence:.2f} '
        '<span class="result-max">/ 1.00</span>'
        '</div>'

        f'<div class="result-status">'
        f'{pac_status}'
        '</div>'

        f'<div class="result-description">'
        f'{pac_description}'
        '<br><br>'
        'This is temporal-coupling evidence, '
        'not a clinical measure.'
        '</div>'

        '</div>'
    )

    st.markdown(
        pac_html,
        unsafe_allow_html=True,
    )


# ============================================================
# PLAIN ENGLISH EXPLANATION
# ============================================================

if (
    active_scenario
    == "rapid_approach"
):

    explanation = (
        "The other person moves toward the wearer quickly. "
        "That approach remains even after correcting for the "
        "wearer's own movement. A simulated physiological "
        "response then occurs shortly afterward, so the "
        "prototype detects a temporal relationship."
    )


elif (
    active_scenario
    == "ego_motion_control"
):

    explanation = (
        "At first, the radar appears to show someone approaching "
        "because the distance is shrinking. But the wearer is "
        "actually walking forward. After correcting for the "
        "wearer's movement, the other person is interpreted as "
        "stationary. This demonstrates how the system can avoid "
        "a false approach alert."
    )


elif (
    active_scenario
    == "retreat_reapproach"
):

    explanation = (
        "The person approaches, moves away, and then approaches "
        "again. The system recognizes the sequence as repeated "
        "approach instead of judging only one distance reading."
    )


elif (
    active_scenario
    == "sustained_proximity"
):

    explanation = (
        "The person does not approach rapidly, but remains close "
        "for a longer period. The system therefore gives more "
        "importance to persistence than to approach speed."
    )


elif (
    active_scenario
    == "standing_nearby"
):

    explanation = (
        "The person stays at a fairly stable nearby distance. "
        "Small changes in distance are not automatically treated "
        "as repeated approaches. Closeness and duration are the "
        "main observations."
    )


else:

    explanation = (
        "The person comes closer briefly and then moves away. "
        "The system observes temporary closeness, but does not "
        "find persistent or repeated approach behaviour."
    )


st.markdown(
    '<div class="section-title">'
    '4. Why?'
    '</div>',
    unsafe_allow_html=True,
)


st.markdown(
    (
        '<div class="explanation">'
        + explanation
        + '</div>'
    ),
    unsafe_allow_html=True,
)


# ============================================================
# TECHNICAL DETAILS — HIDDEN
# ============================================================

with st.expander(
    "🔬 Technical details — open only if needed"
):

    st.caption(
        "Engineering information is hidden from "
        "the main demonstration to keep the simulator simple."
    )


    a, b, c, d = (
        st.columns(4)
    )


    a.metric(
        "Distance evidence",
        (
            f"{behaviour_result.distance_evidence:.2f} / 0.60"
        ),
    )


    b.metric(
        "Approach evidence",
        (
            f"{behaviour_result.approach_evidence:.2f} / 0.80"
        ),
    )


    c.metric(
        "Persistence evidence",
        (
            f"{behaviour_result.persistence_evidence:.2f} / 0.60"
        ),
    )


    d.metric(
        "Re-approach evidence",
        (
            f"{behaviour_result.reapproach_evidence:.2f} / 1.00"
        ),
    )


    tab1, tab2, tab3 = (
        st.tabs(
            [
                "Distance",
                "Ego-motion",
                "PAC timing",
            ]
        )
    )


    times = [
        reading.timestamp
        for reading in readings
    ]


    # --------------------------------------------------------
    # DISTANCE
    # --------------------------------------------------------

    with tab1:

        figure = go.Figure()


        figure.add_trace(
            go.Scatter(
                x=times,

                y=[
                    reading.distance
                    for reading
                    in readings
                ],

                mode="lines+markers",

                name="Distance",
            )
        )


        figure.add_hline(
            y=2.5,

            line_dash="dash",

            annotation_text=(
                "Nearby threshold"
            ),
        )


        figure.update_layout(
            height=320,

            template="plotly_white",

            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10,
            ),

            xaxis_title="Time (s)",

            yaxis_title="Distance (m)",
        )


        st.plotly_chart(
            figure,
            use_container_width=True,
        )


    # --------------------------------------------------------
    # EGO MOTION
    # --------------------------------------------------------

    with tab2:

        figure = go.Figure()


        figure.add_trace(
            go.Scatter(
                x=times,

                y=[
                    item.observed_closing_speed
                    for item
                    in ego_results
                ],

                mode="lines+markers",

                name="Radar sees",
            )
        )


        figure.add_trace(
            go.Scatter(
                x=times,

                y=[
                    item.corrected_target_speed
                    for item
                    in ego_results
                ],

                mode="lines+markers",

                name="After correction",
            )
        )


        figure.add_hline(
            y=0,
            line_dash="dash",
        )


        figure.update_layout(
            height=320,

            template="plotly_white",

            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10,
            ),

            xaxis_title="Time (s)",

            yaxis_title=(
                "Radial speed (m/s)"
            ),
        )


        st.plotly_chart(
            figure,
            use_container_width=True,
        )


        if (
            active_scenario
            == "ego_motion_control"
        ):

            st.success(
                "False-alarm control: raw radar "
                "shows closing motion, but after "
                "wearer-motion correction the "
                "target is approximately stationary."
            )


    # --------------------------------------------------------
    # PAC
    # --------------------------------------------------------

    with tab3:

        figure = go.Figure()


        figure.add_trace(
            go.Scatter(

                x=[
                    sample.timestamp
                    for sample
                    in physiological_samples
                ],

                y=[
                    sample.residual
                    for sample
                    in physiological_samples
                ],

                mode="lines+markers",

                name=(
                    "Simulated body response"
                ),
            )
        )


        if (
            pac_result.peak_approach_time
            is not None
        ):

            figure.add_vline(
                x=(
                    pac_result
                    .peak_approach_time
                ),

                line_dash="dash",

                annotation_text=(
                    "Approach"
                ),
            )


        if (
            pac_result
            .peak_physiological_time
            is not None
        ):

            figure.add_vline(
                x=(
                    pac_result
                    .peak_physiological_time
                ),

                line_dash="dot",

                annotation_text=(
                    "Body response"
                ),
            )


        figure.update_layout(
            height=320,

            template="plotly_white",

            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10,
            ),

            xaxis_title="Time (s)",

            yaxis_title=(
                "Simulated physiological residual"
            ),
        )


        st.plotly_chart(
            figure,
            use_container_width=True,
        )


        st.write(
            "PAC evidence: "
            f"**{pac_result.pac_evidence:.2f} / 1.00**"
        )


        if (
            pac_result.response_lag
            is not None
        ):

            st.write(
                "Response lag: "
                f"**{pac_result.response_lag:.1f} s**"
            )


# ============================================================
# DISCLOSURE
# ============================================================

st.markdown(
    """
<div class="disclaimer"><b>Research prototype.</b> This demonstration currently uses mathematically generated sensor streams. Physiological responses are synthetic placeholders for the future personal-state module. Thresholds and evidence weights are prototype engineering parameters and are not experimentally validated danger probabilities.</div>
""",
    unsafe_allow_html=True,
)