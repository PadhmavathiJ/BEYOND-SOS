"""
BEYOND-SOS
Person 2: Proximity & Behaviour Intelligence

Phase 4 - Behaviour Analysis

Interprets ego-motion-corrected proximity measurements to identify
safety-relevant interpersonal patterns.

This module does NOT classify a situation as "danger".
It produces a Proximity Risk Contribution from 0.00 to 3.00
for later multimodal fusion.

Current thresholds and weights are prototype engineering parameters.
They are not experimentally validated danger probabilities.
"""

from dataclasses import dataclass


@dataclass
class BehaviourResult:
    scenario: str
    minimum_distance: float
    maximum_corrected_approach_speed: float
    maximum_nearby_duration: float

    approach_count: int
    persistent_nearby: bool
    repeated_approach: bool

    distance_evidence: float
    approach_evidence: float
    persistence_evidence: float
    reapproach_evidence: float

    proximity_risk_score: float
    proximity_risk_max: float
    evidence_level: str


class BehaviourAnalyzer:

    def __init__(
        self,
        nearby_threshold=2.5,
        persistence_threshold=5.0,
        rapid_approach_threshold=0.6,
    ):
        # Prototype parameters only.
        # These will later be tuned using real sensor data.
        self.nearby_threshold = nearby_threshold
        self.persistence_threshold = persistence_threshold
        self.rapid_approach_threshold = rapid_approach_threshold

    # -----------------------------------------------------
    # COUNT DISTINCT APPROACH EVENTS
    # -----------------------------------------------------

    def count_approaches(self, ego_results):

        approach_count = 0
        previous_motion = None

        for result in ego_results:

            current_motion = result.corrected_motion

            if (
                current_motion == "TARGET APPROACHING"
                and previous_motion != "TARGET APPROACHING"
            ):
                approach_count += 1

            if current_motion != "INITIAL":
                previous_motion = current_motion

        return approach_count

    # -----------------------------------------------------
    # DETECT REPEATED APPROACH
    # -----------------------------------------------------

    def detect_repeated_approach(self, ego_results):
        """
        Detect:

        APPROACH -> RETREAT -> APPROACH
        """

        states = []

        for result in ego_results:

            if result.corrected_motion == "TARGET APPROACHING":
                state = "APPROACH"

            elif result.corrected_motion == "TARGET RETREATING":
                state = "RETREAT"

            else:
                continue

            if not states or states[-1] != state:
                states.append(state)

        pattern = [
            "APPROACH",
            "RETREAT",
            "APPROACH",
        ]

        for index in range(len(states) - 2):

            if states[index:index + 3] == pattern:
                return True

        return False

    # -----------------------------------------------------
    # DISTANCE COMPONENT
    # Maximum = 0.60
    # -----------------------------------------------------

    def calculate_distance_evidence(
        self,
        minimum_distance,
    ):

        if minimum_distance <= 1.0:
            return 0.60

        elif minimum_distance <= 1.5:
            return 0.50

        elif minimum_distance <= 2.0:
            return 0.35

        elif minimum_distance <= 2.5:
            return 0.20

        return 0.00

    # -----------------------------------------------------
    # APPROACH COMPONENT
    # Maximum = 0.80
    # -----------------------------------------------------

    def calculate_approach_evidence(
        self,
        maximum_approach_speed,
    ):

        if maximum_approach_speed >= 1.2:
            return 0.80

        elif maximum_approach_speed >= 0.8:
            return 0.65

        elif maximum_approach_speed >= 0.6:
            return 0.45

        elif maximum_approach_speed >= 0.3:
            return 0.20

        return 0.00

    # -----------------------------------------------------
    # PERSISTENCE COMPONENT
    # Maximum = 0.60
    # -----------------------------------------------------

    def calculate_persistence_evidence(
        self,
        nearby_duration,
    ):

        if nearby_duration >= 20.0:
            return 0.60

        elif nearby_duration >= 10.0:
            return 0.45

        elif nearby_duration >= 5.0:
            return 0.30

        return 0.00

    # -----------------------------------------------------
    # RE-APPROACH COMPONENT
    # Maximum = 1.00
    # -----------------------------------------------------

    def calculate_reapproach_evidence(
        self,
        approach_count,
        repeated_approach,
    ):

        if not repeated_approach:
            return 0.00

        if approach_count >= 3:
            return 1.00

        return 0.70

    # -----------------------------------------------------
    # PROTOTYPE EVIDENCE LEVEL
    # -----------------------------------------------------

    def classify_evidence_level(self, score):

        if score >= 2.25:
            return "VERY STRONG"

        elif score >= 1.50:
            return "STRONG"

        elif score >= 0.75:
            return "ELEVATED"

        return "LOW"

    # -----------------------------------------------------
    # MAIN ANALYSIS
    # -----------------------------------------------------

    def analyze(
        self,
        scenario_name,
        features,
        ego_results,
    ):

        if not features or not ego_results:
            raise ValueError(
                "Features and ego-motion results cannot be empty."
            )

        minimum_distance = min(
            feature.distance
            for feature in features
        )

        maximum_nearby_duration = max(
            feature.nearby_duration
            for feature in features
        )

        approach_speeds = [
            result.corrected_target_speed
            for result in ego_results
            if result.corrected_motion == "TARGET APPROACHING"
        ]

        maximum_corrected_approach_speed = (
            max(approach_speeds)
            if approach_speeds
            else 0.0
        )

        persistent_nearby = (
            maximum_nearby_duration
            >= self.persistence_threshold
        )

        approach_count = self.count_approaches(
            ego_results
        )

        repeated_approach = (
            self.detect_repeated_approach(
                ego_results
            )
        )

        # ---------------------------------------------
        # COMPONENT EVIDENCE
        # ---------------------------------------------

        distance_evidence = (
            self.calculate_distance_evidence(
                minimum_distance
            )
        )

        approach_evidence = (
            self.calculate_approach_evidence(
                maximum_corrected_approach_speed
            )
        )

        persistence_evidence = (
            self.calculate_persistence_evidence(
                maximum_nearby_duration
            )
        )

        reapproach_evidence = (
            self.calculate_reapproach_evidence(
                approach_count,
                repeated_approach,
            )
        )

        # Maximum possible score:
        #
        # Distance       = 0.60
        # Approach       = 0.80
        # Persistence    = 0.60
        # Re-approach    = 1.00
        # ----------------------
        # Total          = 3.00

        proximity_risk_score = (
            distance_evidence
            + approach_evidence
            + persistence_evidence
            + reapproach_evidence
        )

        proximity_risk_score = min(
            proximity_risk_score,
            3.0,
        )

        evidence_level = (
            self.classify_evidence_level(
                proximity_risk_score
            )
        )

        return BehaviourResult(
            scenario=scenario_name,

            minimum_distance=minimum_distance,

            maximum_corrected_approach_speed=(
                maximum_corrected_approach_speed
            ),

            maximum_nearby_duration=(
                maximum_nearby_duration
            ),

            approach_count=approach_count,

            persistent_nearby=persistent_nearby,

            repeated_approach=repeated_approach,

            distance_evidence=distance_evidence,

            approach_evidence=approach_evidence,

            persistence_evidence=(
                persistence_evidence
            ),

            reapproach_evidence=(
                reapproach_evidence
            ),

            proximity_risk_score=round(
                proximity_risk_score,
                2,
            ),

            proximity_risk_max=3.0,

            evidence_level=evidence_level,
        )


