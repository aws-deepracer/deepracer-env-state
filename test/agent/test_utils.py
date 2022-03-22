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
from deepracer_env_state.agent.utils import (
    rotate,
    quaternion_to_euler)


class UtilsTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_rotate(self) -> None:
        vector = [1.0, 0.0, 0.0]
        quaternion = [0.0, 0.0, 1.0, 0]
        expected_vector = (-1.0, 0.0, 0.0)
        self.assertEqual(rotate(vector, quaternion), expected_vector)

    def test_quaternion_to_euler(self) -> None:
        quaternion = (
            -0.7182870182434113,
            0.31062245106570396,
            0.44443511344300074,
            0.4359528440735657)
        euler = quaternion_to_euler(
            quaternion[0],
            quaternion[1],
            quaternion[2],
            quaternion[3])
        expected_euler = (
            -2.141592653589793,
            1.1415926535897936,
            -0.14159265358979317)
        self.assertEqual(euler, expected_euler)
