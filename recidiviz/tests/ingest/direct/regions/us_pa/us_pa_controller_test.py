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

"""Unit and integration tests for Pennsylvania direct ingest."""
import datetime
import json
from typing import Type

from recidiviz import IngestInfo
from recidiviz.common.constants.charge import ChargeStatus
from recidiviz.common.constants.person_characteristics import Gender, Race, Ethnicity, ResidencyStatus
from recidiviz.common.constants.state.external_id_types import US_PA_CONTROL, US_PA_SID, US_PA_PBPP
from recidiviz.common.constants.state.state_agent import StateAgentType
from recidiviz.common.constants.state.state_assessment import StateAssessmentClass, StateAssessmentType
from recidiviz.common.constants.state.state_court_case import StateCourtCaseStatus, StateCourtType
from recidiviz.common.constants.state.state_incarceration import StateIncarcerationType
from recidiviz.common.constants.state.state_person_alias import StatePersonAliasType
from recidiviz.common.constants.state.state_sentence import StateSentenceStatus
from recidiviz.ingest.direct.controllers.gcsfs_direct_ingest_controller import GcsfsDirectIngestController
from recidiviz.ingest.direct.regions.us_pa.us_pa_controller import UsPaController
from recidiviz.ingest.models.ingest_info import StatePerson, StatePersonExternalId, StatePersonRace, StateAlias, \
    StatePersonEthnicity, StateAssessment, StateSentenceGroup, StateIncarcerationSentence, StateCharge, \
    StateCourtCase, StateAgent
from recidiviz.persistence.entity.state import entities
from recidiviz.tests.ingest.direct.regions.base_state_direct_ingest_controller_tests import \
    BaseStateDirectIngestControllerTests
from recidiviz.tests.ingest.direct.regions.utils import populate_person_backedges

_STATE_CODE_UPPER = 'US_PA'


