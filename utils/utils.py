"""
This script contains utilities for the PCA project.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ndim=1
pc1=0
pc2=None
pc3=None

def get_plot_choice() -> tuple:
    """Retrieve the plotting choices of the user. Currently not in use in the main script."""
    ndim=1
    pc1=0
    pc2=None
    pc3=None
    print("How many dimensions do you want to plot?")
    ndim=input()
    if ndim=='1':
        print("What is the first PC? [0,1,2, ...]")
        pc1=input()
        return ndim, pc1
    elif ndim=='2':
        print("What is the first PC? [0,1,2, ...]")
        pc1 = input()
        print("What is the second PC? [0,1,2, ...]")
        pc2 = input()
        return ndim, pc1,pc2
    else:
        print("What is the first PC? [0,1,2, ...]")
        pc1 = input()
        print("What is the second PC? [0,1,2, ...]")
        pc2 = input()
        print("What is the third PC? [0,1,2, ...]")
        pc3 = input()
        return  ndim, pc1, pc2, pc3
    return None


def plot_projected_data(i, ndim: int, Qm: pd.DataFrame, colors: str, 
                        pc1: int, pc2:int=None, pc3:int=None, savefig:bool=False) -> None:
    """Plot the projected data on image i, given ndim (number of PC) and Qm data. Choose the colors and the first PC.
    If ndim > 1, define also up to two more components. Optionally, save the plot as png."""
    if ndim==1:
        plt.figure(i)
        plt.scatter(Qm[:, pc1], np.zeros_like(Qm[:, pc1]), c=colors)
        plt.axhline(ls='--', lw=0.5)
        plt.axvline(ls='--', lw=0.5)
        title="1D visualization for PC"+ str(pc1 + 1)
        plt.title(title)
    elif ndim==2:
        plt.figure(i)
        plt.scatter(Qm[:, pc1], Qm[:, pc2], c=colors)
        plt.axhline(ls='--', lw=0.5)
        plt.axvline(ls='--', lw=0.5)
        title = "2D visualization for PCs " + str(pc1 + 1)+", "+str(pc2+1)
        plt.title(title)
    else:
        fig3D=plt.figure(i)
        ax = fig3D.add_subplot(111, projection='3d')
        ax.scatter(Qm[:, pc1], Qm[:, pc2], Qm[:, pc3], c=colors)
        title="3D visualization for PCs "+str(pc1 + 1)+", "+str(pc2 + 1)+", "+str(pc3 + 1)
        plt.title(title)
    plt.show()
    if savefig:
        plt.savefig(title + ".png")
    return None

def remove_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Set 'index' column as index and remove column 'Nr'"""
    df.set_index(df['index'], inplace=True)
    df.drop(["index", "Nr"], axis=1, inplace=True)
    return df


def get_features_targets(df: pd.DataFrame) -> tuple:
    """Split the column names to be used as features and as targets."""
    targets=['Mcz', 'e.Mcz', 'MCzml','chi2red']
    features=[label for label in df.columns  if label not in targets]
    return features, targets


def mean_relative_error(actuals: float, predicted: float) -> float:
    """Compute MRE"""
    return np.sum(abs(predicted-actuals)/abs(actuals))*(1/len(actuals))


def get_choice_standardization() -> bool:
    """Get the user choice for standardize data or use original format. Alternative to command line input for
    user friendly interaction. """
    standardize= False
    valid=False
    while not valid:
        print("Do you want to use original data or apply standardization? [1 for original, 2 for standardized]")
        choice=input()
        if choice=='1':
            print('Ok, by using original data the COVARIANCE MATRIX will be used to compute PCA.\n')
            valid=True
        elif choice=='2':
            print("Ok, by using standardized data the CORRELATION MATRIX will be used to compute PCA.\n")
            valid=True
            standardize= True
        else:
            print('You did not input a valid choice.\n')
            valid=False
    return standardize