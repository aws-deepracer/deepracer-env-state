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
"""A class for environment data"""
from typing import Dict, Any, List

from deepracer_track_geometry import TrackGeometry


class DeepRacerEnvData():
    """
    DeepRacerEnvData class
    """
    def __init__(self,
                 done: Dict[str, bool],
                 action: Dict[str, Any],
                 info: Dict[str, Any],
                 track_geometry: TrackGeometry):
        """
        Initialize DeepRacerEnvData

        Args:
            done (Dict[str, bool]): the done(s) for the agent(s) with agent_name as key
            action (Dict[str, Any]): the action(s) for agent(s) with agent_name as key
            info (Dict[str, Any]): the info(s) for agent(s) with agent_name as key
            track_geometry (TrackGeometry): track geometry class instance
        """
        self._done = done
        self._action = action
        self._info = info
        self._track_geometry = track_geometry

    @property
    def done(self) -> Dict[str, bool]:
        """
        Return the done(s) for the agent(s) with agent_name as key

        Returns:
            Dict[str, bool]: the done(s) for the agent(s) with agent_name as key
        """
        return self._done

    @property
    def action(self) -> Dict[str, Any]:
        """
        Return the action(s) for agent(s) with agent_name as key

        Returns:
            Dict[str, Any]: the action(s) for agent(s) with agent_name as key
        """
        return self._action

    @property
    def track_geometry(self) -> TrackGeometry:
        """
        Return track geometry class instance

        Returns:
            TrackGeometry: track geometry class instance
        """
        return self._track_geometry

    @property
    def position(self) -> Dict[str, List[float]]:
        """
        Return position(s) for agent(s) with agent_name as key

        Returns:
            Dict[str, List[float]]: the position list for agent(s) with agent_name as key
        """
        return {agent: info["position"] for agent, info in self._info.items()}

    @property
    def orientation(self) -> Dict[str, List[float]]:
        """
        Return orientation(s) for agent(s) with agent_name as key

        Returns:
            Dict[str, List[float]]: the orientation list for agent(s) with agent_name as key
        """
        return {agent: info["orientation"] for agent, info in self._info.items()}

    @property
    def is_offtrack(self) -> Dict[str, bool]:
        """
        Return is_offtrack bool for agent(s) with agent_name as key

        Returns:
            Dict[str, bool]: is_offtrack for agent(s) with agent_name as key
        """
        return {agent: info["is_offtrack"] for agent, info in self._info.items()}

    @property
    def progress(self) -> Dict[str, float]:
        """
        Return progress for agent(s) with agent_name as key

        Returns:
            Dict[str, float]: progress for agent(s) with agent_name as key
        """
        return {agent: info["progress"] for agent, info in self._info.items()}
