"""
BEYOND-SOS
Person 2: Proximity Intelligence

Phase 4 Upgrade - Parameterized Scenario Generator

Instead of storing one fixed distance array for every situation,
this module generates simulated radar data from scenario parameters.

These streams are for prototype validation and demonstration.
They are not experimental human-behaviour datasets.
"""

from dataclasses import dataclass
import math


@dataclass
class ScenarioSample:
    timestamp: float
    distance: float
    wearer_speed: float


# ---------------------------------------------------------
# PRESETS
# ---------------------------------------------------------
# Presets only provide starting parameters.
# The actual sensor stream is generated mathematically.

PRESETS = {

    "normal_passing": {
        "typical": {
            "start_distance": 7.0,
            "minimum_distance": 1.8,
            "passing_speed": 0.8,
        },
        "close": {
            "start_distance": 7.0,
            "minimum_distance": 1.2,
            "passing_speed": 0.9,
        },
    },

    "rapid_approach": {
        "moderate": {
            "start_distance": 8.0,
            "closest_distance": 1.5,
            "approach_speed": 0.7,
        },
        "rapid": {
            "start_distance": 9.0,
            "closest_distance": 1.0,
            "approach_speed": 1.2,
        },
    },

    "sustained_proximity": {
        "short": {
            "distance": 2.2,
            "duration": 8,
            "variation": 0.12,
        },
        "prolonged": {
            "distance": 1.8,
            "duration": 25,
            "variation": 0.15,
        },
    },

    "standing_nearby": {
        "normal": {
            "distance": 2.3,
            "duration": 10,
            "variation": 0.04,
        },
        "close": {
            "distance": 1.5,
            "duration": 18,
            "variation": 0.04,
        },
    },

    "retreat_reapproach": {
        "once": {
            "start_distance": 6.0,
            "closest_distance": 1.5,
            "retreat_distance": 4.5,
            "cycles": 1,
            "movement_speed": 0.8,
        },
        "repeated": {
            "start_distance": 6.0,
            "closest_distance": 1.2,
            "retreat_distance": 4.5,
            "cycles": 2,
            "movement_speed": 0.9,
        },
    },

    "ego_motion_control": {
        "walking": {
            "start_distance": 8.0,
            "closest_distance": 1.6,
            "wearer_speed": 0.8,
            "target_speed": 0.0,
        },
        "fast_walking": {
            "start_distance": 9.0,
            "closest_distance": 1.5,
            "wearer_speed": 1.2,
            "target_speed": 0.0,
        },
    },
}