def display_behaviour(result):

    print("\n" + "=" * 72)

    print(
        "BEYOND-SOS | PERSON 2 | "
        "BEHAVIOUR INTELLIGENCE"
    )

    print("=" * 72)

    print(
        f"Scenario                  : "
        f"{result.scenario.replace('_', ' ').title()}"
    )

    print(
        f"Minimum Distance          : "
        f"{result.minimum_distance:.2f} m"
    )

    print(
        f"Max Corrected Approach    : "
        f"{result.maximum_corrected_approach_speed:.2f} m/s"
    )

    print(
        f"Maximum Nearby Duration   : "
        f"{result.maximum_nearby_duration:.1f} s"
    )

    print(
        f"Approach Events           : "
        f"{result.approach_count}"
    )

    print(
        f"Persistent Nearby         : "
        f"{'YES' if result.persistent_nearby else 'NO'}"
    )

    print(
        f"Repeated Approach         : "
        f"{'YES' if result.repeated_approach else 'NO'}"
    )

    print("-" * 72)

    print("PROXIMITY EVIDENCE COMPONENTS")

    print(
        f"Distance Evidence         : "
        f"{result.distance_evidence:.2f} / 0.60"
    )

    print(
        f"Approach Evidence         : "
        f"{result.approach_evidence:.2f} / 0.80"
    )

    print(
        f"Persistence Evidence      : "
        f"{result.persistence_evidence:.2f} / 0.60"
    )

    print(
        f"Re-approach Evidence      : "
        f"{result.reapproach_evidence:.2f} / 1.00"
    )

    print("-" * 72)

    print(
        f"PROXIMITY RISK CONTRIBUTION : "
        f"{result.proximity_risk_score:.2f} / "
        f"{result.proximity_risk_max:.2f}"
    )

    print(
        f"PROTOTYPE EVIDENCE LEVEL    : "
        f"{result.evidence_level}"
    )

    print("-" * 72)

    print(
        "NOTE: This is proximity evidence only, "
        "not a standalone danger probability."
    )

    print(
        "Final distress inference will combine "
        "proximity, physiology and context."
    )

    print("=" * 72)