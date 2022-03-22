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
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData


class DeepracerEnvDataTest(TestCase):
    def setUp(self) -> None:
        self.done = {"agent0": True}
        self.action = {"agent0": "action"}
        self.info = {"agent0": {"position": 1, "orientation": 2, "progress": 10, "is_offtrack": True}}
        self.track_geometry = "track_geometry"
        self.deepracer_env_data = DeepRacerEnvData(
            self.done,
            self.action,
            self.info,
            self.track_geometry)

    def test_done(self) -> None:
        self.assertEqual(self.deepracer_env_data.done, self.done)

    def test_action(self) -> None:
        self.assertEqual(self.deepracer_env_data.action, self.action)

    def test_track_geometry(self) -> None:
        self.assertEqual(self.deepracer_env_data.track_geometry, self.track_geometry)

    def test_position(self) -> None:
        self.assertEqual(self.deepracer_env_data.position, {"agent0": 1})

    def test_orinetation(self) -> None:
        self.assertEqual(self.deepracer_env_data.orientation, {"agent0": 2})

    def test_progress(self) -> None:
        self.assertEqual(self.deepracer_env_data.progress, {"agent0": 10})

    def test_is_offtrack(self) -> None:
        self.assertEqual(self.deepracer_env_data.is_offtrack, {"agent0": True})
