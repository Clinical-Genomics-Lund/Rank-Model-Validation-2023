import sys
import matplotlib.pyplot as plt

def main():
    model_name = sys.argv[1]
    input_dir = sys.argv[2]
    output_dir = sys.argv[3]
    bootstrap_plots(model_name, input_dir, output_dir)
    
def bootstrap_plots(model_name, input_dir, output_dir):
    bootstrap_means = []

    inp = open("{}{}_bootstrap_means.txt".format(input_dir, model_name))
    for mean in inp:
        if mean[0] != "#":
            mean = mean.strip()
            bootstrap_means.append(float(mean))
    inp.close()
    bin_nr = int(0.5+((len(bootstrap_means)**0.5)/2)) #Nr of bins for the histogram should be the half the square root of the number of data points.
    fig = plt.hist(bootstrap_means, bins=bin_nr)
    plt.savefig("{}{}_bootstrap_means.png".format(output_dir, model_name))
    plt.close()

if __name__=="__main__": #If this program is run directly
    main()