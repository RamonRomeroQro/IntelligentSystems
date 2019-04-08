from collections import defaultdict, Counter
from copy import deepcopy
import math

class DataSet():
    ''' Data set class abstractiion'''
    def __init__(self):
        self.relationship_name=""
        self.attributes={}
        self.list_attributes=[]
        self.info = defaultdict(list) # arr row
        self.listed_info = [] #arr dic
        
    def update_from_input(self):
        ''' Read from input '''
        while (1):
            try:
                read_line = str(input()).strip()
                if read_line == "":
                    pass
                elif read_line.startswith("%"):
                    pass
                else:
                    if read_line.startswith("@relation"):
                        read_line=read_line.split(" ")
                        self.relationship_name=read_line[1]
                    elif read_line.startswith("@attribute"):
                        read_line=read_line.split()
                        attribute_name=read_line[1]
                        self.list_attributes.append(attribute_name)
                        unparsed_possibilities=read_line[2:]
                        possibilities = [ x.strip('{').strip('}').strip(',') for x in unparsed_possibilities ]
                        self.attributes[attribute_name]= set(possibilities)
                    elif read_line.startswith("@data"):
                        while(1):
                            try:
                                read_data=str(input()).strip()
                                if read_data.startswith('@'):
                                    pass
                                elif read_data.startswith('%'):
                                    pass
                                else:
                                    read_data=[e.strip() for e in read_data.split(",")]
                                    listed_element={}
                                    for i in range(len(self.list_attributes)):
                                        self.info[self.list_attributes[i]].append(read_data[i])
                                        listed_element[self.list_attributes[i]]=read_data[i]
                                    self.listed_info.append(listed_element)
                                    
                            except EOFError:
                                break
            except EOFError:
                break

import pandas as pd
def main():
    data_set=DataSet()
    data_set.update_from_input()
    f = open("qk.csv", "w+")
    f.write(",".join(data_set.list_attributes)+"\n")
    f.write("\n".join([",".join([v for v in i.values()]) for i in data_set.listed_info]))
    f.close()
    df=pd.read_csv("qk.csv", delimiter=',')
    # calc entropia del dataset
    counter=df[df.columns[-1]].value_counts().to_dict()
    total=df[df.columns[-1]].count()
    print(counter, total)
    entropy_dataset=0
    for v2 in counter.values():
        entropy_dataset=entropy_dataset+((v2/total)* math.log2(v2/total))
    entropy_dataset=(entropy_dataset*-1)
    print(entropy_dataset)
    ###
    for i in data_set.list_attributes[:-1]:
        print(df.groupby([i]).count())









if __name__ == "__main__":
    main()