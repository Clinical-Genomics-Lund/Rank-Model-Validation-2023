import pymongo

#Note that all of this script is hardcoded for the database we use in Lund!

mongodb_name = "placeholder" #Should be replaced with your own database.

myclient = pymongo.MongoClient(mongodb_name) #Open the MongoDB database.

scout_db = myclient.scout #Use the scout database.
case_db = scout_db.case #Look at the case collection. Contains information about each case. The gene panel list contain information about the suspected genes.
variant_db = scout_db.variant #Contains the rank score for each variant! Each variant document is unique for each patient (case).

class case_documents:
    def __init__(self, id):
        self.doc = case_db.find_one({"_id": id, "owner": "klingen_38"})
        self.status = self.doc["status"] # type: ignore
        self.causative = ""
        self.error = False

    #Case collection: extract information about each case.
    def get_date(self):
        date = str(self.doc["analysis_date"].date()) # type: ignore
        date = date.rsplit("-")
        for i in range(len(date)):
            date[i] = int(date[i]) # type: ignore
        return(date)

    #Variant collection: extract information about causative variants.
    def get_variant(self):
        if self.status == "solved" and "causatives" in self.doc and len(self.doc["causatives"]) > 0: #If the case is solved, grab the data from the causative list. # type: ignore
            #The causative list must not be empty and must contain at least one element.
            causative = self.doc["causatives"][0] # type: ignore
            var_tuples = []
            if len(self.doc["causatives"]) > 1: #If there are more than one causative variant, choose the one with the highest variant rank. # type: ignore
                for var_id in self.doc["causatives"]: #For every causative variant, add their id and variant rank to a tuple. # type: ignore
                    var = variant_db.find_one({"_id": var_id, "owner": "klingen_38"}) # type: ignore
                    if var != None: #If the variant can be found.
                        var_tuples.append((var["variant_rank"], var_id))
                if len(var_tuples) > 1: #If more than one variant could be found in the causatives list.
                    var_tuples.sort() #Sort the tuple based on variant rank (descending order)
                    causative = var_tuples[0][1] #Choose the variant with the highest rank (lowest variant rank value)
            self.causative = variant_db.find_one({"_id": causative}) # type: ignore
            if self.causative == None: #If no variants can be found.
                self.error = True
                return self.error
            else:
                return self.causative
        else:
            self.error = True
            return self.error

    def get_variant_id (self):
        x = self.get_variant()
        if self.error != True:
            return x["_id"] # type: ignore

    def get_rank_score(self): #Get the rank score.
        x = self.get_variant()
        if self.error != True and "rank_score" in self.causative: # type: ignore
            return x["rank_score"] # type: ignore
        else:
            return self.error

    def get_rank_score_results(self): #Get a more detailed view of the rank scores for each category.
        x = self.get_variant()
        if self.error != True and "rank_score_results" in self.causative: # type: ignore
            return x["rank_score_results"] # type: ignore
        else:
            return self.error

    def get_variant_rank(self): #Get the the rank of the variant in relation to the other variants. Higher rank scores gve higher ranks.
        x = self.get_variant()
        if self.error != True and "variant_rank" in self.causative: # type: ignore
            return x["variant_rank"] # type: ignore
        else:
            return self.error
        
    def get_sub_category(self):
        x = self.get_variant()
        if self.error != True:
            return x["sub_category"] #A string which explains what type of variant it is, such as an indel or a snv. # type: ignore
        else:
            return self.error

    def get_position(self): #Get the position of the variant. Used to find the causative variant(s) in the VCF file. We want this to work for all causative variants.
        causative_positions = []
        for i in (self.doc["causatives"]): # type: ignore
            x = variant_db.find_one({"_id": i}) # type: ignore
            causative_positions.append(x["position"]) # type: ignore
        return causative_positions #Returns a list of the positions for all the causative variants.

