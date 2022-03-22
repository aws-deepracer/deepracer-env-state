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

from deepracer_env_state.agent.pose import Pose
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData


class PoseTest(TestCase):
    def setUp(self) -> None:
        self.name = "agent0"
        self.pose = Pose(self.name)

    def test_init(self) -> None:
        self.assertEqual(self.pose._name, self.name)
        self.assertEqual(self.pose._position,
                         (0.0, 0.0, 0.0))
        self.assertEqual(self.pose._euler_angle,
                         (0.0, 0.0, 0.0))
        self.assertEqual(list(self.pose._front_of_car_position),
                         [0.16176, 0.0, 0.0])

    def test_x(self) -> None:
        self.pose._front_of_car_position = (1, 2, 3)
        self.assertEqual(self.pose.x, 1)

    def test_y(self) -> None:
        self.pose._front_of_car_position = (1, 2, 3)
        self.assertEqual(self.pose.y, 2)

    def test_z(self) -> None:
        self.pose._front_of_car_position = (1, 2, 3)
        self.assertEqual(self.pose.z, 3)

    def test_roll(self) -> None:
        self.pose._euler_angle = (0.1, 0.2, 0.3)
        self.assertAlmostEqual(self.pose.roll, 0.1)

    def test_pitch(self) -> None:
        self.pose._euler_angle = (0.1, 0.2, 0.3)
        self.assertAlmostEqual(self.pose.pitch, 0.2)

    def test_yaw(self) -> None:
        self.pose._euler_angle = (0.1, 0.2, 0.3)
        self.assertAlmostEqual(self.pose.yaw, 0.3)

    def test_update(self) -> None:
        deepracer_env_data = DeepRacerEnvData(
            "test",
            "test",
            {self.name: {"position": (1.0, 2.0, 3.0),
                         "orientation": (0.0, 0.0, 0.3826834323650898, 0.9238795325112867)}},
            "test")
        self.pose.update(deepracer_env_data)
        self.assertEqual(self.pose._position, (1.0, 2.0, 3.0))
        self.assertAlmostEqual(self.pose._euler_angle, (0.0, 0.0, 0.7853981633974484))
        self.assertAlmostEqual(list(self.pose._front_of_car_position),
                               [1.1143815929247358, 2.114381592924736, 3.0])

    def test_to_dict(self) -> None:
        self.assertEqual(
            self.pose.to_dict(),
            {"x": 0.16176,
             "y": 0.0,
             "z": 0.0,
             "roll": 0.0,
             "pitch": 0.0,
             "yaw": 0.0})
