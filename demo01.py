import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier

if_in = False
range_ = []

def normal_error(x):
    if(x[0]!=0):
        x[0]=1
    pass

def test_in(x):
    global if_in,range_

    if x[0]==x_test[i] and x[1] in range_:
        if_in = True
    else:
        if_in = False
    pass

if __name__=='__main__':
    data_train = np.array(pd.read_excel(r'dataset/train.xlsx'))
    x_train = data_train[:,0]
    x_train = x_train.reshape(len(x_train), 1)
    y_train = data_train[:,1]
    data_test = np.array(pd.read_excel(r'dataset/test.xlsx'))
    x_test = data_test[:,0]
    x_test = x_test.reshape(len(x_test), 1)
    y_test = data_test[:,1]

    clf = MLPClassifier(hidden_layer_sizes=(1,4,8,2), activation='logistic', solver='adam', random_state=1, max_iter=1000)
    clf.fit(x_train,y_train)

    y_predict = clf.predict(x_test[0].reshape(1,1))
    
    y_predict_proba = clf.predict_proba(x_test[0].reshape(1,1))



    proba = np.argsort(y_predict_proba)[-10:]
    templates = []
    for p in proba:
        templates.append(clf.classes_[p])

    print('The final prediction outcome is: ', templates)

    # error = []
    # length = len(y_predict)
    # range_ = []
    # if_in = False
    # data_test_in = pd.read_excel(r'dataset/train.xlsx')
    # for i in range(length):
    #     print('Completed: ', i/length, ' error: ', np.sum(error))
    #     if i>0:
    #         print(y_predict_proba[i]-y_predict_proba[i-1])
    #     proba = np.argsort(y_predict_proba[i])[-10:]
    #     range_ = []
    #     print('proba: ', proba)
    #     for p in proba:
    #         range_.append(clf.classes_[p])
    #     print('range: ', range_)
    #     if_in = False
    #     data_test_in.apply(func = test_in, raw=False, axis=1)
    #     if if_in==False:
    #         error.append(1)
    #     else:
    #         error.append(0)
    #     pass

    # print(np.sum(error), ' ', np.sum(error)/len(y_predict))



    pass