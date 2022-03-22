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

from deepracer_env_state.agent.action import Action
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData


class ActionTest(TestCase):
    def setUp(self) -> None:
        self.name = "agent0"
        self.action = Action(self.name)

    def test_init(self) -> None:
        self.assertEqual(self.action._name, self.name)
        self.assertEqual(self.action._steering_angle, 0.0)
        self.assertEqual(self.action._speed, 0.0)

    def test_steering_angle(self) -> None:
        self.action._steering_angle = 1.0
        self.assertEqual(self.action.steering_angle, 1.0)

    def test_speed(self) -> None:
        self.action._speed = 2.0
        self.assertEqual(self.action.speed, 2.0)

    def test_update(self) -> None:
        deepracer_env_data = DeepRacerEnvData(
            "test",
            {self.name: (1.0, 2.0)},
            "test",
            "test")
        self.action.update(deepracer_env_data)
        self.assertEqual(self.action._steering_angle, 1.0)
        self.assertEqual(self.action._speed, 2.0)

    def test_to_dict(self) -> None:
        self.action._steering_angle = 1.0
        self.action._speed = 2.0
        self.assertEqual(
            self.action.to_dict(),
            {"speed": 2.0,
             "steering_angle": 1.0})
