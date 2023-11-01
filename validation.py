import numpy as np
import scipy.stats
import sys
from statsmodels.stats.weightstats import ztest as ztest
import statsmodels.api as sm
import matplotlib.pyplot as plt

def main():
    ID_file = sys.argv[1] #ID list
    model_name = sys.argv[2] #Model name
    input_dir = sys.argv[3] #Input directory with the data text files.
    output_dir = sys.argv[4] #Output directory
    threshold = int(sys.argv[5]) #Rank score threshold

    scores_dict = get_scores_thresh(ID_file, input_dir, threshold) 
    scores = list(scores_dict.values())
    scores = (scores,)
    bootstrap_result = scipy.stats.bootstrap(scores, np.mean, confidence_level=0.95, method='percentile') # type: ignore #Run 9999 bootstrap runs and save the results in bootstrap_results.
    print("The 95{} confidence interval for rank model ver.{}".format("%", model_name))
    print(bootstrap_result.confidence_interval)
    print("Bootstrap standard error: {}".format(bootstrap_result.standard_error))
    print("")
    out = open("{}{}_validation_result.txt".format(output_dir, model_name), "w")
    out.write("Rank model ver.{}\n".format(model_name))
    out.write("The 95{} confidence interval for rank model ver.{}\n".format("%", model_name))
    out.write("{}\n".format(bootstrap_result.confidence_interval))
    out.write("Bootstrap standard error: {}\n".format(bootstrap_result.standard_error))
    out.write("Bootstrap mean of means: {}".format(sum(bootstrap_result.bootstrap_distribution)/len(bootstrap_result.bootstrap_distribution)))
    out.close()
    out_2 = open("{}{}_bootstrap_means.txt".format(output_dir, model_name), "w")
    out_2.write("#Bootstrap results (mean value of every run)\n".format(bootstrap_result.bootstrap_distribution))
    for mean in bootstrap_result.bootstrap_distribution:
        out_2.write("{}\n".format(mean))
    out_2.close()
    fig = sm.qqplot(bootstrap_result.bootstrap_distribution, line='s')
    plt.savefig("{}_test_of_norm.png".format(output_dir, model_name)) #QQ-plot
    plt.close()

def get_scores_thresh(id_file, input_path, threshold):
    score_dict = {} #{ID: nr_above}
    ID_file = open(id_file)
    for ID in ID_file:
        ID = ID.strip()
        score_dict[ID] = 0
        data_file = open("{}{}_data.txt".format(input_path, ID))
        for line in data_file:
            line = line.strip()
            if line[0] != "#":
                line = line.split(sep=";")
                position = line[0]
                score = int(line[3])
                if position[0] != "M": #If it isn't a mt-variant.
                    if score >= threshold:
                        score_dict[ID] += 1
                else:
                    if score >= 12:
                        score_dict[ID] += 1
    ID_file.close()
    return score_dict


if __name__=="__main__": #If this program is run directly
    main()