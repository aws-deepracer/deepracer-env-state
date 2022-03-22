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
"""Module to contain agent related utils"""
import math

from typing import List, Tuple


def rotate(vector: List[float], quaternion: List[float]) -> Tuple[float, float, float]:
    """
    Returns the rotated vector in the orientation of the given quaternion.

    This function assumes that v is a homogeneous quaternion. That is the real part is zero.
    The complete explanation can be found in the link
    https://math.stackexchange.com/questions/40164/how-do-you-rotate-a-vector-by-a-unit-quaternion
    https://en.wikipedia.org/wiki/Quaternion#Hamilton_product

    On an high level. We want the vector v in the direction of the quaternion q. We know that
    q * q_conj = 1

    p = q * v * q_conj, where p is pure quaternion, same length as v in the direction of q.

    The simplified formula in the executed code is derived from the below equations

    quaternion_mult(q,r)
        b1, c1, d1, a1 = q  # Here a1 and a2 are real numbers, b1, c1, d1 are imaginary i,j,k
        b2, c2, d2, a2 = r
        return [
            a1*b2 + b1*a2 + c1*d2 - d1*c2,
            a1*c2 - b1*d2 + c1*a2 + d1*b2,
            a1*d2 + b1*c2 - c1*b2 + d1*a2,
            a1*a2 - b1*b2 - c1*c2 - d1*d2
        ]

    rotate(v, q):
        r = np.insert(v, 3, 0)
        q_conj = [-1*q[0],-1*q[1],-1*q[2], q[3]]
        return quaternion_mult(quaternion_mult(q,r), q_conj)[:3]

    If the vector is not pure quaternion. Then in the below simplified solution the real value returned will be
    a2*( a1_sq + b1_sq + c1_sq + d1_sq)

    Args:
        v (List[float]): vector to apply the given quaternion.
        q (List[float]): A quaternion

    Returns:
        Tuple[float, float, float]: final vector from v with q applied.
    """
    b1, c1, d1, a1 = quaternion[0], quaternion[1], quaternion[2], quaternion[3]
    b2, c2, d2 = vector[0], vector[1], vector[2]

    a1_sq = a1 ** 2
    b1_sq = b1 ** 2
    c1_sq = c1 ** 2
    d1_sq = d1 ** 2

    x = b2 * (-c1_sq - d1_sq + b1_sq + a1_sq) + 2 * \
        (-(a1 * c2 * d1) + (b1 * c1 * c2) + (b1 * d1 * d2) + (a1 * c1 * d2))
    y = c2 * (c1_sq - d1_sq + a1_sq - b1_sq) + 2 * \
        ((a1 * b2 * d1) + (b1 * b2 * c1) + (c1 * d1 * d2) - (a1 * b1 * d2))
    z = d2 * (-c1_sq + d1_sq + a1_sq - b1_sq) + 2 * \
        ((a1 * b1 * c2) + (b1 * b2 * d1) - (a1 * b2 * c1) + (c1 * c2 * d1))
    return x, y, z


def quaternion_to_euler(x: float, y: float, z: float, w: float) -> Tuple[float, float, float]:
    """
    Convert quaternion x, y, z, w to euler angle roll, pitch, yaw

    Args:
        x (float): quaternion x
        y (float): quaternion y
        z (float): quaternion z
        w (float): quaternion w

    Returns:
        Tuple: (roll, pitch, yaw) in radian
    """
    # roll (x-axis rotation)
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = 2.0 * (w * y - z * x)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)  # use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)

    # yaw (z-axis rotation)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw
