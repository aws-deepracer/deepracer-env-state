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
"""A class for action state"""
from typing import Dict, Any
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData
from deepracer_env_state.state_interface import StateInterface


class Action(StateInterface):
    """
    Action class
    """
    def __init__(self, name: str):
        """
        Initialize Action

        Args:
            name (str): agent name
        """
        self._name = name
        self._steering_angle = 0.0
        self._speed = 0.0

    @property
    def steering_angle(self) -> float:
        """
        Return action steering_angle in degree

        Returns:
            float: action steering_angle
        """
        return self._steering_angle

    @property
    def speed(self) -> float:
        """
        Return action speed in meter/second

        Returns:
            float: action speed
        """
        return self._speed

    def update(self, deepracer_env_data: DeepRacerEnvData) -> None:
        """
        Update the internal state information

        Args:
            deepracer_env_data (DeepRacerEnvData): DeepRacerEnvData class instance

        """
        action = deepracer_env_data.action[self._name]
        self._steering_angle = action[0]
        self._speed = action[1]

    def to_dict(self) -> Dict[str, Any]:
        """
        Return all internal state as a dict format

        Returns:
            Dict[str, Any]: internal state as a dict format
        """
        return {"speed": self.speed,
                "steering_angle": self.steering_angle}
