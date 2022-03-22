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
"""A class for agent state"""
from deepracer_env_state.composite_state import CompositeState
from deepracer_env_state.agent.constants import AgentStates
from deepracer_env_state.agent.action import Action
from deepracer_env_state.agent.pose import Pose
from deepracer_env_state.agent.status import Status


class Agent(CompositeState):
    """
    Agent class
    """
    def __init__(self, name: str):
        """
        Initialize Agent

        Args:
            name (str): agent name
        """
        super().__init__()
        self._name = name
        self.add(AgentStates.ACTION, Action(self._name))
        self.add(AgentStates.POSE, Pose(self._name))
        self.add(AgentStates.STATUS, Status(self._name))

    @property
    def name(self) -> str:
        """
        Return agent name

        Returns:
            str: agent name
        """
        return self._name

    @property
    def action(self) -> Action:
        """
        Return Action class instance

        Returns:
            Action: Action class instance
        """
        return self.get(AgentStates.ACTION)

    @property
    def pose(self) -> Pose:
        """
        Return Pose class instance

        Returns:
            Pose: Pose class instance
        """
        return self.get(AgentStates.POSE)

    @property
    def status(self) -> Status:
        """
        Return Status class instance

        Returns:
            Status: Status class instance
        """
        return self.get(AgentStates.STATUS)
