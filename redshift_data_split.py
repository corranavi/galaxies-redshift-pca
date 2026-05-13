"""
This script load the original dataset and splits it into 2 subsets (training-eval).
The new subsets are then saved as csv, therefore it is not necessary to run this script more than once.
"""

import numpy as np
import pandas as pd

data_full = pd.read_csv(r"data/COMBO17.csv")

print(data_full.shape)
seed = 291251
print("Randomseed: ",seed)
np.random.seed(seed)
sub_dataset_index=np.random.choice(    data_full.index,2500, replace=False)
eval_dataset_index= [index for index in data_full.index if index not in sub_dataset_index]
sub_dataset = data_full.loc[sub_dataset_index].copy()
eval_dataset = data_full.loc[eval_dataset_index].copy()
assert len(data_full)==(len(sub_dataset)+len(eval_dataset))

save_path_train=r"data/COMBO17pca.csv"
save_path_eval = r"data/COMBO17eval.csv"

sub_dataset.to_csv(save_path_train, index_label='index')
eval_dataset.to_csv(save_path_eval, index_label='index')

print(f"Split completed. The file 'COMBO17pca' contains"
      f" {len(sub_dataset)} rows, the file 'COMBO17eval' contains"
      f" {len(eval_dataset)} rows.")