class ScenarioGenerator:

    def __init__(self, sample_interval: float = 1.0):
        self.sample_interval = sample_interval

    def available_scenarios(self):
        return list(PRESETS.keys())

    def available_presets(self, scenario_name):
        if scenario_name not in PRESETS:
            raise ValueError(
                f"Unknown scenario: {scenario_name}"
            )

        return list(PRESETS[scenario_name].keys())

    def get_preset(self, scenario_name, preset_name):
        if scenario_name not in PRESETS:
            raise ValueError(
                f"Unknown scenario: {scenario_name}"
            )

        if preset_name not in PRESETS[scenario_name]:
            raise ValueError(
                f"Unknown preset '{preset_name}' "
                f"for scenario '{scenario_name}'"
            )

        # Return a copy so future UI changes do not
        # accidentally modify the original preset.
        return PRESETS[scenario_name][preset_name].copy()

    # -----------------------------------------------------
    # HELPER
    # -----------------------------------------------------

    def _sample(
        self,
        timestamp,
        distance,
        wearer_speed=0.0,
    ):
        return ScenarioSample(
            timestamp=round(timestamp, 2),
            distance=round(max(distance, 0.1), 2),
            wearer_speed=round(wearer_speed, 2),
        )

    # -----------------------------------------------------
    # NORMAL PASSING
    # -----------------------------------------------------

    def generate_normal_passing(
        self,
        start_distance,
        minimum_distance,
        passing_speed,
    ):
        samples = []
        time = 0.0
        distance = start_distance

        # Person approaches.
        while distance > minimum_distance:

            samples.append(
                self._sample(
                    time,
                    distance,
                )
            )

            distance -= (
                passing_speed
                * self.sample_interval
            )

            time += self.sample_interval

        # Add closest point.
        samples.append(
            self._sample(
                time,
                minimum_distance,
            )
        )

        # Person passes and retreats.
        distance = (
            minimum_distance
            + passing_speed * self.sample_interval
        )

        time += self.sample_interval

        while distance <= start_distance:

            samples.append(
                self._sample(
                    time,
                    distance,
                )
            )

            distance += (
                passing_speed
                * self.sample_interval
            )

            time += self.sample_interval

        return samples

    # -----------------------------------------------------
    # RAPID APPROACH
    # -----------------------------------------------------

    def generate_rapid_approach(
        self,
        start_distance,
        closest_distance,
        approach_speed,
    ):
        samples = []
        time = 0.0
        distance = start_distance

        while distance > closest_distance:

            samples.append(
                self._sample(
                    time,
                    distance,
                )
            )

            distance -= (
                approach_speed
                * self.sample_interval
            )

            time += self.sample_interval

        # Add final closest point.
        samples.append(
            self._sample(
                time,
                closest_distance,
            )
        )

        return samples

    # -----------------------------------------------------
    # SUSTAINED PROXIMITY
    # -----------------------------------------------------

    def generate_sustained_proximity(
        self,
        distance,
        duration,
        variation,
    ):
        samples = []

        number_of_samples = int(
            duration / self.sample_interval
        )

        for index in range(number_of_samples + 1):

            time = (
                index
                * self.sample_interval
            )

            # Smooth deterministic variation.
            # This avoids random output during the review.
            offset = variation * math.sin(
                index * 0.8
            )

            current_distance = (
                distance + offset
            )

            samples.append(
                self._sample(
                    time,
                    current_distance,
                )
            )

        return samples

    # -----------------------------------------------------
    # STANDING NEARBY
    # -----------------------------------------------------

    def generate_standing_nearby(
        self,
        distance,
        duration,
        variation,
    ):
        samples = []

        number_of_samples = int(
            duration / self.sample_interval
        )

        for index in range(number_of_samples + 1):

            time = (
                index
                * self.sample_interval
            )

            # Very small deterministic sensor-like variation.
            offset = variation * math.sin(
                index * 0.5
            )

            current_distance = (
                distance + offset
            )

            samples.append(
                self._sample(
                    time,
                    current_distance,
                )
            )

        return samples

    # -----------------------------------------------------
    # RETREAT AND RE-APPROACH
    # -----------------------------------------------------

    def generate_retreat_reapproach(
        self,
        start_distance,
        closest_distance,
        retreat_distance,
        cycles,
        movement_speed,
    ):
        samples = []

        time = 0.0
        distance = start_distance

        for cycle_index in range(cycles + 1):

            # -----------------------------
            # APPROACH
            # -----------------------------

            while distance > closest_distance:

                samples.append(
                    self._sample(
                        time,
                        distance,
                    )
                )

                distance -= (
                    movement_speed
                    * self.sample_interval
                )

                time += self.sample_interval

            distance = closest_distance

            samples.append(
                self._sample(
                    time,
                    distance,
                )
            )

            time += self.sample_interval

            # Do not retreat after
            # the final approach.
            if cycle_index == cycles:
                break

            # -----------------------------
            # RETREAT
            # -----------------------------

            distance += (
                movement_speed
                * self.sample_interval
            )

            while distance < retreat_distance:

                samples.append(
                    self._sample(
                        time,
                        distance,
                    )
                )

                distance += (
                    movement_speed
                    * self.sample_interval
                )

                time += self.sample_interval

            distance = retreat_distance

            samples.append(
                self._sample(
                    time,
                    distance,
                )
            )

            time += self.sample_interval

        return samples

    # -----------------------------------------------------
    # EGO-MOTION CONTROL
    # -----------------------------------------------------

    def generate_ego_motion_control(
        self,
        start_distance,
        closest_distance,
        wearer_speed,
        target_speed,
    ):
        samples = []

        time = 0.0
        distance = start_distance

        # Positive target_speed means that the target is
        # moving away from the wearer in this simplified
        # one-dimensional prototype.
        observed_closing_speed = (
            wearer_speed - target_speed
        )

        # If there is no positive closing motion,
        # return the initial sample only.
        if observed_closing_speed <= 0:

            return [
                self._sample(
                    time,
                    distance,
                    wearer_speed,
                )
            ]

        while distance > closest_distance:

            samples.append(
                self._sample(
                    time,
                    distance,
                    wearer_speed,
                )
            )

            distance -= (
                observed_closing_speed
                * self.sample_interval
            )

            time += self.sample_interval

        # Add closest-distance endpoint only when the
        # previous generated sample is not already equal
        # to that endpoint.
        #
        # This prevents:
        # 8.0 s -> 1.60 m
        # 9.0 s -> 1.60 m
        #
        # which previously created an artificial final
        # motion classification.
        if (
            not samples
            or samples[-1].distance
            != round(closest_distance, 2)
        ):
            samples.append(
                self._sample(
                    time,
                    closest_distance,
                    wearer_speed,
                )
            )

        return samples

    # -----------------------------------------------------
    # MAIN GENERATOR
    # -----------------------------------------------------

    def generate(
        self,
        scenario_name,
        parameters,
    ):

        if scenario_name == "normal_passing":

            return self.generate_normal_passing(
                **parameters
            )

        elif scenario_name == "rapid_approach":

            return self.generate_rapid_approach(
                **parameters
            )

        elif scenario_name == "sustained_proximity":

            return self.generate_sustained_proximity(
                **parameters
            )

        elif scenario_name == "standing_nearby":

            return self.generate_standing_nearby(
                **parameters
            )

        elif scenario_name == "retreat_reapproach":

            return self.generate_retreat_reapproach(
                **parameters
            )

        elif scenario_name == "ego_motion_control":

            return self.generate_ego_motion_control(
                **parameters
            )

        else:

            raise ValueError(
                f"Unknown scenario: {scenario_name}"
            )