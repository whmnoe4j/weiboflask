'''
使用机器学习库sklearn处理多分类问题
'''

import random
import os
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import zero_one_loss
from sklearn.naive_bayes import MultinomialNB

import Bayes as bayes

base_dir = os.path.dirname(__file__)


def getada_real():
    n_estimators = 500
    learning_rate = 1.
    vocabList = bayes.build_key_word(os.path.join(base_dir, "train.txt"))
    line_cut, label = bayes.loadDataSet(os.path.join(base_dir, "train.txt"))
    train_mood_array = bayes.setOfWordsListToVecTor(vocabList, line_cut)
    test_word_array = []
    test_word_arrayLabel = []
    testCount = 100  # 从中随机选取100条用来测试，并删除原来的位置
    for i in range(testCount):
        try:
            randomIndex = int(random.uniform(0, len(train_mood_array)))
            test_word_arrayLabel.append(label[randomIndex])
            test_word_array.append(train_mood_array[randomIndex])
            del (train_mood_array[randomIndex])
            del (label[randomIndex])
        except Exception as e:
            print(e)
    multi = MultinomialNB()
    ada_real = AdaBoostClassifier(
        base_estimator=multi,
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        algorithm="SAMME.R")
    ada_real.fit(train_mood_array, label)
    ada_real_err = np.zeros((n_estimators,))  # 变成一个一维的矩阵，长度为n
    for i, y_pred in enumerate(ada_real.staged_predict(test_word_array)):  # 测试
        ada_real_err[i] = zero_one_loss(y_pred, test_word_arrayLabel)  # 得出不同的，然后除于总数
    ada_real_err_train = np.zeros((n_estimators,))
    for i, y_pred in enumerate(ada_real.staged_predict(train_mood_array)):  # 训练样本对训练样本的结果
        ada_real_err_train[i] = zero_one_loss(y_pred, label)
    return vocabList, ada_real


def test(word):
    vocabList, ada_real = getada_real()
    word_array = bayes.build_word_array(word)
    asfaiajioaf = bayes.setOfWordsListToVecTor(vocabList, word_array)
    # for i, y_pred in enumerate(ada_real.staged_predict(asfaiajioaf)):  # 训练样本对训练样本的结果
    #     print(y_pred)
    print(ada_real.predict(asfaiajioaf))
    return ada_real.predict(asfaiajioaf)[0]


if __name__ == '__main__':
    word = "高兴，开心，非常开心，愉快"
    print(test(word))