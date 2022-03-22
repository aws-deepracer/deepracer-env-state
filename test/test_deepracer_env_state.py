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
from unittest.mock import patch, MagicMock, call
from deepracer_track_geometry import TrackDirection
from deepracer_env_state.deepracer_env_state import DeepRacerEnvState
from deepracer_env_config import Track as TrackConfig
from deepracer_env_config import Agent as AgentConfig
from deepracer_env import DEFAULT_TRACK


class DeepracerEnvStateTest(TestCase):
    def setUp(self) -> None:
        self.deepracer_env = MagicMock()
        self.deepracer_env.get_track.return_value = TrackConfig()
        self.deepracer_env.get_agent.return_value = [AgentConfig()]

    def test_init_agent_not_list(self) -> None:
        self.deepracer_env.get_agent.return_value = AgentConfig()
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        deepracer_env_state._deepracer_env.get_track.assert_called_once()
        deepracer_env_state._deepracer_env.get_agent.assert_called_once()

    def test_init(self) -> None:
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        deepracer_env_state._deepracer_env.get_track.assert_called_once()
        deepracer_env_state._deepracer_env.get_agent.assert_called_once()
        deepracer_env_state._deepracer_env.register.assert_called_once_with(
            deepracer_env_state)

    @patch("deepracer_env_state.deepracer_env_state.DeepRacerEnvData")
    def test_on_step(self, env_data_mock) -> None:
        env = MagicMock()
        done = {"agent0": MagicMock()}
        action = {"agent0": MagicMock()}
        info = {"agent0": MagicMock()}
        step_result = ("test", "test", done, action, info)
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        env_data_mock.return_value = "env_data"
        deepracer_env_state._agents = {MagicMock()}
        deepracer_env_state._track = MagicMock()
        deepracer_env_state.on_step(env, step_result)

        env_data_mock.assert_called_once_with(
            done, action, info, deepracer_env_state._track_geometry)
        [agent.update.assert_has_calls(
            [call("env_data")]) for agent in deepracer_env_state._agents]
        deepracer_env_state._track.update.assert_called_once_with("env_data")

    @patch("deepracer_env_state.deepracer_env_state.TrackGeometry")
    def test_on_reset_same_track(self, track_geometry_mock) -> None:
        env = MagicMock()
        reset_result = MagicMock()
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        deepracer_env_state.on_reset(env, reset_result)
        # called only once from constructor
        track_geometry_mock.assert_called_once()

    @patch("deepracer_env_state.deepracer_env_state.TrackGeometry")
    def test_on_reset_diff_track(self, track_geometry_mock) -> None:
        env = MagicMock()
        reset_result = MagicMock()
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        self.deepracer_env.get_track.return_value = TrackConfig(
            name="austin")
        deepracer_env_state.on_reset(env, reset_result)
        # call twice from constroctor and on_reset
        track_geometry_mock.assert_has_calls(
            [call(DEFAULT_TRACK),
             call(direction=TrackDirection.COUNTER_CLOCKWISE,
                  finish_line=0.0,
                  track_name='austin')])

    @patch("deepracer_env_state.deepracer_env_state.copy")
    def test_track(self, copy_mock) -> None:
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        deepracer_env_state._track = MagicMock()
        copy_mock.deepcopy.return_value = "track"
        deepracer_env_state.track
        copy_mock.deepcopy.assert_called_once()
        self.assertEqual(deepracer_env_state.track, "track")

    @patch("deepracer_env_state.deepracer_env_state.copy")
    def test_agents(self, copy_mock) -> None:
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        agent = MagicMock()
        agent.name = "agent_name"
        copy_mock.deepcopy.return_value = "agent_return"
        deepracer_env_state._agents = {agent}
        deepracer_env_state.agents
        copy_mock.deepcopy.assert_called_once()
        self.assertEqual(deepracer_env_state.agents, {"agent_name": "agent_return"})

    def test_to_dict(self) -> None:
        deepracer_env_state = DeepRacerEnvState(self.deepracer_env)
        agent_mock = MagicMock()
        agent_mock.name = "agent0"
        agent_mock.to_dict.return_value = {"x": 0, "y": 0}
        deepracer_env_state._agents = {agent_mock}
        deepracer_env_state._track = MagicMock()
        deepracer_env_state._track.to_dict.return_value = {"name": "spain"}
        self.assertEqual(deepracer_env_state.to_dict(),
                         {"agent0": {"x": 0, "y": 0}, "name": "spain"})
