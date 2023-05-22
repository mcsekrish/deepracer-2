import math

def reward_function(params):
    ###############################################################################
    '''
    Example of using waypoints and heading to make the car point in the right direction
    '''

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    all_wheels_on_track = params['all_wheels_on_track']
    is_crashed = params['is_crashed']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
    
    distance_from_center = params['distance_from_center']
    steering_angle = params['steering_angle']
    is_left_of_center = params['is_left_of_center']
    track_width = params['track_width']

    # Initialize the reward with typical value
    reward = 1.0

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - (heading + steering_angle))
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 5.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.2

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward *= 1.0
    elif distance_from_center <= marker_2:
        reward *= 0.5
    elif distance_from_center <= marker_3:
        reward *= 0.1

    # If almost off-track and the steering angle still points to off-track
    if (0.5*track_width - distance_from_center) < 0.05:
        if is_left_of_center and steering_angle > -5: 
            reward *= 0.2
        elif not is_left_of_center and steering_angle < 5: 
            reward *= 0.2

    if not all_wheels_on_track or is_crashed or is_offtrack or is_reversed:
        reward = 1e-3

    return float(reward)
