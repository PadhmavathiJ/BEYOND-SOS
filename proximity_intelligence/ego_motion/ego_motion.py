"""
BEYOND-SOS
Person 2: Proximity Intelligence

Phase 3 - Ego-Motion Compensation

Radar measures relative motion between the wearer and another person.
If the wearer is moving, part of the observed closing speed may be
caused by the wearer rather than the other person.

This module uses the wearer's simulated motion information to estimate
the target's corrected approach speed.
"""

from dataclasses import dataclass


@dataclass
class EgoMotionResult:
    """Stores corrected motion information for one time point."""

    timestamp: float
    distance: float

    observed_closing_speed: float
    wearer_speed: float

    corrected_target_speed: float

    raw_motion: str
    corrected_motion: str


class EgoMotionCompensator:

    def __init__(self, motion_threshold: float = 0.15):
        """
        motion_threshold is a prototype parameter.

        Speeds smaller than this magnitude are treated as
        approximately stationary.
        """

        self.motion_threshold = motion_threshold

    def compensate(
        self,
        observed_closing_speed,
        wearer_speed,
    ):
        """
        Estimate target approach speed.

        Prototype 1D radial-motion model:

        corrected target approach
            = observed closing speed - wearer contribution

        Positive  -> target approaching wearer
        Negative  -> target retreating from wearer
        Near zero -> target approximately stationary
        """

        return observed_closing_speed - wearer_speed

    def classify_corrected_motion(self, corrected_speed):

        if corrected_speed > self.motion_threshold:
            return "TARGET APPROACHING"

        elif corrected_speed < -self.motion_threshold:
            return "TARGET RETREATING"

        else:
            return "TARGET STATIONARY"

    def process(self, readings, features):

        if len(readings) != len(features):
            raise ValueError(
                "Radar readings and proximity features must have "
                "the same number of samples."
            )

        results = []

        for reading, feature in zip(readings, features):

            # No motion estimate exists for the initial sample.
            if feature.motion == "INITIAL":

                corrected_speed = 0.0
                corrected_motion = "INITIAL"

            else:

                corrected_speed = self.compensate(
                    feature.closing_speed,
                    reading.wearer_speed,
                )

                corrected_motion = (
                    self.classify_corrected_motion(
                        corrected_speed
                    )
                )

            result = EgoMotionResult(
                timestamp=feature.timestamp,
                distance=feature.distance,
                observed_closing_speed=feature.closing_speed,
                wearer_speed=reading.wearer_speed,
                corrected_target_speed=corrected_speed,
                raw_motion=feature.motion,
                corrected_motion=corrected_motion,
            )

            results.append(result)

        return results


def display_ego_motion(scenario_name, results):

    print("\n" + "=" * 105)
    print("BEYOND-SOS | PERSON 2 | EGO-MOTION COMPENSATION")
    print("=" * 105)

    print(
        f"Scenario: "
        f"{scenario_name.replace('_', ' ').title()}"
    )

    print("-" * 105)

    print(
        f"{'Time':<8}"
        f"{'Dist':<10}"
        f"{'Observed':<13}"
        f"{'Wearer':<12}"
        f"{'Corrected':<13}"
        f"{'Raw Motion':<18}"
        f"{'After Correction':<22}"
    )

    print("-" * 105)

    for result in results:

        print(
            f"{result.timestamp:<8.1f}"
            f"{result.distance:<10.2f}"
            f"{result.observed_closing_speed:<13.2f}"
            f"{result.wearer_speed:<12.2f}"
            f"{result.corrected_target_speed:<13.2f}"
            f"{result.raw_motion:<18}"
            f"{result.corrected_motion:<22}"
        )

    print("=" * 105)