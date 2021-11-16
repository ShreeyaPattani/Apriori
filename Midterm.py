import pandas as pd
import itertools

class App1:

    def generate_frequent_itemset(self, itemlist, size, previous_frequent_itemset = []):
        
        if size == 1:
            candidateset = {}
            for item_set in itemlist:
                for item in item_set:
                    candidateset[item] = (candidateset[item] if candidateset.__contains__(item) else 0 ) + item_set.count(item)
            self.item_list = {item:candidateset[item] for item in list(candidateset.keys()) if (candidateset[item]/len(candidateset)*100) >= self.minimum_support }
            return candidateset, {item:candidateset[item] for item in list(candidateset.keys()) if (candidateset[item]/len(candidateset)*100) >= self.minimum_support }
        else:
            previous_frequent_itemset = (list(previous_frequent_itemset.keys()))

            previous_frequent_itemset_combinations = sorted(list(set([item for a in previous_frequent_itemset for item in a]))) if size > 2 else sorted(previous_frequent_itemset)            

            previous_frequent_itemset_combinations = list(itertools.combinations(previous_frequent_itemset_combinations, size))

            candidate = {}

            frequent_itemset = {}

            for item in previous_frequent_itemset_combinations:
                count = 0
                for iter2 in itemlist:
                    if check_sub_lists(item, iter2):
                        count+=1
                candidate[item] = count
            for key, value in candidate.items():
                if (value/len(candidate)*100) >= self.minimum_support:
                    if subset_frequency(key, previous_frequent_itemset, size-1):
                        frequent_itemset[key] = value 
                        self.item_list[key] = value
    
            return candidate, frequent_itemset
            pass
        pass

    def get_frequent_itemset(self):
        size = 1
        res = {}
        while True:
            can, res = self.generate_frequent_itemset(self.dataset, size, previous_frequent_itemset=res)
            print(f"\n \n Freq Itemset Size {size} : {res}")
            if res and size > 1:
                self.frequent_itemsets.append({"size": size, "itemset": res})
            if not res:
                break
            size+=1
        pass

    def __init__(self,data,minimum_support,minimum_confidence):
        #import dataset
        self.dataset = pd.read_csv(data)
        self.dataset = sorted([[row[column] for column in list (self.dataset) if str(row[column]) != 'nan'] for index, row in self.dataset.iterrows()])
        self.minimum_support = minimum_support
        self.minimum_confidence = minimum_confidence
        self.frequent_itemsets = []
        self.item_list = {}
        self.association_rules = []

    def generate_association_rules(self):
        self.get_frequent_itemset()
        association_rules = []
        for itemset in self.frequent_itemsets:
            print(f" \n \n Itemset size {itemset['size']}")
            rules = []
            for item in list(itemset['itemset'].keys()):
                subsets = list(itertools.combinations(item, itemset['size'] - 1)) if itemset['size'] - 1 > 1 else [it for it in item]
                rules.append(subsets)
            itemset_keys = list(itemset["itemset"].keys())
            for i in range(0, len(itemset_keys)):
                for iter1 in rules[i]:
                    a = iter1
                    b = set(itemset_keys[i]) - (set(iter1) if itemset["size"] > 2 else set({iter1}))
                    confidence = (get_support(itemset_keys[i], self.item_list)/get_support(iter1, self.item_list))*100
                    if confidence >= self.minimum_confidence:
                        print("{} -> {} = ".format(a,b), confidence)
        pass

    def ouput(self):
        pass

def check_sub_lists(list1, list2):
    list1 = list(list1)
    list2 = sorted(list2)
    sub_lists = []
    for L in range(0, len(list2)+1):
        for subset in itertools.combinations(list2, L):
            sub_lists.append(list(subset))
    return True if list1 in sub_lists else False

def subset_frequency(itemset, candidate_set, size):
    if size > 1:    
        subsets = list(itertools.combinations(itemset, size))
    else:
        subsets = itemset
    for item in subsets:
        if not item in candidate_set:
            return False
    return True
    pass

def get_support(itemset, itemlist):
    return itemlist[itemset]

def main():
    minimum_support = int(input('Please enter minimum support \n'))
    minimum_confidence = int(input('Please enter minimum confidence \n' ))
    a = int(input('Choose and enter number from the menu:\n1]Amazon\n2]Best Buy\n3]Generic\n4]Kmart\n5]Nike\n'))
    if a == 1:
        apriori_obj = App1('AmazonDataset.csv',minimum_support, minimum_confidence)
        apriori_obj.generate_association_rules()
    elif a == 2:
        apriori_obj = App1('BestBuyDataset.csv',minimum_support, minimum_confidence)
        apriori_obj.generate_association_rules()
    elif a == 3:
        apriori_obj = App1('GenericDataset.csv',minimum_support, minimum_confidence)
        apriori_obj.generate_association_rules()  
    elif a == 4:
        apriori_obj = App1('KmartDataset.csv',minimum_support, minimum_confidence)
        apriori_obj.generate_association_rules() 
    else :
        apriori_obj = App1('NikeDataset.csv',minimum_support, minimum_confidence)
        apriori_obj.generate_association_rules()     

    pass

if __name__ == '__main__':
    main()