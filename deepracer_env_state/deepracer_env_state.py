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
"""A class for environment state"""
import copy

from typing import Dict, Any
from deepracer_env import (
    DeepRacerEnv,
    DeepRacerEnvObserverInterface,
    DEFAULT_TRACK)
from deepracer_env_state.agent.agent import Agent
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData
from deepracer_env_state.track.track import Track
from deepracer_track_geometry import TrackGeometry
from ude import (
    UDEStepResult,
    UDEResetResult)


class DeepRacerEnvState(DeepRacerEnvObserverInterface):
    """
    DeepRacerEnvState class
    """
    def __init__(self, deepracer_env: DeepRacerEnv):
        """
        Initialize DeepRacerEnvState

        Args:
            deepracer_env (DeepRacerEnv): DeepRacerEnv class instance
        """
        self._deepracer_env = deepracer_env
        self._track_geometry = TrackGeometry(DEFAULT_TRACK)
        self._track_config = self._deepracer_env.get_track()
        self._track = Track()
        # TODO: deepracer_env.get_agent is return single agent now.
        # After supporting multi-agent and return list, we do not need
        # list conversion anymore.
        agents = deepracer_env.get_agent()
        agents = [agents] if not isinstance(agents, list) else agents
        self._agents = {Agent(agent.name) for agent in agents}
        self._deepracer_env.register(self)

    def on_step(self, env: DeepRacerEnv, step_result: UDEStepResult) -> None:
        """
        On step callback

        Args:
            env (DeepRacerEnv): DeepRacer environment.
            step_result (UDEStepResult): step result (obs, reward, done, last action, info)
        """
        _, _, done, action, info = step_result
        deepracer_env_data = DeepRacerEnvData(done, action, info, self._track_geometry)
        [agent.update(deepracer_env_data) for agent in self._agents]
        self._track.update(deepracer_env_data)

    def on_reset(self, env: DeepRacerEnv, reset_result: UDEResetResult) -> None:
        """
        On Reset callback.

        Args:
            env (DeepRacerEnv): DeepRacer environment.
            reset_result (UDEResetResult): reset result (obs, info)
        """
        track_config = self._deepracer_env.get_track()
        if not self._track_config == track_config:
            self._track_geometry = TrackGeometry(
                track_name=track_config.name,
                finish_line=track_config.finish_line,
                direction=track_config.direction)
        self._track_config = track_config

    @property
    def track(self) -> Track:
        """
        Return track state

        Returns:
            Track: track state class instance
        """
        return copy.deepcopy(self._track)

    @property
    def agents(self) -> Dict[str, Agent]:
        """
        Return agents state

        Returns:
            Dict[str, Agent]: dict with key as agent name and value as Agent class instance
        """
        return {agent.name: copy.deepcopy(agent) for agent in self._agents}

    def to_dict(self) -> Dict[str, Any]:
        """
        Return DeepRacerEnvState class instance in dict format

        Returns:
            Dict[str, Any]: DeepRacerEnvState class instance in dict format
        """
        env_dict = {}
        env_dict.update({agent.name: agent.to_dict() for agent in self._agents})
        env_dict.update(self._track.to_dict())
        return env_dict
