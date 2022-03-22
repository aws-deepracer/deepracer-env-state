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

from deepracer_env_state.composite_state import CompositeState
from deepracer_env_state.agent.constants import AgentStates
from deepracer_env_state.agent.action import Action


class CompositeStateTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_init(self) -> None:
        composite_state = CompositeState()
        self.assertFalse(bool(composite_state._states))

    def test_add_not_added(self) -> None:
        composite_state = CompositeState()
        action = Action("agent0")
        composite_state.add(AgentStates.ACTION, action)
        self.assertEqual(composite_state._states, {AgentStates.ACTION: action})

    def test_add_already_added(self) -> None:
        composite_state = CompositeState()
        action = Action("agent0")
        composite_state._states = {AgentStates.ACTION: action}
        composite_state.add(AgentStates.ACTION, Action("agent1"))
        self.assertEqual(composite_state._states, {AgentStates.ACTION: action})

    def test_get(self) -> None:
        composite_state = CompositeState()
        action = Action("agent0")
        composite_state._states = {AgentStates.ACTION: action}
        self.assertEqual(composite_state.get(AgentStates.ACTION), action)

    def test_get_not_exist(self) -> None:
        composite_state = CompositeState()
        with self.assertRaises(Exception):
            composite_state.get(AgentStates.ACTION)

    def test_update(self) -> None:
        composite_state = CompositeState()
        composite_state._states = {AgentStates.ACTION: MagicMock(),
                                   AgentStates.POSE: MagicMock()}
        composite_state.update("env_data")
        [state.update.assert_called_once_with("env_data")
         for state in composite_state._states.values()]

    def test_to_dict(self) -> None:
        state1 = MagicMock()
        state2 = MagicMock()
        state1.to_dict.return_value = {"action": 1.0}
        state2.to_dict.return_value = {"pose": 2.0}
        composite_state = CompositeState()
        composite_state._states = {AgentStates.ACTION: state1,
                                   AgentStates.POSE: state2}
        self.assertEqual(composite_state.to_dict(), {"action": 1.0, "pose": 2.0})
