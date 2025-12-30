# Linear Kalman Filter
class KalmanFilter:
    """
    The linear Kalman filter (trackingKF) is an optimal, recursive algorithm for estimating the state of an object 
    if the estimation system is linear and Gaussian. An estimation system is linear if both the motion model and 
    measurement model are linear. The filter works by recursively predicting the object state using the motion model 
    and correcting the state using measurements.

    ~ Mathworks reference: https://www.mathworks.com/help/tracking/ug/kalman-filter-tracking.html

    """
    
    def __init__(self, initial_state, initial_covariance, transition_matrix, observation_matrix, process_noise_covariance, observation_noise_covariance):
        self.state = initial_state
        self.P = initial_covariance
        self.F = transition_matrix
        self.H = observation_matrix
        self.Q = process_noise_covariance
        self.R = observation_noise_covariance

    # Predict the state and covariance
    def predict(self):
        self.state = self.F @ self.state
        self.P = self.F @ self.P @ self.F.T + self.Q

    # Update the state and covariance with the observation
    def update(self, observation):
        # Calculate the innovation and innovation covariance
        innovation = observation - self.H @ self.state
        innovation_covariance = self.H @ self.P @ self.H.T + self.R
        # Calculate the Kalman gain
        kalman_gain = self.P @ self.H.T @ np.linalg.inv(innovation_covariance)
        # Update the state and covariance
        self.state = self.state + kalman_gain @ innovation
        self.P = (np.eye(self.state.shape[0]) - kalman_gain @ self.H) @ self.P