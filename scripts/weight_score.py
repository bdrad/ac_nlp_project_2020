## Apply different weights for each doc based on user input (if any)

import pandas as pd
import csv
from util_fxns import get_cat_name

scans_f = '../resources/scans_categorized_v2.csv'
sex_f = '../resources/sex.csv'

# Read in file that maps a document to incidence of scans in the different body parts.
scans = pd.read_csv(scans_f, index_col = 0)

# Read in file that maps a document to applicability to either sex or both.
sex = {}
reader = csv.reader(open(sex_f))
for row in reader:
    if len(row)>1:
        key = row[0]
        sex[key] = row[1]

# Calculates different weights depending on user input
def weight_file(name, q_bodypart, q_age, q_sex, POS_WEIGHT = 5):
    b_part_weight = 1
    if q_bodypart and scans.loc[name.split('.')[0]+'.pdf', q_bodypart] > 0:
        b_part_weight = POS_WEIGHT

    pediatric_weight = 1
    if q_age and q_age<18 and get_cat_name(name) == 'Pediatric':
        pediatric_weight = 2
    elif q_age and q_age>=18 and get_cat_name(name) == 'Pediatric':
        pediatric_weight = 1/2

    sex_weight = 1
    if q_sex:
        if sex[name] == 'B':
            sex_weight = POS_WEIGHT
        elif q_sex in ['f','female']:
            if sex[name] == 'F':
                sex_weight = POS_WEIGHT
        elif q_sex in ['m','male']:
            if sex[name] == 'M':
                sex_weight = POS_WEIGHT

    return [b_part_weight, pediatric_weight, sex_weight]
