'''
Describes agents for MAB with and without context

Each agent provides the following two methods :
    choose ()   :   choose an arm from the given contexts. Returns
                    the index of the arm to be played
    update()    :   Updates the model parameters given the context
                    and the reward
'''

import random
import numpy as np
from numpy.random import multivariate_normal
'''
Will contain the following policies :   
    Thompson Sampling   :   Updates using Bayes rule, generates weight
                            vector using distribution
    LinUCB              :   Similar to normal LinUCB rule
    Random              :   Randomly select an arm
    Eps-Greedy          :   Epsilon greedy selection of arm
    Bootstrap           :   Bootstrap method for arm selection

'''


class ThompsonSampling():
    def __init__(self, nu, d):
        self.d = d
        self.B = np.matrix(np.identity(d))
        self.mu = np.matrix(np.zeros(d))
        self.f = np.matrix(np.zeros(d))
        self.nu = nu
        self.Binv = np.matrix(np.identity(d))

        return

    def choose(self, contexts):
        muarray = np.squeeze(np.asarray(self.mu))
        mut = multivariate_normal(muarray, self.nu*self.nu*self.Binv)

        rewards = np.matrix(contexts) * (np.matrix(mut).transpose())
        optarm = np.argmax(rewards)

        return optarm

    def update(self, context, reward):
        b = np.matrix(context)
        self.B = self.B + b.transpose()*b
        self.f = self.f + reward*context
        self.Binv = np.linalg.inv(self.B)
        self.mu = self.Binv * self.f.transpose()
        return
    
    def name(self):
        return "Thompson Sampling"


class LinUCB():
    def __init__(self, alpha, d):
        self.d = d
        self.A = np.matrix(np.identity(d))
        self.b = np.matrix(np.zeros((d, 1)))
        self.t = np.matrix(np.zeros((d, 1)))
        self.alpha = alpha
        self.Ainv = np.matrix(np.identity(d))

    def choose(self, contexts):
        narm = contexts.shape[0]
        first = np.zeros((narm, 1))

        for k in range(0, narm):
            Xk = np.matrix(contexts[k, :])
            first[k, 0] = Xk * self.Ainv * Xk.transpose()

        first = np.sqrt(first) * self.alpha
        second = np.matrix(contexts) * np.matrix(self.t)
        rewards = first + second
        optarm = np.argmax(rewards)

        return optarm

    def update(self, context, reward):
        x = np.matrix(context)
        self.A = self.A + x.transpose()*x
        self.b = self.b + (reward*x).transpose()
        self.Ainv = np.linalg.inv(self.A)
        self.t = self.Ainv*self.b
        return

    def name(self):
        return "LinUCB"


class Random():
    def __init__(self, flag=True):
        self.arm = 0
        self.flag = flag

    def choose(self, contexts):
        N = contexts.shape[0]
        if self.flag:
            optarm = np.random.randint(N)
        else:
            optarm = self.arm
        return optarm

    def update(self, context, reward):
        return

    def name(self):
        return "Random"


class EpsGreedy():
    def __init__(self, epsilon, d, alpha):
        self.epsilon = epsilon
        self.d = d
        self.A = np.matrix(np.identity(d))
        self.b = np.matrix(np.zeros(d))
        self.t = np.matrix(np.zeros(d))
        self.alpha = alpha
        self.Ainv = np.matrix(np.identity(d))

    def choose(self, contexts):
        narm = contexts.shape[0]
        first = np.zeros((narm, 1))

        for k in range(0, narm):
            Xk = np.matrix(contexts[k, :])
            first[k, 0] = Xk * self.Ainv * Xk.transpose()

        first = np.sqrt(first) * self.alpha
        second = np.matrix(contexts) * np.matrix(self.t)
        rewards = first + second
        optarm = np.argmax(rewards)
        threshold = self.epsilon * narm
        if np.random.randint(narm) > threshold:
            return optarm
        else:
            return np.random.randint(narm)

    def update(self, context, reward):
        x = np.matrix(context)
        self.A = self.A + x.tranpose()*x
        self.b = self.b + (reward*x).transpose()
        self.Ainv = np.linalg.inv(self.A)
        self.t = self.Ainv*self.b
        return

    def name(self):
        return "Epsilon Greedy"

class OnlineBootstrap():
    def __init__(self, B=1, narm=10, d=10):     
        self.B = B
        self.d = d
        self.narm = narm
        self.all_arm_feats = np.random.randn(self.narm, self.B, self.d)  # Initialize all arm features 

    
    def choose(self, contexts): 
        selected_arm_feats = np.array((narm, self.d))

        # Sample arm feature for each arm
        for k in range(self.narm):
            selected_feature_index = random.randint(0,self.B-1)
            selected_arm_feats[k,:] = self.all_arm_feats[k, selected_feature_index, : ] # Randomly select the feature

        # Select the arm
        rewards = np.matrix(contexts)*np.matrix(selected_arm_feats)
        optarm = np.argmax(rewards)

        return optarm

    def update(self, selected_arm, context, reward):
        for j in range(self.B):
            p = np.random.poisson(lam=1)
            for z in range(1,p+1):
                eta = 1.0 / (math.sqrt(z)+1)
                self.all_arm_feats[selected_arm, j , :] += eta* # derivative of log-likelihood



    def name(self):
        return "Online Bootstrap"