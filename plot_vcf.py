import matplotlib.pyplot as plt
import statistics
import sys

def main():
    id_file = sys.argv[1]
    case_path = sys.argv[2] #Path to the VCF-files
    output_path = sys.argv[3] #Path to the figures
    rank_model_ver = sys.argv[4] #Name of the rank model
    threshold = int(sys.argv[5]) #Rank score threshold.
    is_trios = sys.argv[6] #Type yes (case sensitive) if the cases are trios.
    make_plots(id_file, case_path, output_path, rank_model_ver, threshold, is_trios)

def make_plots(id_file, case_path, output_path, rank_model_ver, threshold, trios = "yes"):
    #Extract the data from the file.

    IDs = open(id_file)
    score_dict = {} #{score: frequency}
    caus_rank_dict = {} #{rank: frequency}
    caus_scores = []
    above_frequencies = []
    id_name_list = []
    for ID in IDs:
        above = 0
        ID = ID.strip()  
        id_name_list.append(ID)    
        data_file = open("{}{}_data.txt".format(case_path, ID))
        for line in data_file:
            line = line.strip()
            if line[0] != "#":
                line = line.strip()
                line = line.split(sep=";")
                position = line[0]
                rank = int(line[2]) 
                score = int(line[3])

                if score in score_dict:
                    score_dict[score] += 1
                else:
                    score_dict[score] = 1

                if position[0] != "M": #If it's not a mitochondrial variant.
                    if score >= threshold:
                        above += 1
                else:
                    if score >= 12:
                        above += 1


                if line[1] == "True":
                    caus_scores.append(score)
                    if rank in caus_rank_dict:
                        caus_rank_dict[rank] += 1
                    else:
                        caus_rank_dict[rank] = 1
        above_frequencies.append(above)
        data_file.close()
    IDs.close()
    missed_causatives = 0
    for i in caus_scores:
        if i < threshold:
            missed_causatives += 1

    #Plot the ranks of the causative variants.
    x = []
    y = []
    for c in caus_rank_dict:
        x.append(c) #Ranks
        y.append(caus_rank_dict[c]) #Frequencies
        plt.figure(figsize=(7, 6))
    plt.bar(x, y, color = "darkslateblue")
    plt.xlabel("Variant rank\nKnown causative variants that did not reach the threshold: {}".format(missed_causatives))
    plt.ylabel("Frequency")
    plt.suptitle("Rank model v.{}".format(rank_model_ver))
    plt.title("Variants deemed causative under rank model ver 5.2.1.")
    plt.xticks([x[i] for i in range(len(x)) if i % 1 == 0])
    y_max = max(y)
    for element in range(len(x)):
        t = plt.text(x[element], y_max*0.05, y[element], ha = "center") # type: ignore #Add the number of variants in each bar, 1.5 and ha = center denote the position of the text, and y[element] is the number of variants in x[element]
        t.set_bbox(dict(facecolor = "white", alpha=0.5, linewidth = 0.5))
    if trios == "yes":
        plt.savefig("{}causative_variant_rank_v.{}_trios.png".format(output_path, rank_model_ver))
    else:
        plt.savefig("{}causative_variant_rank_v.{}.png".format(output_path, rank_model_ver))
    plt.close()

    #Plot the variants above vs below the score threshold for each case.
    id_name_list = sorted(id_name_list)
    case_counter = 0
    new_names_case_list = []
    for case in id_name_list:
        case_counter += 1
        new_names_case_list.append("Case {}".format(case_counter))
        
    average_above = sum(above_frequencies)/len(above_frequencies)
    stdev_above = statistics.stdev(above_frequencies)

    fig, ax = plt.subplots()
    ax.bar(new_names_case_list, above_frequencies, color = "olivedrab")
    ax.set_title("Rank model v.{}".format(rank_model_ver))
    ax.set_ylabel("Frequency")
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')

    textstr = '\n'.join((r'$\mu=%.2f$' % (average_above, ), r'$\sigma=%.2f$' % (stdev_above, )))

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='olivedrab', alpha=0.1)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    fig.set_figwidth(9)
    plt.tight_layout()
    if trios == "yes":
        plt.savefig("{}rank_score_thresh_v.{}_trios.png".format(output_path, rank_model_ver))
    else:
        plt.savefig("{}rank_score_thresh_v.{}.png".format(output_path, rank_model_ver))
    plt.close()


if __name__=="__main__": #If this program is run directly
    main()