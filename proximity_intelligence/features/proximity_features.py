"""
BEYOND-SOS
Person 2: Proximity Intelligence

Phase 2 - Proximity Feature Extraction

Converts simulated radar distance measurements into meaningful
interpersonal-motion features.

Features:
1. Distance
2. Closing speed
3. Motion direction
4. Nearby duration
"""

from dataclasses import dataclass


@dataclass
class ProximityFeature:
    """Features extracted for one point in time."""

    timestamp: float
    distance: float
    closing_speed: float
    motion: str
    nearby_duration: float


class ProximityFeatureExtractor:

    def __init__(
        self,
        nearby_threshold: float = 2.5,
        motion_threshold: float = 0.15,
    ):
        """
        nearby_threshold:
            Prototype distance used to measure how long someone
            remains nearby.

        motion_threshold:
            Small speed changes below this value are treated as
            approximately stable to reduce sensitivity to noise.

        These are prototype parameters, not validated danger thresholds.
        """

        self.nearby_threshold = nearby_threshold
        self.motion_threshold = motion_threshold

    def calculate_closing_speed(
        self,
        previous_distance,
        current_distance,
        time_difference,
    ):
        """
        Positive closing speed  -> distance decreasing
        Negative closing speed  -> distance increasing
        Near zero               -> approximately stable
        """

        if time_difference <= 0:
            return 0.0

        return (
            previous_distance - current_distance
        ) / time_difference

    def classify_motion(self, closing_speed):
        """Classify relative motion from closing speed."""

        if closing_speed > self.motion_threshold:
            return "APPROACHING"

        elif closing_speed < -self.motion_threshold:
            return "RETREATING"

        else:
            return "STABLE"

    def extract(self, readings):
        """Extract proximity features from radar readings."""

        if not readings:
            return []

        features = []

        nearby_duration = 0.0

        # First measurement has no previous point,
        # so closing speed cannot yet be calculated.
        first = readings[0]

        features.append(
            ProximityFeature(
                timestamp=first.timestamp,
                distance=first.distance,
                closing_speed=0.0,
                motion="INITIAL",
                nearby_duration=0.0,
            )
        )

        for index in range(1, len(readings)):

            previous = readings[index - 1]
            current = readings[index]

            dt = current.timestamp - previous.timestamp

            closing_speed = self.calculate_closing_speed(
                previous.distance,
                current.distance,
                dt,
            )

            motion = self.classify_motion(closing_speed)

            # Measure continuous time spent inside the prototype
            # nearby region.
            if current.distance <= self.nearby_threshold:
                nearby_duration += dt
            else:
                nearby_duration = 0.0

            feature = ProximityFeature(
                timestamp=current.timestamp,
                distance=current.distance,
                closing_speed=closing_speed,
                motion=motion,
                nearby_duration=nearby_duration,
            )

            features.append(feature)

        return features


def display_features(scenario_name, features):

    print("\n" + "=" * 80)
    print("BEYOND-SOS | PERSON 2 | PROXIMITY FEATURE EXTRACTION")
    print("=" * 80)

    print(f"Scenario: {scenario_name.replace('_', ' ').title()}")

    print("-" * 80)

    print(
        f"{'Time':<10}"
        f"{'Distance':<15}"
        f"{'Closing Speed':<20}"
        f"{'Motion':<18}"
        f"{'Nearby Time':<15}"
    )

    print("-" * 80)

    for feature in features:

        print(
            f"{feature.timestamp:<10.1f}"
            f"{feature.distance:<15.2f}"
            f"{feature.closing_speed:<20.2f}"
            f"{feature.motion:<18}"
            f"{feature.nearby_duration:<15.1f}"
        )

    print("=" * 80)