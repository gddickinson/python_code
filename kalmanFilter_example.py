import numpy as np
import matplotlib.pyplot as plt

def kalman_xy(x, P, measurement, R,
              motion = np.matrix('0. 0. 0. 0.').T,
              Q = np.matrix(np.eye(4))):
    """
    Parameters:    
    x: initial state 4-tuple of location and velocity: (x0, x1, x0_dot, x1_dot)
    P: initial uncertainty convariance matrix
    measurement: observed position
    R: measurement noise 
    motion: external motion added to state vector x
    Q: motion noise (same shape as P)
    """
    #print(measurement)    
    return kalman(x, P, measurement, R, motion, Q,
                  F = np.matrix('''
                      1. 0. 1. 0.;
                      0. 1. 0. 1.;
                      0. 0. 1. 0.;
                      0. 0. 0. 1.
                      '''),
                  H = np.matrix('''
                      1. 0. 0. 0.;
                      0. 1. 0. 0.'''))

def kalman(x, P, measurement, R, motion, Q, F, H):
    '''
    Parameters:
    x: initial state
    P: initial uncertainty convariance matrix
    measurement: observed position (same shape as H*x)
    R: measurement noise (same shape as H)
    motion: external motion added to state vector x
    Q: motion noise (same shape as P)
    F: next state function: x_prime = F*x
    H: measurement function: position = H*x

    Return: the updated and predicted new values for (x, P)

    See also http://en.wikipedia.org/wiki/Kalman_filter

    This version of kalman can be applied to many different situations by
    appropriately defining F and H 
    '''
    # UPDATE x, P based on measurement m    
    # distance between measured and current position-belief
    y = np.matrix(measurement).T - H * x
    print(y)
    S = H * P * H.T + R  # residual convariance
    K = P * H.T * S.I    # Kalman gain
    x = x + K*y
    I = np.matrix(np.eye(F.shape[0])) # identity matrix
    P = (I - K*H)*P

    # PREDICT x, P based on motion
    x = F*x + motion
    P = F*P*F.T + Q

    return x, P

#==============================================================================
# def demo_kalman_xy():
#     x = np.matrix('0. 0. 0. 0.').T 
#     P = np.matrix(np.eye(4))*1000 # initial uncertainty
# 
#     N = 20
#     true_x = np.linspace(0.0, 10.0, N)
#     true_y = true_x**2
#     observed_x = true_x + 0.05*np.random.random(N)*true_x
#     observed_y = true_y + 0.05*np.random.random(N)*true_y
#     plt.plot(observed_x, observed_y, 'ro')
#     result = []
#     R = 0.01**2
#     for meas in zip(observed_x, observed_y):
#         x, P = kalman_xy(x, P, meas, R)
#         result.append((x[:2]).tolist())
#     kalman_x, kalman_y = zip(*result)
#     plt.plot(kalman_x, kalman_y, 'g-')
#     plt.show()
#==============================================================================

#demo_kalman_xy()


x = (3.2618187593136714, 4.229518090705041, 4.970144154070997, 5.4584758171066685, 5.677883530716649, 5.620895628364498, 5.289452764715364, 4.694841828968918, 3.857311583384793, 2.8053831159695455)
y = (5.248776670511476,6.394882252046046,7.699287493626686,9.117572439213015,10.601439096028392,12.10035616477686,13.563279822435065,14.940391958424991,16.18479667061946,17.25411724904363)


def demo_kalman_xy2():

    observed_x = (3.2618187593136714, 4.229518090705041, 4.970144154070997, 5.4584758171066685, 5.677883530716649, 5.620895628364498, 5.289452764715364, 4.694841828968918, 3.857311583384793, 2.8053831159695455)
    observed_y = (5.248776670511476,6.394882252046046,7.699287493626686,9.117572439213015,10.601439096028392,12.10035616477686,13.563279822435065,14.940391958424991,16.18479667061946,17.25411724904363)


    x = np.matrix('0. 0. 0. 0.').T 
    P = np.matrix(np.eye(4))*1000 # initial uncertainty

    plt.plot(observed_x, observed_y, 'ro')
    result = []
    R = 0.01**2
    for meas in zip(observed_x, observed_y):
        x, P = kalman_xy(x, P, meas, R)
        result.append((x[:2]).tolist())
    kalman_x, kalman_y = zip(*result)
    plt.plot(kalman_x, kalman_y, 'g-')
    plt.show()

#demo_kalman_xy()
demo_kalman_xy2()