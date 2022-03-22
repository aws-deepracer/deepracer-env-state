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
"""A class for track state"""
from typing import Dict, List, Tuple, Optional, Any

from deepracer_env_state.state_interface import StateInterface
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData
from deepracer_track_geometry import (
    TrackGeometry,
    TrackDirection)
from deepracer_env import DEFAULT_TRACK


class Track(StateInterface):
    """
    Track class
    """
    def __init__(self, track_geometry: Optional[TrackGeometry] = None):
        """
        Initialize Track

        Args:
            track_geometry (Optional[TrackGeometry]): TrackGeometry instance
        """
        self._track_geometry = track_geometry or TrackGeometry(DEFAULT_TRACK)

    @property
    def is_clockwise(self) -> bool:
        """
        Track is_clockwise

        Returns:
            bool: True if Track direction is clockwise and False otherwise
        """
        return self._track_geometry.direction == TrackDirection.CLOCKWISE

    @property
    def track_length(self) -> float:
        """
        Track length

        Returns:
            float: track length
        """
        return self._track_geometry.length

    @property
    def waypoints(self) -> List[Tuple[float, float]]:
        """
        Track center line waypoints

        Return:
            List[Tuple[float, float]]
        """
        return list(self._track_geometry.track_center_line.coords)

    def update(self, deepracer_env_data: DeepRacerEnvData) -> None:
        """
        Update the internal state information

        Args:
            deepracer_env_data (DeepRacerEnvData): DeepRacerEnvData class instance

        """
        self._track_geometry = deepracer_env_data.track_geometry

    def to_dict(self) -> Dict[str, Any]:
        """
        Return all internal state as a dict format

        Returns:
            Dict[str, Any]: internal state as a dict format
        """
        return {"is_clockwise": self.is_clockwise,
                "track_length": self.track_length,
                "waypoints": self.waypoints}
