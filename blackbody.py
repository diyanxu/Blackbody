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

def reduced_chisquared(data_y, model_y, data_error, dof):
    return (1/(data_y.size-dof))*np.sum(((data_y-model_y)/data_error)**2)


def calc_temp(volts, current):
    return 300 + (((volts/current)/1.1 - 1)/0.0045)


def calc_index(angle):
    return np.sqrt((2/np.sqrt(3) * np.sin(angle) + 0.5)**2 + 3/4)


def calc_wave(index):
    return np.sqrt(13900/(index - 1.689))


def sample_std(list):
    mean = np.mean(list)
    total = 0
    for item in list:
        total += (item - mean)**2
    return np.sqrt(total/(len(list) - 1))


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

    plt.savefig('graphs/stefan.png')

    print(reduced_chisquared(area_data, stefan_model, area_error, 1))

    volts = 5
    wien_data = np.loadtxt('data/wien.txt', skiprows=1)

    wien_deg = wien_data[:,0]
    wien_current = wien_data[:,1]

    wien_temp = calc_temp(volts, wien_current)

    # sends angle over after converting to radians
    # intial angle of 80
    wien_index = calc_index(np.radians(80 - wien_deg))

    wien_wave = calc_wave(wien_index)

    average_wave = np.mean(wien_wave)
    error_wave = sample_std(wien_wave)

    average_temp = np.mean(wien_temp)
    error_temp = sample_std(wien_temp)

    wein_value = average_temp * average_wave
    wein_error = wein_value * np.sqrt((error_wave/average_wave)**2 +
                                    (error_temp/average_temp)**2)

    print('Average wavelength: ', round(average_wave), '+-', round(error_wave))
    print('Average temperature: ', round(average_temp), '+-', round(error_temp))

    print('Calculated wein value: ', round(wein_value), '+-', round(wein_error))