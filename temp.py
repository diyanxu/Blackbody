# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def temper_quart_func(x, y):
    return (300+(((x/y)/1.1)-1)/(4.5*10**(-3)))**4


def stefan_func(x, a):
    return a*x


if __name__ == '__main__':
    area_data = np.array([10.2459, 9.5128, 7.6544, 6.0169, 5.2921, 3.6674,
                          2.3005])
    average_area_error = np.mean([0.3982, 0.4102, 0.3852])
    error_data = np.zeros(7)+average_area_error
    print(error_data)
    volt_data = np.array([10, 9, 8, 7, 6, 5, 4])
    amp_data = np.array([0.636, 0.604, 0.561, 0.518, 0.475, 0.426, 0.374])
    areavoltamp_data = np.array([area_data, volt_data, amp_data])
    print(areavoltamp_data)
    temper_quart_data = temper_quart_func(areavoltamp_data[1], 
                                          areavoltamp_data[2])
    print(temper_quart_data)

    popt, pcov = curve_fit(stefan_func, temper_quart_data, areavoltamp_data[0],
                           sigma=error_data, absolute_sigma=True)
    print(popt)
    stefan_model = stefan_func(temper_quart_data, popt)
    plt.errorbar(temper_quart_data, areavoltamp_data[0], yerr=error_data
                 , fmt='.')
    plt.plot(temper_quart_data, stefan_model)
    #amp error is approximately +- 0.01A