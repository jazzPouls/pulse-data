# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2020 Recidiviz, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================
"""Test the PopulationSimulation object"""
import unittest
from copy import deepcopy
import pandas as pd
from pandas.testing import assert_index_equal

from recidiviz.calculator.modeling.population_projection.simulations.compartment_transitions import (
    CompartmentTransitions,
)
from recidiviz.calculator.modeling.population_projection.spark_policy import SparkPolicy
from recidiviz.calculator.modeling.population_projection.simulations.population_simulation.population_simulation_factory import (
    PopulationSimulationFactory,
)


class TestPopulationSimulation(unittest.TestCase):
    """Test the PopulationSimulation class runs correctly"""

    def setUp(self):
        self.test_outflows_data = pd.DataFrame(
            {
                "total_population": [4, 2, 2, 4, 3],
                "crime": ["NAR"] * 5,
                "outflow_to": [
                    "supervision",
                    "prison",
                    "supervision",
                    "prison",
                    "prison",
                ],
                "compartment": [
                    "prison",
                    "supervision",
                    "prison",
                    "pretrial",
                    "pretrial",
                ],
                "time_step": [0] * 5,
            }
        )

        self.test_transitions_data = pd.DataFrame(
            {
                "compartment_duration": [1, 1, 2],
                "total_population": [4, 2, 2],
                "crime": ["NAR"] * 3,
                "outflow_to": ["supervision", "prison", "supervision"],
                "compartment": ["prison", "supervision", "prison"],
                "time_step": [0] * 3,
            }
        )

        self.test_total_population_data = pd.DataFrame(
            {
                "total_population": [10] * 5,
                "compartment": ["prison"] * 5,
                "crime": ["NAR"] * 5,
                "time_step": range(-4, 1),
            }
        )

        self.user_inputs = {
            "projection_time_steps": 10,
            "policy_time_step": 2,
            "start_time_step": 0,
            "constant_admissions": True,
            "speed_run": False,
        }
        self.simulation_architecture = {
            "pretrial": "shell",
            "prison": "full",
            "supervision": "full",
        }

    def test_disaggregation_axes_must_be_in_data_dfs(self):
        test_outflows_data = self.test_outflows_data.drop("crime", axis=1)

        test_transitions_data = self.test_transitions_data.drop("crime", axis=1)

        test_total_population_data = self.test_total_population_data.drop(
            "crime", axis=1
        )

        with self.assertRaises(ValueError):
            _ = PopulationSimulationFactory.build_population_simulation(
                test_outflows_data,
                self.test_transitions_data,
                test_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                [],
                -5,
                pd.DataFrame(),
                False,
                True,
            )

        with self.assertRaises(ValueError):
            _ = PopulationSimulationFactory.build_population_simulation(
                self.test_outflows_data,
                self.test_transitions_data,
                test_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                [],
                -5,
                pd.DataFrame(),
                False,
                True,
            )

        with self.assertRaises(ValueError):
            _ = PopulationSimulationFactory.build_population_simulation(
                test_outflows_data,
                self.test_transitions_data,
                self.test_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                [],
                -5,
                pd.DataFrame(),
                False,
                True,
            )

        with self.assertRaises(ValueError):
            _ = PopulationSimulationFactory.build_population_simulation(
                self.test_outflows_data,
                test_transitions_data,
                self.test_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                [],
                -5,
                pd.DataFrame(),
                False,
                True,
            )

    def test_simulation_forces_complete_user_inputs_dict(self):

        for i in self.user_inputs:
            test_user_inputs = deepcopy(self.user_inputs)
            test_user_inputs.pop(i)
            with self.assertRaises(ValueError):
                _ = PopulationSimulationFactory.build_population_simulation(
                    self.test_outflows_data,
                    self.test_transitions_data,
                    self.test_total_population_data,
                    self.simulation_architecture,
                    ["crime"],
                    test_user_inputs,
                    [],
                    -5,
                    pd.DataFrame(),
                    False,
                    True,
                )

    def test_microsim_requires_empty_policy_list(self):
        with self.assertRaises(ValueError):
            policy_list = [
                SparkPolicy(
                    CompartmentTransitions.test_non_retroactive_policy,
                    "supervision",
                    {"crime": "NAR"},
                )
            ]
            _ = PopulationSimulationFactory.build_population_simulation(
                self.test_outflows_data,
                self.test_transitions_data,
                self.test_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                policy_list,
                -5,
                self.test_outflows_data,
                True,
                False,
            )

    def test_baseline_with_backcast_projection_on(self):
        """Assert that the simulation results has negative time steps when the back-cast is enabled"""
        population_simulation = PopulationSimulationFactory.build_population_simulation(
            self.test_outflows_data,
            self.test_transitions_data,
            self.test_total_population_data,
            self.simulation_architecture,
            ["crime"],
            self.user_inputs,
            [],
            -5,
            pd.DataFrame(),
            False,
            True,
        )
        projection = population_simulation.simulate_policies()

        assert_index_equal(
            projection.index.unique().sort_values(), pd.Int64Index(range(-5, 10))
        )

    def test_baseline_with_backcast_projection_off(self):
        """Assert that microsim simulation results only have positive time steps"""
        population_simulation = PopulationSimulationFactory.build_population_simulation(
            self.test_outflows_data,
            self.test_transitions_data,
            self.test_total_population_data,
            self.simulation_architecture,
            ["crime"],
            self.user_inputs,
            [],
            0,
            self.test_transitions_data,
            True,
            False,
        )
        projection = population_simulation.simulate_policies()

        assert_index_equal(
            projection.index.unique().sort_values(), pd.Int64Index(range(11))
        )

    def test_dropping_data_raises_warning(self):
        """Assert that PopulationSimulation throws an error when some input data goes unused"""
        non_disaggregated_outflows_data = self.test_outflows_data.copy()
        non_disaggregated_transitions_data = self.test_transitions_data.copy()
        non_disaggregated_total_population_data = self.test_total_population_data.copy()

        non_disaggregated_outflows_data.loc[
            non_disaggregated_outflows_data.compartment != "pretrial", "crime"
        ] = None
        non_disaggregated_transitions_data.loc[
            non_disaggregated_transitions_data.index == 0, "crime"
        ] = None
        non_disaggregated_total_population_data.crime = None

        with self.assertWarns(Warning):
            _ = PopulationSimulationFactory.build_population_simulation(
                self.test_outflows_data,
                self.test_transitions_data,
                non_disaggregated_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                [],
                -5,
                pd.DataFrame(),
                False,
                True,
            )

        with self.assertWarns(Warning):
            _ = PopulationSimulationFactory.build_population_simulation(
                self.test_outflows_data,
                non_disaggregated_transitions_data,
                self.test_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                [],
                -5,
                pd.DataFrame(),
                False,
                True,
            )

        with self.assertWarns(Warning):
            _ = PopulationSimulationFactory.build_population_simulation(
                non_disaggregated_outflows_data,
                self.test_transitions_data,
                self.test_total_population_data,
                self.simulation_architecture,
                ["crime"],
                self.user_inputs,
                [],
                -5,
                pd.DataFrame(),
                False,
                True,
            )
