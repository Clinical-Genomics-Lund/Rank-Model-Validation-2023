#A script to visually compare standard deviations of two normal distributions which have been converted to standard normal deviations (with a mean of 0).

import sys
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics
import glob

def main():
    model_1_path = sys.argv[1]
    model_2_path = sys.argv[2]

    model_1_list = get_data(model_1_path)
    model_1_list.sort()
    model_1_x = standardize(model_1_list)
    model_1_y = norm.pdf(model_1_x, statistics.mean(model_1_x), statistics.stdev(model_1_x))

    model_2_list = get_data(model_2_path)
    model_2_list.sort()
    model_2_x = standardize(model_2_list)
    model_2_y = norm.pdf(model_2_x, statistics.mean(model_2_x), statistics.stdev(model_2_x))

    draw_plots(model_1_x, model_1_y, model_2_x, model_2_y, model_2_path)
    
def get_data(model_path): 
    data = []
    filename = glob.glob("{}*_bootstrap_means.txt".format(model_path))
    filename = filename[0]
    data_file = open(filename)
    for line in data_file:
        line = line.strip()
        if line[0] != "#":
            data.append(float(line))
    data_file.close()
    return data

def standardize(model_list):
    x_values = []
    old_mean = statistics.mean(model_list)
    for value in model_list:
        standardized_value = value-old_mean
        x_values.append(standardized_value)
    return x_values

def draw_plots(x_axis_1, y_axis_1, x_axis_2, y_axis_2, out_path):
    y_max_1 = max(y_axis_1)
    y_max_2 = max(y_axis_2)
    if y_max_1 >= y_max_2:
        plt.ylim(0, y_max_1+0.05)
    else:
        plt.ylim(0, y_max_2+0.05)
    plt.plot(x_axis_1, y_axis_1, label = "original_model", color = "blue")
    plt.plot(x_axis_2, y_axis_2, label = "modified_model", color = "red")
    plt.axvline(x=0, color = "gray", linestyle="dashed")
    plt.legend()
    plt.savefig("{}plots/norm_test_fig.png".format(out_path))

if __name__=='__main__': #If this program is run directly
    main()