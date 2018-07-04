##一维稀疏矩阵特征选择
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder,LabelEncoder
from scipy import sparse
print('这真真是、最终版稀疏矩阵特征筛选了')
print('天灵灵地灵灵、太上老君来显灵')
print('两段代码两段代码跑得块、跑得块')
print('一段没有bug、一段出了好结果')
print('真开心、真高兴')
print('Reading...')
train_part_x = pd.DataFrame()
evals_x = pd.DataFrame()
train_index = pd.read_csv('data_preprocessing/train_index_2.csv',header=None)[0].values.tolist()
for i in range(1,11):
    train_part_x = sparse.hstack((train_part_x,sparse.load_npz('data_preprocessing/train_part_x_sparse_two_'+str(i)+'.npz').tocsr()[train_index,:])).tocsc()
    evals_x = sparse.hstack((evals_x,sparse.load_npz('data_preprocessing/evals_x_sparse_two_'+str(i)+'.npz'))).tocsc()
    print('读到了第',i,'个训练集特征文件')
print("Sparse is ready")
print('Label...')
train_part_y=pd.read_csv('data_preprocessing/train_part_y.csv',header=None).loc[train_index]
evals_y=pd.read_csv('data_preprocessing/evals_y.csv',header=None)
##利用特征重要性筛选特征
import pandas as pd
from lightgbm import LGBMClassifier
import time
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')
clf = LGBMClassifier(boosting_type='gbdt',
                     num_leaves=31, max_depth=-1, 
                     learning_rate=0.1, n_estimators=10000, 
                     subsample_for_bin=200000, objective=None,
                     class_weight=None, min_split_gain=0.0, 
                     min_child_weight=0.001,
                     min_child_samples=20, subsample=1.0, subsample_freq=1,
                     colsample_bytree=1.0,
                     reg_alpha=0.0, reg_lambda=0.0, random_state=None,
                     n_jobs=-1, silent=True)
print('Fiting...')
clf.fit(train_part_x, train_part_y, eval_set=[(train_part_x, train_part_y),(evals_x, evals_y)], 
        eval_names =['train','valid'],
        eval_metric='auc',early_stopping_rounds=100)
se = pd.Series(clf.feature_importances_)
se = se[se>0]
col =list(se.sort_values(ascending=False).index)
pd.Series(col).to_csv('data_preprocessing/col_sort_two.csv',index=False)
print('特征重要性不为零的编码特征有',len(se),'个')
n = clf.best_iteration_
baseloss = clf.best_score_['valid']['auc']
print('全量特征得分为',baseloss)

import pandas as pd
col = pd.read_csv("data_preprocessing/col_sort_two.csv",header=None)[0].values.tolist()
best_num = 2000
from scipy import sparse
train_part_x1 = pd.DataFrame()
for i in range(1,11):
    train_part_x1 = sparse.hstack((train_part_x1,sparse.load_npz('data_preprocessing/train_part_x_sparse_two_'+str(i)+'.npz').tocsr()[:20000000,])).tocsc()
    print('读到了第',i,'个train特征文件')
train_part_x2 = pd.DataFrame()
for i in range(1,11):
    train_part_x2 = sparse.hstack((train_part_x2,sparse.load_npz('data_preprocessing/train_part_x_sparse_two_'+str(i)+'.npz').tocsr()[20000000:,])).tocsc()
    print('读到了第',i,'个train特征文件')
print('Saving train part...')
sparse.save_npz("data_preprocessing/train_part_x_sparse_two_select.npz",sparse.vstack((train_part_x1[:,col[:best_num]],train_part_x2[:,col[:best_num]])))
train_part_x1 = []
train_part_x2 = []
evals_x = pd.DataFrame()
for i in range(1,11): 
    evals_x = sparse.hstack((evals_x,sparse.load_npz('data_preprocessing/evals_x_sparse_two_'+str(i)+'.npz'))).tocsc()
    print('读到了第',i,'个valid特征文件')
print('Saving evals...')
sparse.save_npz("data_preprocessing/evals_x_sparse_two_select.npz",evals_x[:,col[:best_num]])
evals_x = []
print('Reading test...')
test1_x = pd.DataFrame()
test2_x = pd.DataFrame()
for i in range(1,11):
    test1_x = sparse.hstack((test1_x,sparse.load_npz('data_preprocessing/test1_x_sparse_two_'+str(i)+'.npz'))).tocsc()
    test2_x = sparse.hstack((test2_x,sparse.load_npz('data_preprocessing/test2_x_sparse_two_'+str(i)+'.npz'))).tocsc()
    print('读到了第',i,'个测试集特征文件')
print('Saving test...')
print('Saving test1...')
sparse.save_npz("data_preprocessing/test1_x_sparse_two_select.npz",test1_x[:,col[:best_num]])
print('Saving test2...')
sparse.save_npz("data_preprocessing/test2_x_sparse_two_select.npz",test2_x[:,col[:best_num]])
print('我的天终于筛选存完了')