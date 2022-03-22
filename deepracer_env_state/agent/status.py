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
"""A class for status state"""
import numpy as np

from typing import Callable, Any, Optional
from shapely.geometry import Point
from typing import Dict, Tuple
from deepracer_env_state.state_interface import StateInterface
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData
from deepracer_env_state.agent.constants import (
    RELATIVE_POSITION_OF_FOUR_WHEELS,
    RELATIVE_POSITION_OF_FRONT_OF_CAR)
from deepracer_env_state.agent.utils import rotate
from deepracer_track_geometry import (
    TrackGeometry,
    TrackRegion,
    TrackDirection)
from deepracer_env import DEFAULT_TRACK


class Status(StateInterface):
    """
    Status Class
    """
    def __init__(self, name: str,
                 track_geometry: Optional[TrackGeometry] = None):
        """
        Initialize Status

        Args:
            name (str): agent name
            track_geometry (Optional[TrackGeometry]): TrackGeometry instance
        """
        self._name = name
        self._steps = 0
        self._done = False
        self._track_geometry = track_geometry or TrackGeometry(DEFAULT_TRACK)
        # posiiton: x, y, z for center of agent
        self._position = (0.0, 0.0, 0.0)
        # quaternion: x, y, z, w
        self._orientation = (0.0, 0.0, 0.0, 1.0)
        # position: x. y, z for front of agent
        self._front_of_car_point = Point(np.array(self._position) + np.array(
            rotate(RELATIVE_POSITION_OF_FRONT_OF_CAR,
                   self._orientation)))
        self._is_offtrack = False
        self._progress = 0

    @property
    def all_wheels_on_track(self) -> bool:
        """
        Return all_wheels_on_track status

        Returns:
            bool: True if all wheels are on track and False if any wheel is offtrack
        """
        return self._is_wheels_on_track(condition=all)

    @property
    def closest_waypoints(self) -> Tuple[int, int]:
        """
        Return closest_waypoints status

        Returns:
            Tuple[int, int]: indices of the two nearest certer lane waypoints
                             based on the current position (front of car)
        """
        return self._track_geometry.get_closest_waypoint_indices(
            self._track_geometry.get_ndist_from_point(self._front_of_car_point))

    @property
    def distance_from_center(self) -> float:
        """
        Return distance_from_center status

        Returns:
            float: distance from current position (front of car) to track center lane
        """
        return self._front_of_car_point.distance(
            self._track_geometry.track_center_line)

    @property
    def is_offtrack(self) -> bool:
        """
        Return is_offtrack status

        Returns:
            bool: True if any wheel is on track and False if all wheels are offtrack
        """
        return self._is_offtrack

    @property
    def progress(self) -> float:
        """
        Return progress status

        Returns:
            float: progress status in range [0, 100.0] based on the current
                   position (front of car)
        """
        return self._progress

    @property
    def steps(self) -> int:
        """
        Return steps status

        Returns:
            int: steps completed since episode starts
        """
        return self._steps

    @property
    def track_width(self) -> float:
        """
        Return current progress (front of car) track_width status

        Returns:
            float: current progress (front of car) track width
        """
        # get ndist based on center line by project front of car point to center line
        ndist = self._track_geometry.get_ndist_from_point(self._front_of_car_point)
        # get center line point based on ndist
        center_point = self._track_geometry.track_center_line.interpolate(
            ndist,
            normalized=True)
        # get inner border line point by project and interpolate center point
        inner_point = self._track_geometry.inner_border_line.interpolate(
            self._track_geometry.inner_border_line.project(center_point),
            normalized=False)
        # get outer border line point by project and interpolate center point
        outer_point = self._track_geometry.outer_border_line.interpolate(
            self._track_geometry.outer_border_line.project(center_point),
            normalized=False)
        # return distance between inner and outer point as current track width distance
        return inner_point.distance(outer_point)

    @property
    def is_left_of_center(self) -> bool:
        """
        Return current point (front of car) is to the left of track

        inner_lane | cw | is_left_of_center
             T     | T  | F
             T     | F  | T
             F     | T  | T
             F     | F  | F

        Returns:
            bool: Return True is to the left of center and False to the right
        """
        region = self._track_geometry.get_region_on_track(self._front_of_car_point)
        is_inner = region in [TrackRegion.INNER_LANE, TrackRegion.INNER_OFFTRACK]
        is_clockwise = self._track_geometry.direction == TrackDirection.CLOCKWISE
        return is_inner ^ is_clockwise

    def _is_wheels_on_track(self, condition: Callable[[bool], bool] = all) -> bool:
        """
        Return bool regarding whether wheels on track based on condition

        Args:
            condition Callable[list[List[bool]], bool]: any for any wheel on track,
                                                  all for all wheel on track

        Returns:
            bool: True if on track and False otherwise based on condition
        """
        wheel_points = [
            Point(np.array(self._position) + np.array(rotate(wheel_relative_position,
                                                             self._orientation)))
            for wheel_relative_position in RELATIVE_POSITION_OF_FOUR_WHEELS]
        return condition([self._track_geometry.is_on_track(wheel_point)
                          for wheel_point in wheel_points])

    def update(self, deepracer_env_data: DeepRacerEnvData) -> None:
        """
        Update the internal state information

        Args:
            deepracer_env_data (DeepRacerEnvData): DeepRacerEnvData class instance

        """
        if self._done:
            self._steps = 0
        self._steps += 1
        self._position = deepracer_env_data.position[self._name]
        self._orientation = deepracer_env_data.orientation[self._name]
        self._done = deepracer_env_data.done[self._name]
        self._track_geometry = deepracer_env_data.track_geometry
        self._front_of_car_point = Point(np.array(self._position) + np.array(
            rotate(RELATIVE_POSITION_OF_FRONT_OF_CAR,
                   self._orientation)))
        self._is_offtrack = deepracer_env_data.is_offtrack[self._name]
        self._progress = deepracer_env_data.progress[self._name]

    def to_dict(self) -> Dict[str, Any]:
        """
        Return all internal state as a dict format

        Returns:
            Dict[str, Any]: internal state as a dict format
        """
        return {"all_wheels_on_track": self.all_wheels_on_track,
                "closest_waypoints": self.closest_waypoints,
                "distance_from_center": self.distance_from_center,
                "is_offtrack": self.is_offtrack,
                "progress": self.progress,
                "steps": self.steps,
                "track_width": self.track_width,
                "is_left_of_center": self.is_left_of_center}
