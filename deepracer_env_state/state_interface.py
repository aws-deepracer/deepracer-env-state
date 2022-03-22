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
"""A abstract class for state interface"""
import abc

from typing import Dict, Any
from deepracer_env_state.deepracer_env_data import DeepRacerEnvData

# Python 2 and 3 compatible Abstract class
ABC = abc.ABCMeta('ABC', (object,), {})


class StateInterface(ABC):
    """
    State Interface
    """
    @abc.abstractmethod
    def update(self, deepracer_env_data: DeepRacerEnvData) -> None:
        """
        Update the internal state information

        Args:
            deepracer_env_data (DeepRacerEnvData): DeepRacerEnvData class instance

        """
        raise NotImplementedError()

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Return all internal state as a dict format

        Returns:
            Dict[str, Any]: internal state as a dict format
        """
        raise NotImplementedError()
