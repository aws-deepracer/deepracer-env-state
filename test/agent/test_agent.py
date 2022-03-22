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

from deepracer_env_state.agent.agent import Agent
from deepracer_env_state.agent.constants import AgentStates


class AgentTest(TestCase):
    def setUp(self) -> None:
        pass

    @patch("deepracer_env_state.agent.agent.Action")
    @patch("deepracer_env_state.agent.agent.Pose")
    @patch("deepracer_env_state.agent.agent.Status")
    def test_init(self, status_mock, pose_mock, action_mock) -> None:
        agent = Agent("agent0")
        self.assertEqual(agent._name, "agent0")
        self.assertEqual(
            agent._states,
            {AgentStates.ACTION: action_mock(agent._name),
             AgentStates.POSE: pose_mock(agent._name),
             AgentStates.STATUS: status_mock(agent._name)})

    def test_name(self) -> None:
        agent = Agent("agent0")
        self.assertEqual(agent.name, "agent0")

    @patch("deepracer_env_state.agent.agent.Action")
    def test_action(self, action_mock) -> None:
        agent = Agent("agent0")
        self.assertEqual(agent.action, action_mock(agent._name))

    @patch("deepracer_env_state.agent.agent.Pose")
    def test_pose(self, pose_mock) -> None:
        agent = Agent("agent0")
        self.assertEqual(agent.pose, pose_mock(agent._name))

    @patch("deepracer_env_state.agent.agent.Status")
    def test_status(self, status_mock) -> None:
        agent = Agent("agent0")
        self.assertEqual(agent.status, status_mock(agent._name))
