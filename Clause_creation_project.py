
# coding: utf-8

# In[10]:


import re
import sys
file_name = sys.argv[1]

text = open(file_name).read() #Read the document


# In[2]:


text = text.replace('\t',' ').split('\n')
text = [x.strip(' ') for x in text if x] #Ignore empty newlines


# In[3]:


def get_index_and_clauses(text):
    all_clauses = []
    indexes = []

    ptns = ['.', '(']
    ptns_1 = ['1','2','3', '4','5','6','7','8','9','0']
    ptns_2 = ['(']
    ptns_3 = ['A','B','C','D','E','F','G','H','I','J','K']
    exp_1 = re.compile(r'\d+(\.\d+)')
    exp_2 = re.compile(r'\d+(\.)')

    for sentence in text:
        res = any([ p in s for p in ptns for s in sentence.split(' ')[:3] ]) # Initial filter; Need not check every sentene for every pattern.
        if res:
            all_clauses.append(sentence) # Extract potential clauses
            
            # Get indexing of the clause to which type of pattern the index might belong to
            if (exp_1.search(sentence.split(' ')[0]) or exp_1.search(sentence.split(' ')[1])):
                indexes.append('5')
                continue
            if exp_2.search(sentence.split(' ')[0]):
                indexes.append('2')
                continue
            if any([ p in s for p in ptns_1 for s in sentence.split(' ')[:2] ]):
                indexes.append('1')
                continue
            if any([ p in s for p in ptns_3 for s in sentence.split(' ')[:2] ]):
                indexes.append('3')
                continue
            if any([ p in s for p in ptns_2 for s in sentence.split(' ')[:2] ]):
                indexes.append('4')
                
    return indexes,all_clauses


# In[7]:


def get_clause_tree(index,clauses):
    
    main_list = []
    temp_list = []
    temp_val_list = []
    
    if len(index) == 0:
        return None
    
    temp_list.append(index[0])
    temp_val_list.append(clauses[0])
    
    # Check for same level sub clauses under a clause
    for i,val in enumerate(index[1:]):
        if val == temp_list[0]:
            
            returns = get_clause_tree(temp_list[1:],temp_val_list[1:]) # Generate tuple of the clause and its sub clauses
            if returns is None:
                to_append = (temp_val_list[0])
            else:
                to_append = (temp_val_list[0],returns)
            
            main_list.append(to_append)
            temp_list = []
            temp_val_list = []
        else:
            pass
        temp_list.append(val)
        temp_val_list.append(clauses[i+1])
    
    returns = get_clause_tree(temp_list[1:],temp_val_list[1:]) # Generate tuple of the clause and its sub clauses
    if returns is None:
        to_append = (temp_val_list[0])
    else:
        to_append = (temp_val_list[0],returns)
    main_list.append(to_append)
    return main_list


# In[8]:


# Get indexes and clause lists
indexes,all_clauses = get_index_and_clauses(text)

#Get the tree structure of the clauses
clauses_tree = get_clause_tree(indexes,all_clauses)


# In[9]:


# Final clauses tree
from pprint import pprint
pprint(clauses_tree)

