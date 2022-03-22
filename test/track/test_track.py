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
from unittest import TestCase
from unittest.mock import MagicMock

from deepracer_env_state.track.track import Track
from deepracer_track_geometry import (
    TrackGeometry,
    TrackDirection)
from deepracer_env import DEFAULT_TRACK


class TrackTest(TestCase):
    def setUp(self) -> None:
        self.track = Track()

    def is_clockwise_false(self) -> None:
        self.assertFalse(self.track.is_clockwise)

    def is_clockwise_true(self) -> None:
        self.track._track_geometry = TrackGeometry(
            track_name=DEFAULT_TRACK,
            finish_line=0.0,
            direction=TrackDirection.CLOCKWISE)
        self.assertFalse(self.track.is_clockwise)

    def test_track_length(self) -> None:
        self.assertEqual(self.track.track_length,
                         self.track._track_geometry.track_center_line.length)

    def test_waypoints(self) -> None:
        print(self.track.waypoints)
        self.assertEqual(self.track.waypoints,
                         list(self.track._track_geometry.track_center_line.coords))

    def test_update(self) -> None:
        env_data_mock = MagicMock()
        env_data_mock.track_geometry = "track_geometry"
        self.track.update(env_data_mock)
        self.assertEqual(self.track._track_geometry, "track_geometry")

    def test_to_dict(self) -> None:
        self.assertEqual(
            self.track.to_dict(),
            {"is_clockwise": self.track.is_clockwise,
             "track_length": self.track.track_length,
             "waypoints": self.track.waypoints})
