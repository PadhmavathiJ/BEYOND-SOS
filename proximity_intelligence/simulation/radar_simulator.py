"""
BEYOND-SOS
Person 2: Proximity Intelligence

Radar Simulator

Connects the parameterized Scenario Generator to the
rest of the proximity-intelligence pipeline.

The generated readings simulate the type of distance and
wearer-motion data that will later come from the physical
radar and IMU.
"""

from dataclasses import dataclass

try:
    from simulation.scenario_generator import ScenarioGenerator
except ModuleNotFoundError:
    from scenario_generator import ScenarioGenerator


@dataclass
class RadarReading:
    """Represents one simulated radar measurement."""

    timestamp: float
    distance: float
    wearer_speed: float = 0.0


class RadarSimulator:

    def __init__(self, sample_interval: float = 1.0):

        self.sample_interval = sample_interval

        self.generator = ScenarioGenerator(
            sample_interval=sample_interval
        )

    def available_scenarios(self):
        """Return all available scenario families."""

        return self.generator.available_scenarios()

    def available_presets(self, scenario_name):
        """Return presets available for a scenario."""

        return self.generator.available_presets(
            scenario_name
        )

    def generate(
        self,
        scenario_name,
        preset_name=None,
        custom_parameters=None,
    ):
        """
        Generate radar readings.

        The caller can either:

        1. Choose a predefined preset

        OR

        2. Supply custom parameters.

        Custom parameters will later come from the
        visual simulator controls.
        """

        if custom_parameters is not None:

            parameters = custom_parameters.copy()

        elif preset_name is not None:

            parameters = self.generator.get_preset(
                scenario_name,
                preset_name,
            )

        else:

            raise ValueError(
                "Either preset_name or "
                "custom_parameters must be provided."
            )

        generated_samples = self.generator.generate(
            scenario_name,
            parameters,
        )

        readings = []

        for sample in generated_samples:

            reading = RadarReading(
                timestamp=sample.timestamp,
                distance=sample.distance,
                wearer_speed=sample.wearer_speed,
            )

            readings.append(reading)

        return readings


def display_readings(
    scenario_name,
    preset_name,
    readings,
):

    print("\n" + "=" * 70)

    print(
        "BEYOND-SOS | PERSON 2 | "
        "PARAMETERIZED RADAR SIMULATION"
    )

    print("=" * 70)

    print(
        f"Scenario : "
        f"{scenario_name.replace('_', ' ').title()}"
    )

    if preset_name:

        print(
            f"Preset   : "
            f"{preset_name.replace('_', ' ').title()}"
        )

    print("-" * 70)

    print(
        f"{'Time (s)':<15}"
        f"{'Distance (m)':<20}"
        f"{'Wearer Speed (m/s)':<25}"
    )

    print("-" * 70)

    for reading in readings:

        print(
            f"{reading.timestamp:<15.1f}"
            f"{reading.distance:<20.2f}"
            f"{reading.wearer_speed:<25.2f}"
        )

    print("=" * 70)


# ---------------------------------------------------------
# Standalone test
# ---------------------------------------------------------

if __name__ == "__main__":

    simulator = RadarSimulator(
        sample_interval=1.0
    )

    scenarios = simulator.available_scenarios()

    print("\nAvailable Scenarios:")

    for number, scenario in enumerate(
        scenarios,
        start=1,
    ):

        print(
            f"{number}. "
            f"{scenario.replace('_', ' ').title()}"
        )

    try:

        scenario_choice = int(
            input("\nSelect scenario number: ")
        )

        if (
            scenario_choice < 1
            or scenario_choice > len(scenarios)
        ):
            raise ValueError

        selected_scenario = scenarios[
            scenario_choice - 1
        ]

        presets = simulator.available_presets(
            selected_scenario
        )

        print("\nAvailable Presets:")

        for number, preset in enumerate(
            presets,
            start=1,
        ):

            print(
                f"{number}. "
                f"{preset.replace('_', ' ').title()}"
            )

        preset_choice = int(
            input("\nSelect preset number: ")
        )

        if (
            preset_choice < 1
            or preset_choice > len(presets)
        ):
            raise ValueError

        selected_preset = presets[
            preset_choice - 1
        ]

        readings = simulator.generate(
            scenario_name=selected_scenario,
            preset_name=selected_preset,
        )

        display_readings(
            selected_scenario,
            selected_preset,
            readings,
        )

    except ValueError as error:

        print(
            "\nInvalid selection or parameters."
        )

        if str(error):
            print(error)