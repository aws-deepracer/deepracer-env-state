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
"""A class for pose state"""
import numpy as np

from typing import Dict, Any
from deepracer_env_state.state_interface import StateInterface
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData
from deepracer_env_state.agent.utils import quaternion_to_euler
from deepracer_env_state.agent.utils import rotate
from deepracer_env_state.agent.constants import RELATIVE_POSITION_OF_FRONT_OF_CAR


class Pose(StateInterface):
    """
    Pose Class
    """
    def __init__(self, name: str):
        """
        Initialize Pose

        Args:
            name (str): agent name
        """
        self._name = name
        # posiiton: x, y, z for center of agent
        self._position = (0.0, 0.0, 0.0)
        # euler angle: roll, pitch, yaw
        self._euler_angle = (0.0, 0.0, 0.0)
        # position: x. y, z for front of agent
        self._front_of_car_position = np.array(self._position) + np.array(
            rotate(RELATIVE_POSITION_OF_FRONT_OF_CAR,
                   (0.0, 0.0, 0.0, 1)))

    @property
    def x(self) -> float:
        """
        Return position x of front of agent in meter

        Returns:
            float: position x
        """
        return self._front_of_car_position[0]

    @property
    def y(self) -> float:
        """
        Return position y of front of agent in meter

        Returns:
            float: position y
        """
        return self._front_of_car_position[1]

    @property
    def z(self) -> float:
        """
        Return position z of front of agent in meter

        Returns:
            float: position z
        """
        return self._front_of_car_position[2]

    @property
    def roll(self) -> float:
        """
        Return euler roll in radian

        Returns:
            float: euler roll
        """
        return self._euler_angle[0]

    @property
    def pitch(self) -> float:
        """
        Return euler pitch in radian

        Returns:
            float: euler pitch
        """
        return self._euler_angle[1]

    @property
    def yaw(self) -> float:
        """
        Return euler yaw in radian

        Returns:
            float: euler yaw
        """
        return self._euler_angle[2]

    def update(self, deepracer_env_data: DeepRacerEnvData) -> None:
        """
        Update the internal state information

        Args:
            deepracer_env_data (DeepRacerEnvData): DeepRacerEnvData class instance

        """
        orientation = deepracer_env_data.orientation[self._name]
        self._position = deepracer_env_data.position[self._name]
        self._front_of_car_position = np.array(self._position) + np.array(
            rotate(RELATIVE_POSITION_OF_FRONT_OF_CAR,
                   orientation))
        self._euler_angle = quaternion_to_euler(
            orientation[0],
            orientation[1],
            orientation[2],
            orientation[3])

    def to_dict(self) -> Dict[str, Any]:
        """
        Return all internal state as a dict format

        Returns:
            Dict[str, Any]: internal state as a dict format
        """
        return {"x": self.x,
                "y": self.y,
                "z": self.z,
                "roll": self.roll,
                "pitch": self.pitch,
                "yaw": self.yaw}
