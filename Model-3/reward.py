def reward_function(params):
    '''
    Example of rewarding the agent to stay inside the two borders of the track and follow center line and higher speed
    '''
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    
     # Penalize if the car is too far away from the center
    marker_2 = 0.4 * track_width

    # Give a high reward if no wheels go off the track and
    # the agent is somewhere in between the track borders
    if not all_wheels_on_track or distance_from_center > marker_2:
        # Penalize if the car goes off track
        reward = 1e-3
    elif distance_from_center <= marker_2:
        # Penalize if the car goes too slow
        reward = 0.5 * (speed / 5.0)
    else:
        # High reward if the car stays on track and goes fast
        reward = 1.0 * (speed / 5.0)

    # Always return a float value
    return float(reward)