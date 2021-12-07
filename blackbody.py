import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#v is volts, i is current
def temper_fourth_func(v, i):
    return (300+(((v/i)/1.1)-1)/(4.5*10**(-3)))**4

#di is current error and tq is temperature^4
def temper_fourth_error_func(v, i, di, tq):
    return 4*tq**(3/4)*(v*di/(i**2*1.1*4.5*10**(-3)))

#x is temperature^4 and a is a constant
def stefan_func(x, a):
    return a*x


if __name__ == '__main__':
    #loading data
    stefan_data = np.loadtxt('data/stefan_dataset.txt', skiprows=1)
    area_data = stefan_data[:,0]
    area_error = stefan_data[:,1]
    volt_data = stefan_data[:,2]
    amp_data = stefan_data[:,3]
    amp_error = stefan_data[:,4]
    temper_fourth_data = temper_fourth_func(volt_data, amp_data)
    temper_fourth_error = temper_fourth_error_func(volt_data, amp_data,
                                                   amp_error,
                                                   temper_fourth_data)
    #curve_fit for optimized constant a to use for the model
    popt, pcov = curve_fit(stefan_func, temper_fourth_data, area_data,
                           sigma=area_error, absolute_sigma=True)

    stefan_model = stefan_func(temper_fourth_data, popt)

    plt.errorbar(temper_fourth_data, area_data, xerr=temper_fourth_error,
                 yerr=area_error, fmt='.', label='Data')
    plt.plot(temper_fourth_data, stefan_model, label='Model')
    plt.title('Area vs Temperature^4 Plot for Stefan-Boltzmann Law ')
    plt.xlabel('Temperature^4')
    plt.ylabel('Area')
    plt.legend()