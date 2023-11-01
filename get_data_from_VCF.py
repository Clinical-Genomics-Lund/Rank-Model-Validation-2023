from find_filename import find_filename
import re
import gzip
import sys
import scout_class as sc

def main():
    ids = sys.argv[1] #A txt file with all the Lab IDs, one ID for each row.
    inp_path = sys.argv[2] #The directory of the VCF files.
    scores_dict = get_score_data(ids, inp_path)
    add_ranks(ids, scores_dict, inp_path) #Add the rank of each variant. In this script, each variant with the same score will recieve the same rank.


def get_score_data(id_file, case_path):
    score_dict = {}
    ID_file = open(id_file)
    for ID in ID_file:
        ID = ID.strip()
        case_doc = sc.case_documents(ID)
        causatives = case_doc.get_position() #Get the position for the variant IF the variant
        case_filename = find_filename(ID, case_path)
        case_vcf = gzip.open("{}{}".format(case_path, case_filename), mode='rb')
        case_output = open("{}{}_data_temp.txt".format(case_path, ID), "w")
        header_added = False #A variable which makes sure that the header isn't added to the output more than once.
        scores = set()
        for line in case_vcf:
            is_causative = False
            line = str(line)
            line = line[2:-3]
            if line[0] == "#" and "RankResult" in line:
                if header_added == False:
                    result_pattern = re.compile(r'".*?["]')
                    desc = re.findall(result_pattern, line)
                    desc = desc[0][1:-1]
                    case_output.write("#Position;Causative;Rank;Score;Score Details\n#Score Details: {}\n".format(desc)) #Add the header
                    header_added = True
            if line[0] != "#" and "RankScore" in line:
                line_list = line[0:100]
                line_list = re.split(r'\\t', line)
                chrom = line_list[0]
                pos = line_list[1]
                ref = line_list[3]
                alt = line_list[4]
                if int(pos) in causatives:
                    is_causative = True
                position = "{}:{}_{}_{}".format(chrom, pos, ref, alt) #Chromosome:Position_Reference_Alternative

                #Rank score.
                rank_score_pattern = re.compile(f"RankScore={ID}:.*?[;]") #Find the rank score in the line, including RankScore=.
                rank_score_inner_pattern = re.compile(r":.*?[;]") #Find the rank score number within the previous pattern.
                rank_score = str(re.findall(rank_score_pattern, line)) 
                rank_score = str(re.findall(rank_score_inner_pattern, rank_score)) #Note that the string will begin with [ and end with ]. 
                rank_score = str(rank_score[3:-3])
                try:
                    if rank_score not in scores:
                        scores.add(int(rank_score))
                except:
                    print(ID)
                    print(pos)
                    print(rank_score)
                #Rank score details.
                rank_result_pattern = re.compile(r"RankResult=.*?(?=\\t)")
                rank_result = re.findall(rank_result_pattern, line)
                rank_result = rank_result[0][11:] #Exclude the RankResult= bit of the match.
                
                case_output.write("{};{};{};{};{}\n".format(position, is_causative, "placeholder", rank_score, rank_result))
        case_vcf.close()
        case_output.close()
        scores = sorted(scores, reverse = True)
        score_dict[ID] = scores
    ID_file.close()
    return score_dict

def add_ranks(id_list, score_dict, case_path): 
    ID_file = open(id_list)
    for ID in ID_file:
        ID = ID.strip()
        scores = score_dict[ID]
        scores = list(scores)
        scores = sorted(scores, reverse=True)
        case_data_old = open("{}{}_data_temp.txt".format(case_path, ID))
        #Get the scores in a list, sort the scores, assign ranks, add ranks to dict.
        case_ranks = list(range(1, len(scores)+1))
        case_data_old.close()
        
        case_data_old = open("{}{}_data_temp.txt".format(case_path, ID))
        case_data_new = open("{}{}_data.txt".format(case_path, ID), "w")
        for line in case_data_old:
            if line[0] == "#":
                case_data_new.write(line)
            else:
                line = line.strip()
                line = line.split(sep=";")
                score_index = scores.index(int(line[3]))
                rank = case_ranks[score_index]
                case_data_new.write("{};{};{};{};{}\n".format(line[0], line[1], rank, line[3], line[4]))
        case_data_new.close()
        case_data_old.close()
    
    ID_file.close()

    
if __name__=="__main__": #If this program is run directly
    main()