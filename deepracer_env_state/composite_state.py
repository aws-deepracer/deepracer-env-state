#################################################################################
#   Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.          #
#                                                                               #
#   Licensed under the Apache License, Version 2.0 (the "License").             #
#   You may not use this file except in compliance with the License.            #
#   You may obtain a copy of the License at                                     #
#                                                                               #
#       http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                               #
#   Unless required by applicable law or agreed to in writing, software         #
#   distributed under the License is distributed on an "AS IS" BASIS,           #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
#   See the License for the specific language governing permissions and         #
#   limitations under the License.                                              #
#################################################################################
"""A class for composite state"""
import logging

from typing import Dict, Any
from deepracer_env_state.state_interface import StateInterface
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData
from deepracer_env_state.agent.constants import AgentStates


class CompositeState(StateInterface):
    """
    CompositeState class
    """
    def __init__(self):
        """
        Initialize CompositeState
        """
        self._states = dict()

    def add(self, name: AgentStates, state: StateInterface) -> None:
        """
        Add a state

        Args:
            name (AgentStates): state name
            state (StateInterface): state implementing StateInterface
        """
        if name not in self._states:
            self._states[name] = state
        else:
            logging.info("[CompositeState]: state {} has already added,"
                         " so ignore.".format(name))

    def get(self, name: AgentStates) -> StateInterface:
        """
        Get a state

        Args:
            name (AgentStates): state name

        Returns:
            StateInterface: state implementing StateInterface
        """
        return self._states[name]

    def update(self, deepracer_env_data: DeepRacerEnvData) -> None:
        """
        update each state using DeepRacerEnvData instance

        Args:
            deepracer_env_data (DeepRacerEnvData): DeepRacerEnvData class instance
        """
        [state.update(deepracer_env_data) for state in self._states.values()]

    def to_dict(self) -> Dict[str, Any]:
        """
        Return CompositeState class instance in dict format

        Returns:
            Dict[str, Any]: CompositeState class instance in dict format
        """
        states_dict = dict()
        for state in self._states.values():
            states_dict.update(state.to_dict())
        return states_dict
