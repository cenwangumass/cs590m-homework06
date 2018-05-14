import json
from math import ceil, sqrt

import numpy as np
from scipy import stats

from constants import *


def q(data, quantile):
    n = len(data)
    i = int(ceil(quantile * n)) - 1 if quantile != 0 else 0
    return data[i]


def compute_inter_quartile_range(data, m):
    sorted_data = sorted(data)

    n = len(data)
    k = n // m
    q25 = q(sorted_data, .25)
    q75 = q(sorted_data, .75)
    alpha_n = q75 - q25

    pseudovalues = []
    for i in range(m):
        start = i * k
        end = i * k + k
        remaining_data = data[0:start] + data[end:n]
        remaining_data.sort()
        alpha_i = q(remaining_data, .75) - q(remaining_data, .25)
        pseudovalue = m * alpha_n - (m - 1) * alpha_i
        pseudovalues.append(pseudovalue)

    alpha = np.mean(pseudovalues)
    std = stats.sem(pseudovalues, ddof=1)
    ci = stats.t.interval(0.95, len(pseudovalues) - 1, loc=alpha, scale=std)

    return alpha, ci


def compute_idle_time(simulation) -> float:
    t = 0
    for i in range(0, len(simulation), 2):
        t += simulation[i + 1][0] - simulation[i][0]
    return t


def compute_idle_time_inter_quartile_range(data):
    idle_times = []
    for simulation in data:
        idle_time = compute_idle_time(simulation)
        idle_times.append(idle_time)

    return compute_inter_quartile_range(idle_times, 5)


def compute_link_2_idle_fraction(data) -> (float, tuple):
    i = 0
    j = 1
    s = 0
    result = []
    while j < len(data):
        state = data[j][1]

        if state == BUSY:
            s += data[j][0] - data[j - 1][0]

        if data[j][2]:
            result.append((s, data[j][0] - data[i][0]))
            i = j
            j = i + 1
            s = 0
        else:
            j += 1
    result = np.asarray(result)

    x, y = result.T
    n = len(x)

    x_bar = np.mean(x)
    y_bar = np.mean(y)
    alpha = x_bar / y_bar

    c_n = 1 / y_bar
    d_n = -x_bar / y_bar ** 2
    s_n = sqrt(
        1 / (n - 1) * np.sum((c_n * (x - x_bar) + d_n * (y - y_bar)) ** 2)
    )
    hw = stats.norm.ppf(0.975) * s_n / sqrt(n)
    ci = (alpha - hw, alpha + hw)

    return alpha, ci


def compute_standard_deviation(data):
    idle_times = []
    for simulation in data:
        idle_time = compute_idle_time(simulation)
        idle_times.append(idle_time)
    idle_times = np.asarray(idle_times)

    x = idle_times ** 2
    y = idle_times
    x_bar = np.mean(x)
    y_bar = np.mean(y)
    alpha = sqrt(x_bar - y_bar ** 2)

    tmp = sqrt(x_bar - y_bar ** 2)
    c_n = 0.5 / tmp
    d_n = -y / tmp

    n = len(x)
    s_n = sqrt(
        1 / (n - 1) * np.sum((c_n * (x - x_bar) + d_n * (y - y_bar)) ** 2)
    )
    hw = stats.norm.ppf(0.975) * s_n / sqrt(n)
    ci = (alpha - hw, alpha + hw)

    return alpha, ci, s_n


def main():
    with open("data.json") as f:
        data = json.load(f)

    mu, ci = compute_idle_time_inter_quartile_range(data["idle"])
    print(mu, ci)

    mu, ci = compute_link_2_idle_fraction(data["link2"][0])
    print(mu, ci)

    mu, ci, s_n = compute_standard_deviation(data["idle"])
    print(mu, ci)
    print(s_n * stats.norm.ppf(0.975) ** 2 / (0.02 ** 2 * mu ** 2))


if __name__ == "__main__":
    main()
