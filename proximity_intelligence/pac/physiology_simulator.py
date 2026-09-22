"""
BEYOND-SOS
Person 2: PAC Prototype

Simulated activity-conditioned physiological residual stream.

This temporarily represents the processed physiological output
that will later be supplied by Person 1's module.

Values are synthetic and are used only for software-pipeline
validation and demonstration.
"""

from pac.pac_analyzer import PhysiologicalSample


class PhysiologySimulator:

    # -----------------------------------------------------
    # APPROACH-LINKED RESPONSE
    # -----------------------------------------------------

    def approach_response(
        self,
        duration=12,
        response_start=2,
        peak_residual=0.85,
    ):
        """
        Simulates a physiological deviation that develops
        shortly after an interpersonal approach event.
        """

        samples = []

        for time in range(duration + 1):

            if time < response_start:
                residual = 0.05

            elif time == response_start:
                residual = 0.35

            elif time == response_start + 1:
                residual = 0.65

            elif time == response_start + 2:
                residual = peak_residual

            elif time == response_start + 3:
                residual = 0.55

            else:
                residual = 0.15

            samples.append(
                PhysiologicalSample(
                    timestamp=float(time),
                    residual=round(residual, 2),
                )
            )

        return samples

    # -----------------------------------------------------
    # EXERCISE / ACTIVITY RESPONSE
    # -----------------------------------------------------

    def exercise_response(
        self,
        duration=12,
    ):
        """
        Simulates elevated raw physiology caused by activity.

        Because this value represents an activity-conditioned
        residual rather than raw heart rate, the residual
        remains relatively small.
        """

        samples = []

        for time in range(duration + 1):

            residual = (
                0.08
                if time % 3 != 0
                else 0.12
            )

            samples.append(
                PhysiologicalSample(
                    timestamp=float(time),
                    residual=residual,
                )
            )

        return samples

    # -----------------------------------------------------
    # NO SIGNIFICANT PHYSIOLOGICAL RESPONSE
    # -----------------------------------------------------

    def neutral_response(
        self,
        duration=12,
    ):

        samples = []

        for time in range(duration + 1):

            residual = (
                0.04
                if time % 2 == 0
                else 0.06
            )

            samples.append(
                PhysiologicalSample(
                    timestamp=float(time),
                    residual=residual,
                )
            )

        return samples