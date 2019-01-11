import numpy as np
from numpy import genfromtxt
import sys

#Reading the Command-Line Arguments
part = sys.argv[1]
TrainingData = sys.argv[2]
TestData = sys.argv[3]
output = sys.argv[4]

#Loading Training and Test Data

data_train = genfromtxt(TrainingData, delimiter=',')
data_test = genfromtxt(TestData, delimiter=',')
#data_train = np.load(TrainingData)
#data_test = np.load(TestData)

arrayof1 = [1]*len(data_train)
arrayof1 = np.reshape(arrayof1, (len(arrayof1) , 1))

#Splitting Training and Test Data into Feature Matrix and Response Variable Vector
X_train = np.concatenate((arrayof1 , data_train[:,1:]), axis=1)
#X_train = data_train[:,1:]
Y_train = data_train[:,0]
arrayof1 = [1]*len(data_test)
arrayof1 = np.reshape(arrayof1, (len(arrayof1) , 1))
X_test = np.concatenate((arrayof1 , data_test[:,1:]), axis=1)
#X_test = data_test[:,1:]
Y_test = data_test[:,0]
Y_train = np.reshape(Y_train, (len(Y_train) , 1))
Y_test = np.reshape(Y_test, (len(Y_test) , 1))

I_p = np.identity(91)
I_p[0][0] = 0

#Linear Regression Function
def linearregression():
    #print("doing lr")
    trans = X_train.T
    MPinv = np.linalg.pinv(np.dot(trans ,X_train))
    Theta = MPinv @ trans @ Y_train
    answer = np.dot(X_test,Theta)
    np.savetxt(output, answer, delimiter=",")
    return answer

#answer_lr = linearregression()

def error(a , b):
    sum = 0
    l = len(a)
    if l!=len(b):
        print("The lengths of the prediction array and test array don't match")
        return
    for i in range(0 , l):
        sum += (a[i] - b[i])**2
    sum /= 2*(l)
    return sum

def ridgeregression():
    lambdas = [0, 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9 , 1 ]
    default = 0
    minimum = 100000
    batches = np.array_split(data_train, 10)
    
    for i in lambdas:
        avg = 0
        for j in range(0,10):
            if j<9:
                train = np.concatenate(batches[:j] + batches[j+1:], axis=0)
            else:
                train = np.concatenate(batches[:j], axis=0)
                
            #print(str(i) + "     " + str(j))
            
            arrayof1 = [1]*len(train)
            arrayof1 = np.reshape(arrayof1, (len(arrayof1) , 1))
            X_train = np.concatenate((arrayof1 , train[:,1:]), axis=1)
            Y_train = train[:,0]
            Y_train = np.reshape(Y_train, (len(Y_train) , 1))
            
            arrayof1 = [1]*len(batches[j])
            arrayof1 = np.reshape(arrayof1, (len(arrayof1) , 1))
            X_test = np.concatenate((arrayof1 , batches[j][:,1:]), axis=1)
            Y_test = (batches[j])[:,0]
            Y_test = np.reshape(Y_test, (len(Y_test) , 1))
            
            trans = X_train.T
            blabla = np.dot(trans ,X_train)
            blabla += I_p*i
            MPinv = np.linalg.pinv(blabla)
            Theta = MPinv @ trans @ Y_train
            answer = np.dot(X_test,Theta)
            
            err = error(answer , Y_test)
            #print("ERROR = " + str(err))
            
            avg += err
        avg /= 10
        #print("average =  " + str(avg))
        
        if avg<minimum:
            minimum = avg
            #print("i is :- " + str(i))
            default = i
    
    #print("VALU OF LAMBDA -> " + str(default))


    arrayof1 = [1]*len(data_train)
    arrayof1 = np.reshape(arrayof1, (len(arrayof1) , 1))
    X_train = np.concatenate((arrayof1 , data_train[:,1:]), axis=1)
    Y_train = data_train[:,0]
    arrayof1 = [1]*len(data_test)
    arrayof1 = np.reshape(arrayof1, (len(arrayof1) , 1))
    X_test = np.concatenate((arrayof1 , data_test[:,1:]), axis=1)
    Y_test = data_test[:,0]
    Y_train = np.reshape(Y_train, (len(Y_train) , 1))
    Y_test = np.reshape(Y_test, (len(Y_test) , 1))
    
    trans = X_train.T
    blabla = np.dot(trans ,X_train)
    blabla += I_p*i
    MPinv = np.linalg.pinv(blabla)
    Theta = MPinv @ trans @ Y_train
    answer = np.dot(X_test,Theta)
    
    np.savetxt(output, answer, delimiter=",")
    
    return answer

if part == 'a':
    linearregression()
elif part =='b':
    ridgeregression()
elif part =='c':
    ridgeregression()


    
#answer_rr = ridgeregression()



#ridgeregression()  
    