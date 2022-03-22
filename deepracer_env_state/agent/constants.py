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
"""Module to contain agent related constants"""
from enum import Enum


class AgentStates(Enum):
    """
    AgentStates class
    """
    ACTION = "action"
    POSE = "pose"
    STATUS = "status"


# DeepRacer device dimension
DEEPRACER_LENGTH = 0.32352
DEEPRACER_WIDTH = 0.1961

# DeepRacer offtrack collider dimension

# approximated length between the centers of front and rear wheel.
# - Used 82.31 mm * 2 instead of 82.31 mm + 81.05 mm as the collider
#   will rotate around the center of car.
DEEPRACER_OFFTRACK_COLLIDER_LENGTH = 0.16462
# Same as DeepRacer device width
DEEPRACER_OFFTRACK_COLLIDER_WIDTH = 0.1961

# DeepRacer wheel relative position to car center origion
RELATIVE_POSITION_OF_FRONT_LEFT_WHEEL = (DEEPRACER_OFFTRACK_COLLIDER_LENGTH / 2,
                                         DEEPRACER_OFFTRACK_COLLIDER_WIDTH / 2,
                                         0)
RELATIVE_POSITION_OF_FRONT_RIGHT_WHEEL = (DEEPRACER_OFFTRACK_COLLIDER_LENGTH / 2,
                                          - DEEPRACER_OFFTRACK_COLLIDER_WIDTH / 2,
                                          0)
RELATIVE_POSITION_OF_REAR_LEFT_WHEEL = (- DEEPRACER_OFFTRACK_COLLIDER_LENGTH / 2,
                                        DEEPRACER_OFFTRACK_COLLIDER_WIDTH / 2,
                                        0)
RELATIVE_POSITION_OF_REAR_RIGHT_WHEEL = (- DEEPRACER_OFFTRACK_COLLIDER_LENGTH / 2,
                                         - DEEPRACER_OFFTRACK_COLLIDER_WIDTH / 2,
                                         0)

RELATIVE_POSITION_OF_FOUR_WHEELS = [
    RELATIVE_POSITION_OF_FRONT_LEFT_WHEEL,
    RELATIVE_POSITION_OF_FRONT_RIGHT_WHEEL,
    RELATIVE_POSITION_OF_REAR_LEFT_WHEEL,
    RELATIVE_POSITION_OF_REAR_RIGHT_WHEEL]

RELATIVE_POSITION_OF_FRONT_OF_CAR = (DEEPRACER_LENGTH / 2, 0, 0)
