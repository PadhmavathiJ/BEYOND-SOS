"""
BEYOND-SOS
Person 2: Proximity & PAC Intelligence

Phase 5 - Temporal Proximity-Autonomic Coupling Prototype

This module investigates whether an activity-conditioned
physiological deviation occurs in temporal association with
an interpersonal approach event.

PAC is prototype evidence, not a clinical measurement and
not a standalone danger probability.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class PhysiologicalSample:
    timestamp: float
    residual: float


@dataclass
class PACResult:
    peak_approach_time: float | None
    peak_approach_speed: float
    peak_physiological_time: float | None
    peak_physiological_residual: float
    response_lag: float | None
    temporal_alignment: float
    approach_strength: float
    physiological_strength: float
    pac_evidence: float
    coupling_detected: bool


class PACAnalyzer:

    def __init__(
        self,
        max_response_lag: float = 5.0,
        minimum_approach_speed: float = 0.30,
        minimum_physiological_residual: float = 0.25,
    ):
        self.max_response_lag = max_response_lag
        self.minimum_approach_speed = minimum_approach_speed
        self.minimum_physiological_residual = (
            minimum_physiological_residual
        )

    # -----------------------------------------------------
    # FIND STRONGEST APPROACH EVENT
    # -----------------------------------------------------

    def find_peak_approach(self, ego_results):

        valid = [
            item
            for item in ego_results
            if item.corrected_target_speed
            >= self.minimum_approach_speed
        ]

        if not valid:
            return None, 0.0

        strongest = max(
            valid,
            key=lambda item: item.corrected_target_speed,
        )

        return (
            strongest.timestamp,
            strongest.corrected_target_speed,
        )

    # -----------------------------------------------------
    # FIND PHYSIOLOGICAL RESPONSE AFTER APPROACH
    # -----------------------------------------------------

    def find_physiological_response(
        self,
        physiological_samples: List[PhysiologicalSample],
        approach_time,
    ):

        if approach_time is None:
            return None, 0.0

        window_end = (
            approach_time
            + self.max_response_lag
        )

        candidates = [
            sample
            for sample in physiological_samples
            if approach_time
            <= sample.timestamp
            <= window_end
        ]

        if not candidates:
            return None, 0.0

        strongest = max(
            candidates,
            key=lambda sample: sample.residual,
        )

        return (
            strongest.timestamp,
            strongest.residual,
        )

    # -----------------------------------------------------
    # TEMPORAL ALIGNMENT
    # -----------------------------------------------------

    def calculate_temporal_alignment(
        self,
        approach_time,
        physiological_time,
    ):

        if (
            approach_time is None
            or physiological_time is None
        ):
            return 0.0, None

        lag = (
            physiological_time
            - approach_time
        )

        if (
            lag < 0
            or lag > self.max_response_lag
        ):
            return 0.0, lag

        alignment = (
            1.0
            - lag / self.max_response_lag
        )

        return max(0.0, alignment), lag

    # -----------------------------------------------------
    # NORMALIZED EVIDENCE COMPONENTS
    # -----------------------------------------------------

    def normalize_approach(self, speed):

        if speed <= 0:
            return 0.0

        # 1.2 m/s or above reaches prototype maximum.
        return min(
            speed / 1.2,
            1.0,
        )

    def normalize_physiology(self, residual):

        if residual <= 0:
            return 0.0

        return min(
            residual,
            1.0,
        )

    # -----------------------------------------------------
    # PAC
    # -----------------------------------------------------

    def analyze(
        self,
        ego_results,
        physiological_samples,
    ):

        approach_time, approach_speed = (
            self.find_peak_approach(
                ego_results
            )
        )

        physiology_time, physiology_residual = (
            self.find_physiological_response(
                physiological_samples,
                approach_time,
            )
        )

        temporal_alignment, lag = (
            self.calculate_temporal_alignment(
                approach_time,
                physiology_time,
            )
        )

        approach_strength = (
            self.normalize_approach(
                approach_speed
            )
        )

        physiological_strength = (
            self.normalize_physiology(
                physiology_residual
            )
        )

        # Multiplicative prototype coupling:
        # PAC becomes strong only when all three exist:
        # approach + physiological response + temporal alignment.
        pac_evidence = (
            approach_strength
            * physiological_strength
            * temporal_alignment
        )

        pac_evidence = round(
            min(max(pac_evidence, 0.0), 1.0),
            2,
        )

        coupling_detected = (
            approach_speed
            >= self.minimum_approach_speed
            and physiology_residual
            >= self.minimum_physiological_residual
            and temporal_alignment > 0
        )

        return PACResult(
            peak_approach_time=approach_time,
            peak_approach_speed=round(
                approach_speed,
                2,
            ),
            peak_physiological_time=physiology_time,
            peak_physiological_residual=round(
                physiology_residual,
                2,
            ),
            response_lag=(
                round(lag, 2)
                if lag is not None
                else None
            ),
            temporal_alignment=round(
                temporal_alignment,
                2,
            ),
            approach_strength=round(
                approach_strength,
                2,
            ),
            physiological_strength=round(
                physiological_strength,
                2,
            ),
            pac_evidence=pac_evidence,
            coupling_detected=coupling_detected,
        )


def display_pac(
    scenario_name,
    result: PACResult,
):

    print()
    print("=" * 72)
    print(
        "BEYOND-SOS | PERSON 2 | "
        "TEMPORAL PAC PROTOTYPE"
    )
    print("=" * 72)

    print(
        f"Scenario                  : "
        f"{scenario_name}"
    )

    print("-" * 72)

    if result.peak_approach_time is None:

        print("Corrected Approach Event  : NONE")

    else:

        print(
            f"Peak Approach Time        : "
            f"{result.peak_approach_time:.1f} s"
        )

        print(
            f"Peak Corrected Approach   : "
            f"{result.peak_approach_speed:.2f} m/s"
        )

    if result.peak_physiological_time is None:

        print(
            "Physiological Response    : "
            "NO TIME-ALIGNED RESPONSE"
        )

    else:

        print(
            f"Physiology Peak Time      : "
            f"{result.peak_physiological_time:.1f} s"
        )

        print(
            f"Physiology Residual       : "
            f"{result.peak_physiological_residual:.2f}"
        )

    print("-" * 72)

    if result.response_lag is None:

        print(
            "Response Lag              : "
            "N/A"
        )

    else:

        print(
            f"Response Lag              : "
            f"{result.response_lag:.1f} s"
        )

    print(
        f"Temporal Alignment        : "
        f"{result.temporal_alignment:.2f}"
    )

    print(
        f"Approach Strength         : "
        f"{result.approach_strength:.2f}"
    )

    print(
        f"Physiology Strength       : "
        f"{result.physiological_strength:.2f}"
    )

    print("-" * 72)

    print(
        f"PAC EVIDENCE              : "
        f"{result.pac_evidence:.2f} / 1.00"
    )

    print(
        f"TEMPORAL COUPLING         : "
        f"{'DETECTED' if result.coupling_detected else 'NOT DETECTED'}"
    )

    print("-" * 72)

    print(
        "NOTE: PAC represents prototype temporal coupling evidence."
    )

    print(
        "It is not a clinical metric or standalone danger probability."
    )

    print("=" * 72)