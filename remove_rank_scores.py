import re
import sys
from find_filename import find_unzipped_filename

def main():
    #The input VCF file needs to be unzipped for this script!
    ID_list = sys.argv[1]
    inp = sys.argv[2]
    out = sys.argv[3]
    remove_scores(ID_list, inp, out)

def remove_scores(ID_file, inp_folder, out_folder):
    ID_list = open(ID_file)

    for ID in ID_list:
        ID = ID.strip()
        filename = find_unzipped_filename(ID, inp_folder)
        inp = open("{}{}".format(inp_folder, filename), "r")
        out = open("{}{}".format(out_folder, filename), "w")
        for line in inp: #Only adds lines from the VCF that don't contain a score or has had their scores removed.
            if "RankScore" in line or "RankResult" in line:
                if line[0] != "#":
                    pattern = re.compile(r";RankScore=.*?[\t]") #Find the rank score field, including the following tabulator.
                    line_noscore = re.sub(pattern, "\t", line) #Replace the pattern with a tabulator.
                    if "Compounds" in line:
                        outer_comp_pattern = re.compile(r"Compounds=.*?;")
                        comp_field = re.findall(outer_comp_pattern, line_noscore)
                        comp_field=comp_field[0]
                        inner_comp_pattern_1 = re.compile(r"[>].*?[|]")
                        inner_comp_pattern_2 = re.compile(r"[>].*?[;]")
                        comp_field = re.sub(inner_comp_pattern_1, "|", comp_field)
                        comp_field = re.sub(inner_comp_pattern_2, ";", comp_field)
                        line_noscore = re.sub(outer_comp_pattern, comp_field, line_noscore)
                    out.write("{}".format(line_noscore))
            else:
                out.write("{}".format(line))
        inp.close()
        out.close()
    ID_list.close()

if __name__=="__main__": #If this program is run directly
    main()