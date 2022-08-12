Kalman Filter implementation on a sample of generated data of x and y gps coordinates

GenerateDataSet.py is imported into KalmanFIlter.py
GenerateDataSet.py contains the class to generate the test sample data which has True values of X and Y coordinates as numpy arrays and X and Y coordinates with noise added to them to simulate a sensor. the measurement time interval, number of measurements and the sensor's standard deviation from the real values can be altered through the params of creating the CoordDataSet object class.

KalmanFilter.py runs a Kalman Filter on the dataset object we get from GenerateDataSet.py
plotData() function of a Kalman Filter object plots out the real , deviated and filtered values of the coords

The standard deviation of the sensor and the Filter are printed out at the end to evaulte performance
