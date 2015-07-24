from l1 import l1, strip_outliers
from matplotlib import pyplot as plt
import numpy as np
import os

plt.style.use('fivethirtyeight')

_DATA_DIR = 'data'
_FIG_DIR = 'figures'
_SNP500_FILE_NAME = 'snp500.txt'
_SNP500_FILE_PATH = os.path.join(_DATA_DIR, _SNP500_FILE_NAME)


def get_signal(file_path=_SNP500_FILE_PATH):
    return np.genfromtxt(file_path)


def get_outlier_signal(x, percent_of_outliers=.2):
    outliers = np.random.random(len(x)) < percent_of_outliers
    outlier_signal = x.copy()
    outlier_signal[outliers] = (np.random.random(outliers.sum()) - 0.5) * 2 + x[outliers]

    return outlier_signal


def plot_l1_trend_fits(x, delta_values=(1 ,5, 10)):
    plt.figure(figsize=(16, 12))
    plt.suptitle('Different trends for different $\delta$ s')

    for ii, delta in enumerate(delta_values):
        plt.subplot(len(delta_values), 1, ii + 1)
        filtered = l1(x, delta)
        plt.plot(x, label='Original signal')
        label = 'Filtered, $\delta$ = {}'.format(delta)
        plt.plot(filtered, linewidth=5, label=label, alpha=0.5)
        plt.legend(loc='best')

    fig_name = 'l1_trend_filtering_snp_{}.png'.format(len(x))
    fig_path = os.path.join(_FIG_DIR, fig_name)
    plt.savefig(fig_path, format='png', dpi=1000)


def plot_outlier_removal_via_l1(outlier_signal, mad_coefficients=None):
    plt.figure(figsize=(16, 12))
    plt.suptitle('Outlier detection via l1 with different MAD coefficient')
    if mad_coefficients is None:
        mad_coefficients = range(1, 4)

    for ii, mad_coef in enumerate(mad_coefficients):
        plt.subplot(len(mad_coefficients), 1, ii + 1)
        x_wo_outliers = strip_outliers(outlier_signal, delta=1, mad_coef=mad_coef)
        plt.plot(outlier_signal, label='Original signal')
        label = 'Stripped Outliers, mad_coef = {}'.format(mad_coef)
        plt.plot(x_wo_outliers, linewidth=5, label=label, alpha=0.5)
        plt.legend(loc='best')

    fig_name = 'remove_outliers_snp_{}.png'.format(len(outlier_signal))
    fig_path = os.path.join(_FIG_DIR, fig_name)
    plt.savefig(fig_path, format='png', dpi=1000)


def flow():
    original_signal = get_signal()
    for length in (100, 500, 1000, 5000, 10000):
        signal = original_signal[:length]
        outlier_signal = get_outlier_signal(signal)
        plot_l1_trend_fits(signal)
        plot_outlier_removal_via_l1(outlier_signal)
        print('Trend extraction of signal for length: {} is completed'.format(length))

if __name__ == '__main__':
    flow()
