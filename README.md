
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Distant_and_ancient_SPT0615-JD.jpg/960px-Distant_and_ancient_SPT0615-JD.jpg"
     alt="Distant and ancient SPT0615-JD"
     width="30%">

# Scope
This project contains the files for the academic project for the course *Computational Linear Algebra for Large Scale problems* focused on **Principal Component Analysis**.  

The aim of the present project is In this homework, we A dataset characterizing **galaxy** observations is used to estimate the corresponding **redshift**. This dataset is given by approximately three thousands of records
described by 65 attributes, and it is based on the on the public catalog of Wolf et al. (2004).
By exploiting PCA, it is possible to reduce the number of features and therefore improve machine learning algorithms based on distance computations, such as
K-Nearest Neighbors.

Mathematical topics involved: *Standardization*, *PCA* and *Reconstruction errors*, *KNN algorithm*.

The [PCA_for_redshift_estimation](PCA_for_redshift_estimation.pdf) pdf contains a detailed report with mathematical explanation and implementation details. In particular, an intepretation of the
components meaning is performed as an example of use case where it is possible to get insights about correlated features as side-product for PCA (example: "what may an interpretation of the first PC be?")

# Language
The code is developed entirely in Python 3.9.

# Dataset
An explanation of the available features is available in the file [DATA_EXPLANATION.md](DATA_EXPLANATION.md)

# Instruction
1. Create a virtual environment and install dependencies (example using venv and pip)
```
python -m venv pcaenv
pcaenv\Scripts\activate
pip install -r requirements.txt
```

2. Split the dataset into train and test
```
python redshift_data_split.py
```

3. Run the main code
```
python redshift_estimation.py
```

## How to replicate the results from the report
- When asked to choose between standardized / original data, choose original data ("1")
- Keep the hardcoded values from the code, i.e.:
    |Variable name | Value | Description |
    |--------------|-------|-------------|
    | seed | 291251 |         seed for dataset split|
    | max_components | 10 |   max number of components to consider|
    | k | 6 |                 the number of principal components to achieve 99% of explained variability|
    | threshold | 0.01 |      min threshold to consider a feature as significant for the component under examination|

# Author
Corrado Navilli