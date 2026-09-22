"""
BEYOND-SOS
Person 2 - Proximity Intelligence Demo

Current pipeline:

Parameterized Scenario Generation
        ↓
Radar Simulation
        ↓
Proximity Feature Extraction
        ↓
Ego-Motion Compensation
        ↓
Behaviour Intelligence
"""

from simulation.radar_simulator import RadarSimulator

from features.proximity_features import (
    ProximityFeatureExtractor,
    display_features,
)

from ego_motion.ego_motion import (
    EgoMotionCompensator,
    display_ego_motion,
)

from behavior.behavior_analyzer import (
    BehaviourAnalyzer,
    display_behaviour,
)


def main():

    print("\n" + "=" * 65)
    print("BEYOND-SOS")
    print("PERSON 2 - PROXIMITY INTELLIGENCE")
    print("=" * 65)

    simulator = RadarSimulator(
        sample_interval=1.0
    )

    # -----------------------------------------------------
    # SELECT SCENARIO
    # -----------------------------------------------------

    scenarios = simulator.available_scenarios()

    print("\nAvailable Scenarios\n")

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

        # -------------------------------------------------
        # SELECT PRESET
        # -------------------------------------------------

        presets = simulator.available_presets(
            selected_scenario
        )

        print("\nAvailable Presets\n")

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

        # -------------------------------------------------
        # PHASE 1 - PARAMETERIZED RADAR SIMULATION
        # -------------------------------------------------

        readings = simulator.generate(
            scenario_name=selected_scenario,
            preset_name=selected_preset,
        )

        # -------------------------------------------------
        # PHASE 2 - PROXIMITY FEATURE EXTRACTION
        # -------------------------------------------------

        extractor = ProximityFeatureExtractor(
            nearby_threshold=2.5,
            motion_threshold=0.15,
        )

        features = extractor.extract(
            readings
        )

        display_features(
            selected_scenario,
            features,
        )

        # -------------------------------------------------
        # PHASE 3 - EGO-MOTION COMPENSATION
        # -------------------------------------------------

        compensator = EgoMotionCompensator(
            motion_threshold=0.15
        )

        ego_results = compensator.process(
            readings,
            features,
        )

        display_ego_motion(
            selected_scenario,
            ego_results,
        )

        # -------------------------------------------------
        # PHASE 4 - BEHAVIOUR INTELLIGENCE
        # -------------------------------------------------

        behaviour_analyzer = BehaviourAnalyzer(
            nearby_threshold=2.5,
            persistence_threshold=5.0,
            rapid_approach_threshold=0.6,
        )

        behaviour_result = behaviour_analyzer.analyze(
            selected_scenario,
            features,
            ego_results,
        )

        display_behaviour(
            behaviour_result
        )

    except ValueError as error:

        print(
            "\nInvalid selection or parameters."
        )

        if str(error):
            print(error)


if __name__ == "__main__":
    main()