class TestUsPaController(BaseStateDirectIngestControllerTests):
    """Unit tests for each Idaho file to be ingested by the UsNdController."""

    @classmethod
    def region_code(cls) -> str:
        return _STATE_CODE_UPPER.lower()

    @classmethod
    def controller_cls(cls) -> Type[GcsfsDirectIngestController]:
        return UsPaController

    def test_populate_data_person_external_ids(self):
        expected = IngestInfo(state_people=[
            StatePerson(state_person_id='RECIDIVIZ_MASTER_STATE_ID_12345678',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='12345678', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='123456', id_type=US_PA_CONTROL),
                            StatePersonExternalId(state_person_external_id_id='123A', id_type=US_PA_PBPP),
                        ]),
            StatePerson(state_person_id='RECIDIVIZ_MASTER_STATE_ID_55554444',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='55554444', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='66665555', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='654321', id_type=US_PA_CONTROL),
                            StatePersonExternalId(state_person_external_id_id='456B', id_type=US_PA_PBPP),
                        ]),
            StatePerson(state_person_id='RECIDIVIZ_MASTER_CONTROL_NUMBER_445566',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='445566', id_type=US_PA_CONTROL),
                        ]),
            StatePerson(state_person_id='RECIDIVIZ_MASTER_STATE_ID_09876543',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='09876543', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='778899', id_type=US_PA_CONTROL),
                            StatePersonExternalId(state_person_external_id_id='889900', id_type=US_PA_CONTROL),
                            StatePersonExternalId(state_person_external_id_id='345E', id_type=US_PA_PBPP),
                            StatePersonExternalId(state_person_external_id_id='999Z', id_type=US_PA_PBPP),
                        ]),
            StatePerson(state_person_id='RECIDIVIZ_MASTER_PAROLE_NUMBER_789C',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='789C', id_type=US_PA_PBPP),
                        ]),
            StatePerson(state_person_id='RECIDIVIZ_MASTER_STATE_ID_888888888',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='888888888', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='888P', id_type=US_PA_PBPP),
                        ]),
            StatePerson(state_person_id='RECIDIVIZ_MASTER_STATE_ID_9999999',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='9999999', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='090909', id_type=US_PA_CONTROL),
                        ]),
            StatePerson(state_person_id='RECIDIVIZ_MASTER_STATE_ID_66666666',
                        state_person_external_ids=[
                            StatePersonExternalId(state_person_external_id_id='66666666', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='66666667', id_type=US_PA_SID),
                            StatePersonExternalId(state_person_external_id_id='060606', id_type=US_PA_CONTROL),
                            StatePersonExternalId(state_person_external_id_id='060607', id_type=US_PA_CONTROL),
                            StatePersonExternalId(state_person_external_id_id='666P', id_type=US_PA_PBPP),
                            StatePersonExternalId(state_person_external_id_id='777M', id_type=US_PA_PBPP),
                        ]),
        ])

        self.run_parse_file_test(expected, 'person_external_ids')

    def test_populate_data_doc_person_info(self):
        expected = IngestInfo(
            state_people=[
                StatePerson(state_person_id='123456',
                            surname='RUSSELL',
                            given_names='BERTRAND',
                            gender='MALE',
                            birthdate='19760318',
                            current_address='123 Easy Street, PITTSBURGH, PA 16161',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='123456', id_type=US_PA_CONTROL),
                            ],
                            state_person_races=[StatePersonRace(race='BLACK')],
                            state_aliases=[
                                StateAlias(
                                    surname='RUSSELL',
                                    given_names='BERTRAND',
                                    alias_type='GIVEN_NAME'
                                )
                            ],
                            state_sentence_groups=[
                                StateSentenceGroup(state_sentence_group_id='AB7413'),
                                StateSentenceGroup(state_sentence_group_id='BC8524'),
                            ]),
                StatePerson(state_person_id='654321',
                            surname='SARTRE',
                            given_names='JEAN-PAUL',
                            gender='MALE',
                            birthdate='19821002',
                            current_address='555 FLATBUSH DR, NEW YORK, NY 10031',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='654321', id_type=US_PA_CONTROL),
                            ],
                            state_person_races=[StatePersonRace(race='BLACK')],
                            state_aliases=[
                                StateAlias(
                                    surname='SARTRE',
                                    given_names='JEAN-PAUL',
                                    alias_type='GIVEN_NAME'
                                )
                            ],
                            state_sentence_groups=[
                                StateSentenceGroup(state_sentence_group_id='GF3374'),
                            ]),
                StatePerson(state_person_id='445566',
                            surname='KIERKEGAARD',
                            given_names='SOREN',
                            name_suffix='JR',
                            gender='FEMALE',
                            birthdate='19911120',
                            current_address='5000 SUNNY LANE, APT. 55D, PHILADELPHIA, PA 19129',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='445566', id_type=US_PA_CONTROL),
                            ],
                            state_person_races=[StatePersonRace(race='WHITE')],
                            state_aliases=[
                                StateAlias(
                                    surname='KIERKEGAARD',
                                    given_names='SOREN',
                                    name_suffix='JR',
                                    alias_type='GIVEN_NAME'
                                )
                            ],
                            state_sentence_groups=[
                                StateSentenceGroup(state_sentence_group_id='CJ1991'),
                            ]),
                StatePerson(state_person_id='778899',
                            surname='RAWLS',
                            given_names='JOHN',
                            gender='MALE',
                            birthdate='19890617',
                            current_address='214 HAPPY PLACE, PHILADELPHIA, PA 19129',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='778899', id_type=US_PA_CONTROL),
                            ],
                            state_person_ethnicities=[StatePersonEthnicity(ethnicity='HISPANIC')],
                            state_aliases=[
                                StateAlias(
                                    surname='RAWLS',
                                    given_names='JOHN',
                                    alias_type='GIVEN_NAME'
                                )
                            ],
                            state_sentence_groups=[
                                StateSentenceGroup(state_sentence_group_id='JE1989'),
                            ]),
            ])

        self.run_parse_file_test(expected, 'doc_person_info')

    def test_populate_data_dbo_tblInmTestScore(self):
        expected = IngestInfo(
            state_people=[
                StatePerson(state_person_id='123456',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='123456', id_type=US_PA_CONTROL),
                            ],
                            state_assessments=[
                                StateAssessment(state_assessment_id='123456-AB7413-1-1',
                                                assessment_type='CSS-M                                             ',
                                                assessment_class='SOCIAL',
                                                assessment_date='6/22/2008 13:20:54',
                                                assessment_score='19'),
                                StateAssessment(state_assessment_id='123456-BC8524-1-1',
                                                assessment_type='CSS-M                                             ',
                                                assessment_class='SOCIAL',
                                                assessment_date='1/1/2010 01:01:01',
                                                assessment_score='11'),
                                StateAssessment(state_assessment_id='123456-AB7413-2-1',
                                                assessment_type='HIQ                                               ',
                                                assessment_class='SOCIAL',
                                                assessment_date='7/12/2004 8:23:28',
                                                assessment_score='62'),
                                StateAssessment(state_assessment_id='123456-AB7413-3-3',
                                                assessment_type='LSI-R                                             ',
                                                assessment_class='RISK',
                                                assessment_date='10/3/2010 12:11:41',
                                                assessment_score='25'),
                            ]),
                StatePerson(state_person_id='654321',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='654321', id_type=US_PA_CONTROL),
                            ],
                            state_assessments=[
                                StateAssessment(state_assessment_id='654321-GF3374-1-1',
                                                assessment_type='CSS-M                                             ',
                                                assessment_class='SOCIAL',
                                                assessment_date='4/1/2003 11:42:17',
                                                assessment_score='22'),
                                StateAssessment(state_assessment_id='654321-GF3374-3-1',
                                                assessment_type='LSI-R                                             ',
                                                assessment_class='RISK',
                                                assessment_date='6/8/2004 11:07:48',
                                                assessment_score='19'),
                                StateAssessment(state_assessment_id='654321-GF3374-4-1',
                                                assessment_type='TCU                                               ',
                                                assessment_class='SUBSTANCE_ABUSE',
                                                assessment_date='1/4/2004 11:09:52',
                                                assessment_score='6'),
                                StateAssessment(state_assessment_id='654321-GF3374-5-1',
                                                assessment_type='ST99                                              ',
                                                assessment_class='SEX_OFFENSE',
                                                assessment_date='7/5/2004 15:30:59',
                                                assessment_score='4'),
                            ]),
                StatePerson(state_person_id='445566',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='445566', id_type=US_PA_CONTROL),
                            ],
                            state_assessments=[
                                StateAssessment(state_assessment_id='445566-CJ1991-2-1',
                                                assessment_type='HIQ                                               ',
                                                assessment_class='SOCIAL',
                                                assessment_date='7/28/2005 10:33:31',
                                                assessment_score='61'),
                                StateAssessment(state_assessment_id='445566-CJ1991-3-2',
                                                assessment_type='LSI-R                                             ',
                                                assessment_class='RISK',
                                                assessment_date='12/19/2016 15:21:56',
                                                assessment_score='13'),
                            ]),
                StatePerson(state_person_id='778899',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='778899', id_type=US_PA_CONTROL),
                            ],
                            state_assessments=[
                                StateAssessment(state_assessment_id='778899-JE1989-3-3',
                                                assessment_type='LSI-R                                             ',
                                                assessment_class='RISK',
                                                assessment_date='1/6/2017 18:16:56',
                                                assessment_score='14'),
                                StateAssessment(state_assessment_id='778899-JE1989-6-1',
                                                assessment_type='RST                                               ',
                                                assessment_class='RISK',
                                                assessment_date='12/8/2012 15:09:08',
                                                assessment_score='9',
                                                assessment_metadata=json.dumps({"latest_version": False})),
                                StateAssessment(state_assessment_id='778899-JE1989-6-2',
                                                assessment_type='RST                                               ',
                                                assessment_class='RISK',
                                                assessment_date='5/11/2018 15:54:06',
                                                assessment_score='7',
                                                assessment_metadata=json.dumps({"latest_version": True})),
                            ]),
            ])

        self.run_parse_file_test(expected, 'dbo_tblInmTestScore')

    def test_populate_data_dbo_Senrec(self):
        expected = IngestInfo(
            state_people=[
                StatePerson(
                    state_sentence_groups=[
                        StateSentenceGroup(
                            state_sentence_group_id="AB7413",
                            state_incarceration_sentences=[
                                StateIncarcerationSentence(
                                    state_incarceration_sentence_id="AB7413-01",
                                    status="SC", incarceration_type="S", county_code="PHI",
                                    date_imposed="20080815", start_date="20080815", completion_date="20090104",
                                    min_length="549", max_length="1095",
                                    is_life="False", is_capital_punishment="False",
                                    state_charges=[
                                        StateCharge(
                                            state_charge_id="N7825555", statute="CC3701A ",
                                            state_court_case=StateCourtCase(
                                                state_court_case_id="CP0001111 CT",
                                                judge=StateAgent(full_name="REYNOLDS, FRANK", agent_type="JUDGE")
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                        StateSentenceGroup(
                            state_sentence_group_id="GF3374",
                            state_incarceration_sentences=[
                                StateIncarcerationSentence(
                                    state_incarceration_sentence_id="GF3374-01",
                                    status="AS", incarceration_type="S", county_code="PHI",
                                    date_imposed="20080816", start_date="00000000", completion_date="00000000",
                                    min_length="4287", max_length="5113",
                                    is_life="False", is_capital_punishment="False",
                                    state_charges=[
                                        StateCharge(
                                            state_charge_id="U1196666", statute="CC3701A ",
                                            state_court_case=StateCourtCase(
                                                state_court_case_id="CP0002222 CT",
                                                judge=StateAgent(full_name="REYNOLDS, FRANK", agent_type="JUDGE")
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                        StateSentenceGroup(
                            state_sentence_group_id="CJ1991",
                            state_incarceration_sentences=[
                                StateIncarcerationSentence(
                                    state_incarceration_sentence_id="CJ1991-01",
                                    status="AS", incarceration_type="S", county_code="BUC",
                                    date_imposed="20160820", start_date="20160820", completion_date="00000000",
                                    min_length="457", max_length="914",
                                    is_life="False", is_capital_punishment="False",
                                    state_charges=[
                                        StateCharge(
                                            state_charge_id="L3947777", statute="CC6318A1",
                                            state_court_case=StateCourtCase(
                                                state_court_case_id="CP0003333 CT",
                                                judge=StateAgent(full_name="REYNOLDS, DEE", agent_type="JUDGE")
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                        StateSentenceGroup(
                            state_sentence_group_id="JE1989",
                            state_incarceration_sentences=[
                                StateIncarcerationSentence(
                                    state_incarceration_sentence_id="JE1989-01",
                                    status="AS", incarceration_type="S", county_code="BUC",
                                    date_imposed="20160820", start_date="20160820", completion_date="00000000",
                                    max_length="1095",
                                    is_life="False", is_capital_punishment="False",
                                    state_charges=[
                                        StateCharge(
                                            state_charge_id="L7858888", statute="CC3503A ",
                                            state_court_case=StateCourtCase(
                                                state_court_case_id="CP0004444 CT",
                                                judge=StateAgent(full_name="REYNOLDS, DEE", agent_type="JUDGE")
                                            )
                                        )
                                    ]
                                ),
                                StateIncarcerationSentence(
                                    state_incarceration_sentence_id="JE1989-02",
                                    status="AS", incarceration_type="S", county_code="BUC",
                                    date_imposed="20160820", start_date="20160820", completion_date="00000000",
                                    min_length="549",
                                    is_life="False", is_capital_punishment="False",
                                    state_charges=[
                                        StateCharge(
                                            state_charge_id="L7858890", statute="CC3503B ",
                                            state_court_case=StateCourtCase(
                                                state_court_case_id="CP0004445 CT",
                                                judge=StateAgent(full_name="REYNOLDS, DEE", agent_type="JUDGE")
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                    ]
                )
            ])

        self.run_parse_file_test(expected, 'dbo_Senrec')

    def test_populate_data_dbo_Offender(self):
        expected = IngestInfo(
            state_people=[
                StatePerson(state_person_id=' 123A ',
                            gender='M       ',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id=' 123A ', id_type=US_PA_PBPP),
                                StatePersonExternalId(state_person_external_id_id='12345678', id_type=US_PA_SID),
                            ],
                            state_person_races=[StatePersonRace(race='B    ')],
                            ),
                StatePerson(state_person_id='456B ',
                            gender='M       ',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='456B ', id_type=US_PA_PBPP),
                                StatePersonExternalId(state_person_external_id_id='55554444', id_type=US_PA_SID),
                            ],
                            state_person_races=[StatePersonRace(race='I    ')],
                            ),
                StatePerson(state_person_id='789C ',
                            gender='  F      ',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='789C ', id_type=US_PA_PBPP),
                            ],
                            state_person_races=[StatePersonRace(race='N    ')],
                            ),
                StatePerson(state_person_id='345E ',
                            gender='  M     ',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='345E ', id_type=US_PA_PBPP),
                                StatePersonExternalId(state_person_external_id_id='09876543', id_type=US_PA_SID),
                            ],
                            state_person_races=[StatePersonRace(race='W    ')],
                            )
            ])

        self.run_parse_file_test(expected, 'dbo_Offender')

    def test_populate_data_dbo_LSIR(self):
        expected = IngestInfo(
            state_people=[
                StatePerson(state_person_id='789C',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='789C', id_type=US_PA_PBPP),
                            ],
                            state_assessments=[
                                StateAssessment(state_assessment_id='789C-0-1',
                                                assessment_type='LSIR',
                                                assessment_class='RISK',
                                                assessment_date='01312001',
                                                assessment_score='14'),
                            ]),
                StatePerson(state_person_id='456B',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='456B', id_type=US_PA_PBPP),
                            ],
                            state_assessments=[
                                StateAssessment(state_assessment_id='456B-1-1',
                                                assessment_type='LSIR',
                                                assessment_class='RISK',
                                                assessment_date='12222005',
                                                assessment_score='23'),
                            ]),
                StatePerson(state_person_id='345E',
                            state_person_external_ids=[
                                StatePersonExternalId(state_person_external_id_id='345E', id_type=US_PA_PBPP),
                            ],
                            state_assessments=[
                                StateAssessment(state_assessment_id='345E-3-1',
                                                assessment_type='LSIR',
                                                assessment_class='RISK',
                                                assessment_date='01192006',
                                                assessment_score='30'),
                                StateAssessment(state_assessment_id='345E-3-2',
                                                assessment_type='LSIR',
                                                assessment_class='RISK',
                                                assessment_date='08032006',
                                                assessment_score='30'),
                                StateAssessment(state_assessment_id='345E-3-3',
                                                assessment_type='LSIR',
                                                assessment_class='RISK',
                                                assessment_date='01152007',
                                                assessment_score='31'),
                                StateAssessment(state_assessment_id='345E-4-1',
                                                assessment_type='LSIR',
                                                assessment_class='RISK',
                                                assessment_date='07142007',
                                                assessment_score='33'),
                            ]),
            ])

        self.run_parse_file_test(expected, 'dbo_LSIR')

    def test_run_full_ingest_all_files_specific_order(self) -> None:
        self.maxDiff = None
        ######################################
        # person_external_ids
        ######################################
        # Arrange
        person_1 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='123456', id_type=US_PA_CONTROL),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='123A', id_type=US_PA_PBPP),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='12345678', id_type=US_PA_SID),
            ]
        )

        person_2 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='654321', id_type=US_PA_CONTROL),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='456B', id_type=US_PA_PBPP),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='55554444', id_type=US_PA_SID),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='66665555', id_type=US_PA_SID),
            ]
        )

        person_3 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='445566', id_type=US_PA_CONTROL),
            ]
        )

        person_4 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='778899', id_type=US_PA_CONTROL),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='889900', id_type=US_PA_CONTROL),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='345E', id_type=US_PA_PBPP),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='999Z', id_type=US_PA_PBPP),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='09876543', id_type=US_PA_SID),
            ]
        )

        person_5 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='789C', id_type=US_PA_PBPP),
            ]
        )

        person_6 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='888888888', id_type=US_PA_SID),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='888P', id_type=US_PA_PBPP),
            ]
        )

        person_7 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='9999999', id_type=US_PA_SID),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='090909', id_type=US_PA_CONTROL),
            ]
        )

        person_8 = entities.StatePerson.new_with_defaults(
            external_ids=[
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='66666666', id_type=US_PA_SID),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='66666667', id_type=US_PA_SID),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='060606', id_type=US_PA_CONTROL),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='060607', id_type=US_PA_CONTROL),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='666P', id_type=US_PA_PBPP),
                entities.StatePersonExternalId.new_with_defaults(
                    state_code=_STATE_CODE_UPPER, external_id='777M', id_type=US_PA_PBPP),
            ]
        )

        expected_people = [person_1, person_2, person_3, person_4, person_5, person_6, person_7, person_8]

        populate_person_backedges(expected_people)

        # Act
        self._run_ingest_job_for_filename('person_external_ids.csv')

        # Assert
        self.assert_expected_db_people(expected_people)

        ######################################
        # doc_person_info
        ######################################
        # Arrange
        person_1.full_name = '{"given_names": "BERTRAND", "surname": "RUSSELL"}'
        person_1.gender = Gender.MALE
        person_1.gender_raw_text = 'MALE'
        person_1.birthdate = datetime.date(year=1976, month=3, day=18)
        person_1.birthdate_inferred_from_age = False
        person_1.current_address = '123 EASY STREET, PITTSBURGH, PA 16161'
        person_1.residency_status = ResidencyStatus.PERMANENT
        person_1.aliases = [
            entities.StatePersonAlias.new_with_defaults(
                full_name='{"given_names": "BERTRAND", "surname": "RUSSELL"}',
                state_code=_STATE_CODE_UPPER,
                alias_type=StatePersonAliasType.GIVEN_NAME,
                alias_type_raw_text='GIVEN_NAME')
        ]
        person_1.races = [
            entities.StatePersonRace.new_with_defaults(
                state_code=_STATE_CODE_UPPER, race=Race.BLACK, race_raw_text='BLACK'),
        ]

        p1_sg = entities.StateSentenceGroup.new_with_defaults(
            external_id='AB7413', state_code=_STATE_CODE_UPPER, status=StateSentenceStatus.PRESENT_WITHOUT_INFO,
            person=person_1
        )
        p1_sg2 = entities.StateSentenceGroup.new_with_defaults(
            external_id='BC8524', state_code=_STATE_CODE_UPPER, status=StateSentenceStatus.PRESENT_WITHOUT_INFO,
            person=person_1
        )

        person_1.sentence_groups.append(p1_sg)
        person_1.sentence_groups.append(p1_sg2)

        person_2.full_name = '{"given_names": "JEAN-PAUL", "surname": "SARTRE"}'
        person_2.gender = Gender.MALE
        person_2.gender_raw_text = 'MALE'
        person_2.birthdate = datetime.date(year=1982, month=10, day=2)
        person_2.birthdate_inferred_from_age = False
        person_2.current_address = '555 FLATBUSH DR, NEW YORK, NY 10031'
        person_2.residency_status = ResidencyStatus.PERMANENT
        person_2.aliases = [
            entities.StatePersonAlias.new_with_defaults(
                full_name='{"given_names": "JEAN-PAUL", "surname": "SARTRE"}',
                state_code=_STATE_CODE_UPPER,
                alias_type=StatePersonAliasType.GIVEN_NAME,
                alias_type_raw_text='GIVEN_NAME')
        ]
        person_2.races = [
            entities.StatePersonRace.new_with_defaults(
                state_code=_STATE_CODE_UPPER, race=Race.BLACK, race_raw_text='BLACK'),
        ]

        p2_sg = entities.StateSentenceGroup.new_with_defaults(
            external_id='GF3374', state_code=_STATE_CODE_UPPER, status=StateSentenceStatus.PRESENT_WITHOUT_INFO,
            person=person_2
        )
        person_2.sentence_groups.append(p2_sg)

        person_3.full_name = '{"given_names": "SOREN", "name_suffix": "JR", "surname": "KIERKEGAARD"}'
        person_3.gender = Gender.FEMALE
        person_3.gender_raw_text = 'FEMALE'
        person_3.birthdate = datetime.date(year=1991, month=11, day=20)
        person_3.birthdate_inferred_from_age = False
        person_3.current_address = '5000 SUNNY LANE, APT. 55D, PHILADELPHIA, PA 19129'
        person_3.residency_status = ResidencyStatus.PERMANENT
        person_3.aliases = [
            entities.StatePersonAlias.new_with_defaults(
                full_name='{"given_names": "SOREN", "name_suffix": "JR", "surname": "KIERKEGAARD"}',
                state_code=_STATE_CODE_UPPER,
                alias_type=StatePersonAliasType.GIVEN_NAME,
                alias_type_raw_text='GIVEN_NAME')
        ]
        person_3.races = [
            entities.StatePersonRace.new_with_defaults(
                state_code=_STATE_CODE_UPPER, race=Race.WHITE, race_raw_text='WHITE'),
        ]

        p3_sg = entities.StateSentenceGroup.new_with_defaults(
            external_id='CJ1991', state_code=_STATE_CODE_UPPER, status=StateSentenceStatus.PRESENT_WITHOUT_INFO,
            person=person_3
        )
        person_3.sentence_groups.append(p3_sg)

        person_4.full_name = '{"given_names": "JOHN", "surname": "RAWLS"}'
        person_4.gender = Gender.MALE
        person_4.gender_raw_text = 'MALE'
        person_4.birthdate = datetime.date(year=1989, month=6, day=17)
        person_4.birthdate_inferred_from_age = False
        person_4.current_address = '214 HAPPY PLACE, PHILADELPHIA, PA 19129'
        person_4.residency_status = ResidencyStatus.PERMANENT
        person_4.aliases = [
            entities.StatePersonAlias.new_with_defaults(
                full_name='{"given_names": "JOHN", "surname": "RAWLS"}',
                state_code=_STATE_CODE_UPPER,
                alias_type=StatePersonAliasType.GIVEN_NAME,
                alias_type_raw_text='GIVEN_NAME')
        ]
        person_4.ethnicities = [
            entities.StatePersonEthnicity.new_with_defaults(
                state_code=_STATE_CODE_UPPER, ethnicity=Ethnicity.HISPANIC, ethnicity_raw_text='HISPANIC'),
        ]

        p4_sg = entities.StateSentenceGroup.new_with_defaults(
            external_id='JE1989', state_code=_STATE_CODE_UPPER, status=StateSentenceStatus.PRESENT_WITHOUT_INFO,
            person=person_4
        )
        person_4.sentence_groups.append(p4_sg)

        populate_person_backedges(expected_people)

        # Act
        self._run_ingest_job_for_filename('doc_person_info.csv')

        # Assert
        self.assert_expected_db_people(expected_people)

        ######################################
        # dbo_tblInmTestScore
        ######################################

        person_1_doc_assessments = [
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.SOCIAL, assessment_class_raw_text='SOCIAL',
                assessment_type=StateAssessmentType.CSSM, assessment_type_raw_text='CSS-M',
                assessment_score=19, assessment_date=datetime.date(year=2008, month=6, day=22),
                external_id='123456-AB7413-1-1', state_code=_STATE_CODE_UPPER, person=person_1),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.SOCIAL, assessment_class_raw_text='SOCIAL',
                assessment_type=StateAssessmentType.CSSM, assessment_type_raw_text='CSS-M',
                assessment_score=11, assessment_date=datetime.date(year=2010, month=1, day=1),
                external_id='123456-BC8524-1-1', state_code=_STATE_CODE_UPPER, person=person_1),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.SOCIAL, assessment_class_raw_text='SOCIAL',
                assessment_type=StateAssessmentType.HIQ, assessment_type_raw_text='HIQ',
                assessment_score=62, assessment_date=datetime.date(year=2004, month=7, day=12),
                external_id='123456-AB7413-2-1', state_code=_STATE_CODE_UPPER, person=person_1),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSI-R',
                assessment_score=25, assessment_date=datetime.date(year=2010, month=10, day=3),
                external_id='123456-AB7413-3-3', state_code=_STATE_CODE_UPPER, person=person_1),
        ]
        person_1.assessments = person_1_doc_assessments

        person_2_doc_assessments = [
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.SOCIAL, assessment_class_raw_text='SOCIAL',
                assessment_type=StateAssessmentType.CSSM, assessment_type_raw_text='CSS-M',
                assessment_score=22, assessment_date=datetime.date(year=2003, month=4, day=1),
                external_id='654321-GF3374-1-1', state_code=_STATE_CODE_UPPER, person=person_2),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSI-R',
                assessment_score=19, assessment_date=datetime.date(year=2004, month=6, day=8),
                external_id='654321-GF3374-3-1', state_code=_STATE_CODE_UPPER, person=person_2),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.SUBSTANCE_ABUSE, assessment_class_raw_text='SUBSTANCE_ABUSE',
                assessment_type=StateAssessmentType.TCU_DRUG_SCREEN, assessment_type_raw_text='TCU',
                assessment_score=6, assessment_date=datetime.date(year=2004, month=1, day=4),
                external_id='654321-GF3374-4-1', state_code=_STATE_CODE_UPPER, person=person_2),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.SEX_OFFENSE, assessment_class_raw_text='SEX_OFFENSE',
                assessment_type=StateAssessmentType.STATIC_99, assessment_type_raw_text='ST99',
                assessment_score=4, assessment_date=datetime.date(year=2004, month=7, day=5),
                external_id='654321-GF3374-5-1', state_code=_STATE_CODE_UPPER, person=person_2),
        ]
        person_2.assessments = person_2_doc_assessments

        person_3_doc_assessments = [
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.SOCIAL, assessment_class_raw_text='SOCIAL',
                assessment_type=StateAssessmentType.HIQ, assessment_type_raw_text='HIQ',
                assessment_score=61, assessment_date=datetime.date(year=2005, month=7, day=28),
                external_id='445566-CJ1991-2-1', state_code=_STATE_CODE_UPPER, person=person_3),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSI-R',
                assessment_score=13, assessment_date=datetime.date(year=2016, month=12, day=19),
                external_id='445566-CJ1991-3-2', state_code=_STATE_CODE_UPPER, person=person_3),
        ]
        person_3.assessments = person_3_doc_assessments

        person_4_doc_assessments = [
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSI-R',
                assessment_score=14, assessment_date=datetime.date(year=2017, month=1, day=6),
                external_id='778899-JE1989-3-3', state_code=_STATE_CODE_UPPER, person=person_4),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.PA_RST, assessment_type_raw_text='RST',
                assessment_score=9, assessment_date=datetime.date(year=2012, month=12, day=8),
                assessment_metadata='{"LATEST_VERSION": FALSE}',
                external_id='778899-JE1989-6-1', state_code=_STATE_CODE_UPPER, person=person_4),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.PA_RST, assessment_type_raw_text='RST',
                assessment_score=7, assessment_date=datetime.date(year=2018, month=5, day=11),
                assessment_metadata='{"LATEST_VERSION": TRUE}',
                external_id='778899-JE1989-6-2', state_code=_STATE_CODE_UPPER, person=person_4),
        ]
        person_4.assessments = person_4_doc_assessments

        populate_person_backedges(expected_people)

        # Act
        self._run_ingest_job_for_filename('dbo_tblInmTestScore.csv')

        # Assert
        self.assert_expected_db_people(expected_people)

        ######################################
        # dbo_Senrec
        ######################################

        # Person 1 updates
        p1_is = entities.StateIncarcerationSentence.new_with_defaults(
            external_id="AB7413-01", state_code=_STATE_CODE_UPPER, county_code="PHI",
            status=StateSentenceStatus.COMPLETED, status_raw_text="SC",
            incarceration_type=StateIncarcerationType.STATE_PRISON, incarceration_type_raw_text="S",
            date_imposed=datetime.date(year=2008, month=8, day=15),
            start_date=datetime.date(year=2008, month=8, day=15),
            completion_date=datetime.date(year=2009, month=1, day=4),
            min_length_days=549, max_length_days=1095, is_life=False, is_capital_punishment=False,
            person=person_1, sentence_group=p1_sg
        )
        p1_sg.incarceration_sentences.append(p1_is)

        p1_is_charge = entities.StateCharge.new_with_defaults(
            external_id="N7825555", statute="CC3701A", status=ChargeStatus.PRESENT_WITHOUT_INFO,
            state_code=_STATE_CODE_UPPER,
            person=person_1, incarceration_sentences=[p1_is]
        )
        p1_is.charges.append(p1_is_charge)

        p1_is_charge_case = entities.StateCourtCase.new_with_defaults(
            external_id="CP0001111 CT", state_code=_STATE_CODE_UPPER,
            status=StateCourtCaseStatus.PRESENT_WITHOUT_INFO,
            court_type=StateCourtType.PRESENT_WITHOUT_INFO,
            judge=entities.StateAgent.new_with_defaults(
                full_name='{"full_name": "REYNOLDS, FRANK"}',
                agent_type=StateAgentType.JUDGE, agent_type_raw_text="JUDGE",
                state_code=_STATE_CODE_UPPER
            ),
            person=person_1, charges=[p1_is_charge]
        )
        p1_is_charge.court_case = p1_is_charge_case

        # Person 2 updates
        p2_is = entities.StateIncarcerationSentence.new_with_defaults(
            external_id="GF3374-01", state_code=_STATE_CODE_UPPER, county_code="PHI",
            status=StateSentenceStatus.SERVING, status_raw_text="AS",
            incarceration_type=StateIncarcerationType.STATE_PRISON, incarceration_type_raw_text="S",
            date_imposed=datetime.date(year=2008, month=8, day=16),
            min_length_days=4287, max_length_days=5113, is_life=False, is_capital_punishment=False,
            person=person_2, sentence_group=p2_sg
        )
        p2_sg.incarceration_sentences.append(p2_is)

        p2_is_charge = entities.StateCharge.new_with_defaults(
            external_id="U1196666", statute="CC3701A", status=ChargeStatus.PRESENT_WITHOUT_INFO,
            state_code=_STATE_CODE_UPPER,
            person=person_2, incarceration_sentences=[p2_is]
        )
        p2_is.charges.append(p2_is_charge)

        p2_is_charge_case = entities.StateCourtCase.new_with_defaults(
            external_id="CP0002222 CT", state_code=_STATE_CODE_UPPER,
            status=StateCourtCaseStatus.PRESENT_WITHOUT_INFO,
            court_type=StateCourtType.PRESENT_WITHOUT_INFO,
            judge=entities.StateAgent.new_with_defaults(
                full_name='{"full_name": "REYNOLDS, FRANK"}',
                agent_type=StateAgentType.JUDGE, agent_type_raw_text="JUDGE",
                state_code=_STATE_CODE_UPPER
            ),
            person=person_2, charges=[p2_is_charge]
        )
        p2_is_charge.court_case = p2_is_charge_case

        # Person 3 updates
        p3_is = entities.StateIncarcerationSentence.new_with_defaults(
            external_id="CJ1991-01", state_code=_STATE_CODE_UPPER, county_code="BUC",
            status=StateSentenceStatus.SERVING, status_raw_text="AS",
            incarceration_type=StateIncarcerationType.STATE_PRISON, incarceration_type_raw_text="S",
            date_imposed=datetime.date(year=2016, month=8, day=20),
            start_date=datetime.date(year=2016, month=8, day=20),
            min_length_days=457, max_length_days=914, is_life=False, is_capital_punishment=False,
            person=person_3, sentence_group=p3_sg
        )
        p3_sg.incarceration_sentences.append(p3_is)

        p3_is_charge = entities.StateCharge.new_with_defaults(
            external_id="L3947777", statute="CC6318A1", status=ChargeStatus.PRESENT_WITHOUT_INFO,
            state_code=_STATE_CODE_UPPER,
            person=person_3, incarceration_sentences=[p3_is]
        )
        p3_is.charges.append(p3_is_charge)

        p3_is_charge_case = entities.StateCourtCase.new_with_defaults(
            external_id="CP0003333 CT", state_code=_STATE_CODE_UPPER,
            status=StateCourtCaseStatus.PRESENT_WITHOUT_INFO,
            court_type=StateCourtType.PRESENT_WITHOUT_INFO,
            judge=entities.StateAgent.new_with_defaults(
                full_name='{"full_name": "REYNOLDS, DEE"}',
                agent_type=StateAgentType.JUDGE, agent_type_raw_text="JUDGE",
                state_code=_STATE_CODE_UPPER
            ),
            person=person_3, charges=[p3_is_charge]
        )
        p3_is_charge.court_case = p3_is_charge_case

        # Person 4 updates
        p4_is_1 = entities.StateIncarcerationSentence.new_with_defaults(
            external_id="JE1989-01", state_code=_STATE_CODE_UPPER, county_code="BUC",
            status=StateSentenceStatus.SERVING, status_raw_text="AS",
            incarceration_type=StateIncarcerationType.STATE_PRISON, incarceration_type_raw_text="S",
            date_imposed=datetime.date(year=2016, month=8, day=20),
            start_date=datetime.date(year=2016, month=8, day=20),
            max_length_days=1095, is_life=False, is_capital_punishment=False,
            person=person_4, sentence_group=p4_sg
        )
        p4_is_2 = entities.StateIncarcerationSentence.new_with_defaults(
            external_id="JE1989-02", state_code=_STATE_CODE_UPPER, county_code="BUC",
            status=StateSentenceStatus.SERVING, status_raw_text="AS",
            incarceration_type=StateIncarcerationType.STATE_PRISON, incarceration_type_raw_text="S",
            date_imposed=datetime.date(year=2016, month=8, day=20),
            start_date=datetime.date(year=2016, month=8, day=20),
            min_length_days=549, is_life=False, is_capital_punishment=False,
            person=person_4, sentence_group=p4_sg
        )
        p4_sg.incarceration_sentences.extend([p4_is_1, p4_is_2])

        p4_is_1_charge = entities.StateCharge.new_with_defaults(
            external_id="L7858888", statute="CC3503A", status=ChargeStatus.PRESENT_WITHOUT_INFO,
            state_code=_STATE_CODE_UPPER,
            person=person_4, incarceration_sentences=[p4_is_1]
        )
        p4_is_1.charges.append(p4_is_1_charge)

        p4_is_2_charge = entities.StateCharge.new_with_defaults(
            external_id="L7858890", statute="CC3503B", status=ChargeStatus.PRESENT_WITHOUT_INFO,
            state_code=_STATE_CODE_UPPER,
            person=person_4, incarceration_sentences=[p4_is_2]
        )
        p4_is_2.charges.append(p4_is_2_charge)

        p4_is_1_charge_case = entities.StateCourtCase.new_with_defaults(
            external_id="CP0004444 CT", state_code=_STATE_CODE_UPPER,
            status=StateCourtCaseStatus.PRESENT_WITHOUT_INFO, court_type=StateCourtType.PRESENT_WITHOUT_INFO,
            judge=entities.StateAgent.new_with_defaults(
                full_name='{"full_name": "REYNOLDS, DEE"}',
                agent_type=StateAgentType.JUDGE, agent_type_raw_text="JUDGE", state_code=_STATE_CODE_UPPER
            ),
            person=person_4, charges=[p4_is_1_charge]
        )
        p4_is_1_charge.court_case = p4_is_1_charge_case

        p4_is_2_charge_case = entities.StateCourtCase.new_with_defaults(
            external_id="CP0004445 CT", state_code=_STATE_CODE_UPPER,
            status=StateCourtCaseStatus.PRESENT_WITHOUT_INFO, court_type=StateCourtType.PRESENT_WITHOUT_INFO,
            judge=entities.StateAgent.new_with_defaults(
                full_name='{"full_name": "REYNOLDS, DEE"}',
                agent_type=StateAgentType.JUDGE, agent_type_raw_text="JUDGE", state_code=_STATE_CODE_UPPER
            ),
            person=person_4, charges=[p4_is_2_charge]
        )
        p4_is_2_charge.court_case = p4_is_2_charge_case

        populate_person_backedges(expected_people)

        # Act
        self._run_ingest_job_for_filename('dbo_Senrec.csv')

        # Assert
        self.assert_expected_db_people(expected_people)

        ######################################
        # dbo_Offender
        ######################################
        # Arrange
        person_1.gender_raw_text = 'M'
        person_1.races[0].race_raw_text = 'B'

        person_2.gender_raw_text = 'M'
        person_2.races.append(entities.StatePersonRace.new_with_defaults(
            state_code=_STATE_CODE_UPPER, race=Race.AMERICAN_INDIAN_ALASKAN_NATIVE, race_raw_text='I'
        ))

        person_4.gender_raw_text = 'M'
        person_4.races = [entities.StatePersonRace.new_with_defaults(
            state_code=_STATE_CODE_UPPER, race=Race.WHITE, race_raw_text='W'
        )]

        person_5.gender = Gender.FEMALE
        person_5.gender_raw_text = 'F'
        person_5.races = [
            entities.StatePersonRace.new_with_defaults(
                state_code=_STATE_CODE_UPPER, race=Race.OTHER, race_raw_text='N'),
        ]

        populate_person_backedges(expected_people)

        # Act
        self._run_ingest_job_for_filename('dbo_Offender.csv')

        # Assert
        self.assert_expected_db_people(expected_people)

        ######################################
        # dbo_LSIR
        ######################################
        # Arrange
        person_2_pbpp_assessments = [
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSIR',
                assessment_score=23, assessment_date=datetime.date(year=2005, month=12, day=22),
                external_id='456B-1-1', state_code=_STATE_CODE_UPPER, person=person_2),
        ]
        person_2.assessments.extend(person_2_pbpp_assessments)

        person_4_pbpp_assessments = [
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSIR',
                assessment_score=30, assessment_date=datetime.date(year=2006, month=1, day=19),
                external_id='345E-3-1', state_code=_STATE_CODE_UPPER, person=person_4),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSIR',
                assessment_score=30, assessment_date=datetime.date(year=2006, month=8, day=3),
                external_id='345E-3-2', state_code=_STATE_CODE_UPPER, person=person_4),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSIR',
                assessment_score=31, assessment_date=datetime.date(year=2007, month=1, day=15),
                external_id='345E-3-3', state_code=_STATE_CODE_UPPER, person=person_4),
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSIR',
                assessment_score=33, assessment_date=datetime.date(year=2007, month=7, day=14),
                external_id='345E-4-1', state_code=_STATE_CODE_UPPER, person=person_4),
        ]
        person_4.assessments.extend(person_4_pbpp_assessments)

        person_5_pbpp_assessments = [
            entities.StateAssessment.new_with_defaults(
                assessment_class=StateAssessmentClass.RISK, assessment_class_raw_text='RISK',
                assessment_type=StateAssessmentType.LSIR, assessment_type_raw_text='LSIR',
                assessment_score=14, assessment_date=datetime.date(year=2001, month=1, day=31),
                external_id='789C-0-1', state_code=_STATE_CODE_UPPER, person=person_5),
        ]
        person_5.assessments.extend(person_5_pbpp_assessments)

        populate_person_backedges(expected_people)

        # Act
        self._run_ingest_job_for_filename('dbo_LSIR.csv')

        # Assert
        self.assert_expected_db_people(expected_people)

        ######################################
        # Full Rerun for Idempotence
        ######################################

        # Rerun for sanity
        self._do_ingest_job_rerun_for_tags(self.controller.get_file_tag_rank_list())

        self.assert_expected_db_people(expected_people)
