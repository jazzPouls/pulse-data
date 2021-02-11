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
"""Simulation object that models a given policy scenario"""

from typing import Dict, List, Any, Tuple
from time import time
import pandas as pd

from recidiviz.calculator.modeling.population_projection.simulations.population_simulation.\
    population_simulation_initializer import PopulationSimulationInitializer
from recidiviz.calculator.modeling.population_projection.spark_policy import SparkPolicy
from recidiviz.calculator.modeling.population_projection.simulations.sub_simulation.sub_simulation import SubSimulation


class PopulationSimulation:
    """Control the many sub simulations for one scenario (baseline/control or policy)"""
    def __init__(self, initializer: PopulationSimulationInitializer) -> None:
        self.sub_simulations: Dict[str, SubSimulation] = {}
        self.sub_group_ids_dict: Dict[str, Dict[str, Any]] = {}
        self.validation_population_data = pd.DataFrame()
        self.validation_transition_data = pd.DataFrame()
        self.population_projections = pd.DataFrame()
        self.initializer = initializer

    def simulate_policies(self, outflows_data: pd.DataFrame,
                          transitions_data: pd.DataFrame,
                          total_population_data: pd.DataFrame,
                          simulation_compartments: Dict[str, str],
                          disaggregation_axes: List[str],
                          user_inputs: Dict,
                          first_relevant_ts: int,
                          microsim_data: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Run a population projection and return population counts by year, compartment, and sub-group.
        `outflows_data` should be a DataFrame with columns for each sub-group, year, compartment, outflow_to,
            and total_population
        `transitions_data` should be a DataFrame with columns for each dis-aggregation axis, compartment,
            outflow_to, compartment_duration, and total_population
        `total_population_data` should be a DataFrame with columns for each disaggregation axis, compartment,
            time_step and total_population
        `disaggregation_axes` should be names of columns in historical_data that refer to sub-group categorizations
        `user_inputs` should be a dict including:
            'projection_time_steps': number of ts to project forward
            'policy_time_step': ts policies take effect
            'start_time_step': first ts of projection
            'policy_list': List of SparkPolicy objects to use for this simulation
            'backcast_projection': True if the simulation should be initialized with a backcast projection
            'constant_admissions': True if the admission population total should remain constant for each time step
        `first_relevant_ts` should be the ts to start initialization at
            initialization. Default is 2 to ensure long-sentence cohorts are well-populated.
        `microsim` should be a boolean indicating whether the simulation is a micro-simulation
        `microsim_data` should only be passed if microsim, and should be a DataFrame with real transitions data, whereas
            in that case `transitions_data` will actually be remaining_duration_data
        """

        start = time()

        self.validation_population_data = total_population_data

        # Check the inputs have the required fields and types
        required_user_inputs = ['projection_time_steps', 'policy_time_step', 'start_time_step', 'policy_list',
                                'constant_admissions', 'speed_run']
        missing_inputs = [key for key in required_user_inputs if key not in user_inputs]
        if len(missing_inputs) != 0:
            raise ValueError(f"Required user input are missing: {missing_inputs}")

        if any(not isinstance(policy, SparkPolicy) for policy in user_inputs['policy_list']):
            raise ValueError(f"Policy list can only include SparkPolicy objects: {user_inputs['policy_list']}")

        for axis in disaggregation_axes:
            for df in [outflows_data, transitions_data, total_population_data]:
                if axis not in df.columns:
                    raise ValueError(f"All disagregation axis must be included in the input dataframe columns\n"
                                     f"Expected: {disaggregation_axes}, Actual: {df.columns}")

        self.initializer.initialize_simulation(outflows_data, transitions_data, total_population_data,
                                               simulation_compartments, disaggregation_axes, user_inputs,
                                               first_relevant_ts, self.sub_group_ids_dict, microsim_data,
                                               self.sub_simulations)

        # run simulation up to the start_year
        self.step_forward(user_inputs['start_time_step'] - first_relevant_ts)

        time1 = time()
        print('initialization time: ', time1 - start)

        # Run the sub simulations for each ts
        self.step_forward(user_inputs['projection_time_steps'])

        #  Store the results in one Dataframe
        for simulation_group_id, simulation_obj in self.sub_simulations.items():
            sub_population_projection = simulation_obj.get_population_projections()
            sub_population_projection['simulation_group'] = simulation_group_id
            self.population_projections = pd.concat([self.population_projections, sub_population_projection])

        time2 = time()

        print('simulation_time: ', time2 - time1)

        return self.population_projections

    def step_forward(self, num_ts: int) -> None:
        for _ in range(num_ts):
            for simulation_obj in self.sub_simulations.values():
                simulation_obj.step_forward()

            cross_simulation_flows = pd.DataFrame(columns=['sub_group_id', 'compartment'])
            for sub_group_id, simulation_obj in self.sub_simulations.items():
                simulation_cohorts = simulation_obj.cross_flow()
                simulation_cohorts['sub_group_id'] = sub_group_id
                cross_simulation_flows = pd.concat([cross_simulation_flows, simulation_cohorts], sort=True)

            unassigned_cohorts = cross_simulation_flows[cross_simulation_flows.compartment.isnull()]
            if len(unassigned_cohorts) > 0:
                raise ValueError(f'cohorts passed up without compartment: {unassigned_cohorts}')

            cross_simulation_flows = self.update_cohort_attributes(cross_simulation_flows)

            for sub_group_id, simulation_obj in self.sub_simulations.items():
                sub_group_cohorts = cross_simulation_flows[cross_simulation_flows.sub_group_id
                                                           == sub_group_id].drop('sub_group_id', axis=1)
                simulation_obj.ingest_cross_simulation_cohorts(sub_group_cohorts)

    @staticmethod
    def update_cohort_attributes(cross_simulation_flows: pd.DataFrame) -> pd.DataFrame:
        """Should change sub_group_id for each row to whatever simulation that cohort should move to in the next ts"""
        return cross_simulation_flows

    def calculate_transition_error(self, validation_data: pd.DataFrame) -> pd.DataFrame:
        """
        validation_data should be a DataFrame with exactly:
            one column per axis of disaggregation, 'time_step', 'count', 'compartment', 'outflow_to'
        """

        self.validation_transition_data = validation_data

        aggregated_results = self.validation_transition_data.copy()
        aggregated_results['count'] = 0

        for sub_group_id, sub_group_obj in self.sub_simulations.items():
            for compartment_tag, compartment in sub_group_obj.simulation_compartments.items():
                for ts in set(self.validation_transition_data['time_step']):
                    index_locator = aggregated_results[aggregated_results['time_step'] == ts]
                    sub_group_id_dict = self.sub_group_ids_dict[sub_group_id]
                    sub_group_id_dict['compartment'] = compartment_tag
                    for axis in sub_group_id_dict:
                        if axis in index_locator.columns:
                            keepers = [sub_group_id_dict[axis] in i for i in index_locator[axis]]
                            index_locator = index_locator[keepers]

                    validation_indices = {outflow: index for index, outflow in
                                          index_locator['outflow_to'].iteritems()}

                    for outflow in validation_indices:
                        aggregated_results.loc[validation_indices[outflow], 'count'] += \
                            compartment.outflows[ts][outflow]
        return aggregated_results

    def gen_arima_output_df(self) -> pd.DataFrame:
        arima_output_df = pd.DataFrame()
        for simulation_group, sub_simulation in self.sub_simulations.items():
            output_df_sub = \
                pd.concat({simulation_group: sub_simulation.gen_arima_output_df()}, names=['simulation_group'])
            arima_output_df = arima_output_df.append(output_df_sub)
        return arima_output_df

    def gen_scale_factors_df(self) -> pd.DataFrame:
        scale_factors_df = pd.DataFrame()
        for subgroup_name, subgroup_obj in self.sub_simulations.items():
            subgroup_scale_factors = subgroup_obj.get_scale_factors()
            subgroup_scale_factors['sub-group'] = subgroup_name
            scale_factors_df = pd.concat([scale_factors_df, subgroup_scale_factors])
        return scale_factors_df

    def get_data_for_compartment_ts(self, compartment: str, ts: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
        simulation_population = self.population_projections[
            (self.population_projections.compartment == compartment) &
            (self.population_projections.time_step == ts)]
        historical_population = self.validation_population_data[
            (self.validation_population_data.compartment == compartment) &
            (self.validation_population_data.time_step == ts)]

        return simulation_population, historical_population

    def gen_total_population_error(self) -> pd.DataFrame:
        total_population_error = pd.DataFrame(index=self.validation_population_data.time_step.unique(),
                                              columns=self.validation_population_data.compartment.unique())

        min_projection_ts = min(self.population_projections['time_step'])
        for compartment in total_population_error.columns:
            for ts in total_population_error.index:
                if ts < min_projection_ts:
                    continue

                simulation_population, historical_population = self.get_data_for_compartment_ts(compartment, ts)
                simulation_population = simulation_population.total_population.sum()
                historical_population = historical_population.total_population.sum()

                if simulation_population == 0:
                    raise ValueError(f"Simulation population total for compartment {compartment} and time step {ts} "
                                     "cannot be 0 for validation")
                if historical_population == 0:
                    raise ValueError(f"Historical population data for compartment {compartment} and time step {ts} "
                                     "cannot be 0 for validation")

                total_population_error.loc[ts, compartment] = \
                    (simulation_population - historical_population) / historical_population

        return total_population_error.sort_index()

    def gen_full_error(self) -> pd.DataFrame:
        """Compile error data from sub-simulations"""
        min_projection_ts = min(self.population_projections['time_step'])
        total_population_error = pd.DataFrame(
            index=pd.MultiIndex.from_product([self.validation_population_data.compartment.unique(),
                                              range(min_projection_ts,
                                                    self.validation_population_data.time_step.max() + 1)],
                                             names=['compartment', 'time_step']),
            columns=['simulation_population', 'historical_population', 'percent_error']
        )

        for (compartment, ts) in total_population_error.index:

            simulation_population, historical_population = self.get_data_for_compartment_ts(compartment, ts)
            if simulation_population.empty:
                simulation_population = None
            else:
                simulation_population = simulation_population.total_population.sum()

            if historical_population.empty:
                historical_population = None
            else:
                historical_population = historical_population.total_population.sum()

            if simulation_population == 0:
                raise ValueError(f"Simulation population total for compartment {compartment} and time step {ts} "
                                 "cannot be 0 for validation")
            if historical_population == 0:
                raise ValueError(f"Historical population data for compartment {compartment} and time step {ts} "
                                 "cannot be 0 for validation")

            if simulation_population is not None and historical_population is not None:
                total_population_error.loc[(compartment, ts), 'simulation_population'] = simulation_population
                total_population_error.loc[(compartment, ts), 'historical_population'] = historical_population
                total_population_error.loc[(compartment, ts), 'percent_error'] = \
                    (simulation_population - historical_population) / historical_population

        return total_population_error.sort_index().dropna()