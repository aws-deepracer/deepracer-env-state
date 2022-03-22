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
from unittest.mock import patch

from shapely.geometry import Point
from deepracer_env_state.agent.status import Status
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData
from deepracer_env_state.agent.constants import RELATIVE_POSITION_OF_FRONT_OF_CAR
from deepracer_track_geometry import (
    TrackGeometry,
    TrackDirection)


class StatusTest(TestCase):
    def setUp(self) -> None:
        self.name = "agent0"
        self.status = Status(self.name)
        self.status._track_geometry = TrackGeometry("monaco")

    def test_init(self) -> None:
        self.assertEqual(self.status._name, self.name)
        self.assertEqual(self.status._steps, 0)
        self.assertEqual(self.status._position, (0.0, 0.0, 0.0))
        self.assertEqual(
            self.status._front_of_car_point.coords[:][0],
            RELATIVE_POSITION_OF_FRONT_OF_CAR)
        self.assertEqual(self.status._orientation, (0.0, 0.0, 0.0, 1.0))
        self.assertEqual(self.status._is_offtrack, False)
        self.assertEqual(self.status._progress, 0)

    @patch.object(Status, "_is_wheels_on_track")
    def test_all_wheels_on_track(self, is_wheels_on_track_mock) -> None:
        is_wheels_on_track_mock.return_value = True
        self.assertTrue(self.status.all_wheels_on_track)
        is_wheels_on_track_mock.assert_called_once_with(condition=all)

    def test_closest_waypoints(self) -> None:
        self.status._front_of_car_point = \
            self.status._track_geometry.get_point_from_ndist(0.9)
        self.assertEqual(self.status.closest_waypoints, (211, 212))

    def test_distance_from_center(self) -> None:
        self.status._front_of_car_point = \
            Point(self.status._track_geometry.get_point_from_ndist(0.9))
        self.assertAlmostEqual(self.status.distance_from_center, 0)

    def test_is_offtrack(self) -> None:
        self.status._is_offtrack = True
        self.assertTrue(self.status.is_offtrack)

    def test_progress(self) -> None:
        self.status._progress = 90
        self.assertEqual(self.status.progress, 90)

    def test_steps(self) -> None:
        self.status._steps = 100
        self.assertEqual(self.status.steps, 100)

    def test_track_width(self) -> None:
        self.status._front_of_car_point = \
            Point(self.status._track_geometry.get_point_from_ndist(0.1))
        self.assertAlmostEqual(self.status.track_width, 1.4225172646452378)

        self.status._front_of_car_point = \
            Point(self.status._track_geometry.get_point_from_ndist(0.3))
        self.assertAlmostEqual(self.status.track_width, 1.4422976314751388)

        self.status._front_of_car_point = \
            Point(self.status._track_geometry.get_point_from_ndist(0.5))
        self.assertAlmostEqual(self.status.track_width, 1.437603192260296)

        self.status._front_of_car_point = \
            Point(self.status._track_geometry.get_point_from_ndist(0.7))
        self.assertAlmostEqual(self.status.track_width, 1.4514809963425641)

        self.status._front_of_car_point = \
            Point(self.status._track_geometry.get_point_from_ndist(0.9))
        self.assertAlmostEqual(self.status.track_width, 1.447689103441436)

    def test_is_left_of_center(self) -> None:
        # inner lane and cw
        self.status._front_of_car_point = Point(-6.75, 1)
        self.status._track_geometry = TrackGeometry(
            "monaco", 0.0, TrackDirection.CLOCKWISE)
        self.assertFalse(self.status.is_left_of_center)

        # inner lane and ccw
        self.status._front_of_car_point = Point(-6.75, 1)
        self.status._track_geometry = TrackGeometry(
            "monaco", 0.0, TrackDirection.COUNTER_CLOCKWISE)
        self.assertTrue(self.status.is_left_of_center)

        # outer lane and cw
        self.status._track_geometry = TrackGeometry(
            "monaco", 0.0, TrackDirection.CLOCKWISE)
        self.status._front_of_car_point = Point(-7.5, 1)
        self.assertTrue(self.status.is_left_of_center)

        # outer lane and ccw
        self.status._track_geometry = TrackGeometry(
            "monaco", 0.0, TrackDirection.COUNTER_CLOCKWISE)
        self.status._front_of_car_point = Point(-7.5, 1)
        self.assertFalse(self.status.is_left_of_center)

    def test_is_wheels_on_track_all(self) -> None:
        # all wheels on track
        self.status._position = (-7.25, 0.9, 0)
        self.assertTrue(self.status._is_wheels_on_track(all))

        # one wheel off track
        self.status._position = (-7.75, 1.42, 0)
        self.assertFalse(self.status._is_wheels_on_track(all))

        # all wheel off track
        self.status._position = (-8.75, 1.2, 0)
        self.assertFalse(self.status._is_wheels_on_track(all))

    def test_is_wheels_on_track_any(self) -> None:
        # all wheels on track
        self.status._position = (-7.25, 0.9, 0)
        self.assertTrue(self.status._is_wheels_on_track(any))

        # one wheel off track
        self.status._position = (-7.75, 1.42, 0)
        self.assertTrue(self.status._is_wheels_on_track(any))

        # all wheel off track
        self.status._position = (-8.75, 1.2, 0)
        self.assertFalse(self.status._is_wheels_on_track(any))

    def test_update_not_done(self) -> None:
        self.status._orientation = (1, 1, 1, 1)
        deepracer_env_data = DeepRacerEnvData(
            {self.name: False},
            "test",
            {self.name: {"position": (1.0, 2.0, 3.0),
                         "orientation": (0, 0, 0, 1),
                         "is_offtrack": True,
                         "progress": 10}},
            "track_geometry")
        self.status.update(deepracer_env_data)
        self.assertEqual(self.status._steps, 1)
        self.assertEqual(self.status._position, (1.0, 2.0, 3.0))
        self.assertEqual(self.status._orientation, (0, 0, 0, 1))
        self.assertFalse(self.status._done)
        self.assertEqual(self.status._track_geometry, "track_geometry")
        self.assertEqual(self.status._front_of_car_point.coords[:][0],
                         (1.16176, 2.0, 3.0))
        self.assertEqual(self.status._is_offtrack, True)
        self.assertEqual(self.status._progress, 10)

    def test_update_done(self) -> None:
        self.status._orientation = (1, 1, 1, 1)
        deepracer_env_data = DeepRacerEnvData(
            {self.name: True},
            "test",
            {self.name: {"position": (1.0, 2.0, 3.0),
                         "orientation": (0, 0, 0, 1),
                         "is_offtrack": True,
                         "progress": 10}},
            "track_geometry")
        self.status.update(deepracer_env_data)
        self.assertEqual(self.status._steps, 1)
        self.assertEqual(self.status._position, (1.0, 2.0, 3.0))
        self.assertEqual(self.status._orientation, (0, 0, 0, 1))
        self.assertTrue(self.status._done)
        self.assertEqual(self.status._track_geometry, "track_geometry")
        self.assertEqual(self.status._front_of_car_point.coords[:][0],
                         (1.16176, 2.0, 3.0))
        self.assertEqual(self.status._is_offtrack, True)
        self.assertEqual(self.status._progress, 10)

    def test_to_dict(self) -> None:
        self.status._position = (-7.25, 0.9, 0)
        self.status._orientation = (0.0, 0.0, 0.0, 1.0)
        self.status._front_of_car_point = Point(-7.08824, 0.9, 0)
        self.status._progress = 99.5298442510512
        status_dict = {
            "all_wheels_on_track": True,
            "closest_waypoints": (233, 234),
            "distance_from_center": 0.12220389538742775,
            "is_offtrack": False,
            "progress": 99.5298442510512,
            "steps": 0,
            "track_width": 1.4475344276809832,
            "is_left_of_center": True}
        self.assertEqual(status_dict, self.status.to_dict())
