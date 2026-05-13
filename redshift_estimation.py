#Computation
import pandas as pd
import numpy as np
import time
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor

#import custom library written for the project
import utils as u

#Visualization
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    #Import of data and preparation
    file_name="COMBO17pca.csv"
    load_path= os.path.join("data/",file_name)
    type="cov"           #used for the name of the saved images
    max_components=10
    k=6                 #number of components for reaching 99%
    img_count=1
    threshold=0.1

    # Import data from csv
    data=pd.read_csv(load_path)
    data=u.remove_columns(data)
    data.describe()
    dict_means={ }
    features, targets = u.get_features_targets(data)
    data_original=data.copy()

    standardize=u.get_choice_standardization()

    scaler = StandardScaler()
    df_standardized = pd.DataFrame(scaler.fit_transform(data[features]), columns=features)

    #Removal of outliers
    print("Original dataset has ",df_standardized.shape[0]," rows.")
    z_scores = np.array(np.abs(df_standardized))
    outlier_indices = np.where(z_scores > 3)
    indices_droppanda=list(set(outlier_indices[0]))
    data=data.drop(data.index[indices_droppanda])
    print("Dataset after outlier removal has ",data.shape[0], " rows.")

    if standardize==True:
        #using the standardized matrix as source and setting some variable values
        df_standardized = pd.DataFrame(scaler.fit_transform(data[features]), columns=features, index=data.index)
        data=df_standardized[features].merge(data[targets],left_index=True, right_index=True, how='left')
        type="corr"
        max_components=30
        k=30                #number of components for reaching 99% #29 without removal of outliers (lost 400 datapoints)

        print("Standardization applied on features columns.")

    print("\nMissing values analysis.")
    list_empties=[]
    for col in data.columns:
        percentage_empty=sum(data[col].isna())/len(data[col])
        if percentage_empty>0:
            list_empties.append((col, 1-percentage_empty))

    print('The following columns present missing values: ')
    for name,percentage_full in list_empties:
        print(name,": ",(1-percentage_full)*100,"%")


    #filling missing values
    for col in data.columns:
        dict_means[col]=data[col].mean()
        data[col].fillna(inplace=True,value=dict_means[col])
    print("\nMissing value filled with mean values.\n")

    S=data[features].values


    #---------------PCA FULL -----------------------------------------------------------
    print("PCA full will now be performed.\n")
    pca_full= PCA(svd_solver='full')
    pca_full.fit(S)
    Qm_full=pca_full.transform(S)

    print("\n3- Visualizing PCA")
    print("\nFirst, we can look at the graphs of the cumulative explained variance ratio"
        " in order to evaluate the presence of knee point: ")


    #----- PLOTS ------------------------------------------------------------------------
    all_PCs=pd.Series(pca_full.explained_variance_ratio_, index=range(1,len(pca_full.explained_variance_ratio_)+1))
    cumsum_all=np.cumsum(all_PCs)
    plt.figure(img_count)
    plt.plot(cumsum_all)
    plt.title('Explained variance ratio of individual PCs and cumulative - all.')
    plt.show()
    img_count+=1

    print(f"\nIt can be seen that beyond the {max_components}th PC there is a plateau, therefore it would be "
        f"reasonable to focus on the first {max_components} PCs.")

    print("\nIn repeating the previous analysis we can add a barplot for analyzing the individual "
        "contribution of each PC.")
    top_PCs=pd.Series(pca_full.explained_variance_ratio_[:max_components], index=range(1,max_components+1))
    cumsum_top=np.cumsum(top_PCs)

    plt.figure(img_count)
    plt.plot(cumsum_top, color='orange')
    plt.bar(top_PCs.index, top_PCs)
    plt.hlines(y=0.99,  xmin=0.5,xmax=max_components+0.4, colors='black', linestyles="-.", lw=0.8, label='0.99')
    plt.hlines(y=0.95,  xmin=0.5,xmax=max_components+0.4, colors='black', linestyles="--", lw=0.8, label='0.95')
    plt.xticks(range(1,max_components+1))
    plt.title(f'Explained variance ratio of individual PCs and cumulative - top {max_components}.')
    plt.legend()
    plt.show()
    img_count+=1

    #-----------------------PLOTTING ONLY TOP MEANINGFUL PCs-----------------------------

    k=np.where(cumsum_top>=0.99)[0][0] #retrieving only those PC with at least 0.99 explained cumulative.
    print("We can notice the following, denoting with k the number of the first k PCs: \n"
        f"with k={k+1} we reach 99% of the total explained variability\n")

    pcs=[0,1,2,3,4]
    fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20, 16))
    for i in range(5):
        for j in range(5):
            if i > j:
                axes[i, j].scatter(Qm_full[:, pcs[j]], Qm_full[:, pcs[i]], c=data['Mcz'])
                axes[i, j].set_title(f'PC {pcs[j]+1} vs PC {pcs[i]+1}')  # Aggiungi +1 perché l'indice inizia da 0
                axes[i, j].axhline(y=0, ls='--', lw=0.5)
                axes[i, j].axvline(x=0, ls='--', lw=0.5)
            #elif i==j:
            #    axes[i, j].scatter(Qm_full[:, pcs[i]], np.zeros(len(pcs[i])), c=data['Mcz'])
            #    axes[i, j].set_title(f'PC {pcs[i]}')
            else:
                axes[i, j].axis('off')
    plt.tight_layout(h_pad=4.5, w_pad=1)
    plt.show()

    print("Plotting 1D for PC1, 2D for PC1 vs PC2, 3D for PC1 vs PC2 vs PC3")
    pc1,pc2,pc3=0,1,2
    u.plot_projected_data(img_count,1,Qm_full,data['Mcz'],pc1)
    img_count+=1
    u.plot_projected_data(img_count,2,Qm_full,data['Mcz'],pc1,pc2)
    img_count+=1
    u.plot_projected_data(img_count,3,Qm_full,data['Mcz'],pc1,pc2,pc3)
    img_count+=1

    #----------------------INTERPRETATIONS -----------------------------------------------
    #Only relevants
    print(f"\nInterpretation: \nbarplots for top {k+1} PCs are displayed.\n ")
    pc_list=[0,1,2,3,4,5]
    for pc_to_analyze in pc_list:
        xi_list=[]
        feat_list = []

        for xi,name in zip(pca_full.components_[pc_to_analyze],features):
            if(abs(xi)>=threshold):
                xi_list.append(xi)
                feat_list.append(name)

        plt.figure(img_count)
        plt.bar(range(len(xi_list)),
                xi_list,
                tick_label=feat_list)
        plt.title(f'Analysis of the component #{pc_to_analyze+1}')
        plt.show()
        img_count+=1

    #---------- KNN ALGORITHM -----------
    print("MACHINE LEARNING PHASE-------------------------------------\n")
    print(f"KNN using top {k+1} PCs (cumulative explained variability > 99% )")
    pca_k=PCA(n_components=k+1, svd_solver="full")
    pca_k.fit(S)
    Qm_k=pca_k.transform(S)

    Qm_k_df=pd.DataFrame(Qm_k)
    Qm_k_df.index=data.index
    Qm_k_df['Mcz']=data['Mcz']
    Qm_k_df.to_csv("COMBO17pca_"+type+"_"+str(k+1)+"pc.csv")

    #test dataset upload and corrections
    eval_data=pd.read_csv("COMBO17eval.csv")
    eval_data=u.remove_columns(eval_data)
    for col in eval_data.columns:
        eval_data[col].fillna(inplace=True, value=dict_means[col])

    if standardize:
        eval_S = pd.DataFrame(scaler.transform(eval_data[features]), columns=features)
        eval_S=eval_S.values
    else:
        eval_S = eval_data[features].values

    #PCA on test dataset
    Qm_k_eval=pca_k.transform(eval_S)
    Qm_k_eval_df=pd.DataFrame(Qm_k_eval)
    Qm_k_eval_df.index=eval_data.index
    Qm_k_eval_df['Mcz']=eval_data['Mcz']

    # Fitting
    knn_reg=KNeighborsRegressor(n_neighbors=5)
    knn_reg.fit(Qm_k, Qm_k_df['Mcz'])
    predictions=knn_reg.predict(Qm_k_eval)

    Qm_k_eval_df['Mcz_hat']=predictions.copy()
    Qm_k_eval_df.to_csv("COMBO17eval_291251_"+type+"_"+str(k+1)+"pc.csv")

    mae=mean_absolute_error(Qm_k_eval_df['Mcz'], Qm_k_eval_df['Mcz_hat'])
    mre = u.mean_relative_error(Qm_k_eval_df['Mcz'], Qm_k_eval_df['Mcz_hat'])
    print(f"Regression results using PCA with {k+1} components: ")
    print(f"MAE: {mae}")
    print(f"MRE: {mre}")


    #----- Without PCA ---------------------------------------------------

    X_train=data[features].values
    y_train = data['Mcz']

    X_test= eval_S
    y_test = eval_data['Mcz']

    knn_reg_full=KNeighborsRegressor(n_neighbors=5)
    knn_reg_full.fit(X_train, y_train)
    predictions_full=knn_reg_full.predict(X_test)

    mae_full=mean_absolute_error(y_test, predictions_full)
    mre_full=u.mean_relative_error(y_test, predictions_full)

    print(f"Regression results using original data without PCA: ")
    print(f"MAE: {mae_full}")
    print(f"MRE: {mre_full}")


if __name__ == "__main__":
    main()