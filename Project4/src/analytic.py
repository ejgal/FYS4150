import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



DATADIR = '../data/'

J = 1

def energy(state):
    return -2*(state[0] + state[3])*(state[2] + state[1])

def count(state):
    up = np.count_nonzero(state == 1)
    return up

def magnetization(state):
    return np.sum(state)


def z(T):
    B = 1/T
    return 2*(np.exp(8*B*J) + np.exp(-8*B*J)) + 12

def probability(T,state):
    E = energy(state)
    B = 1/T
    # z = 2*(np.exp(8*B*J) + np.exp(-8*B*J)) + 12
    return np.exp(-1*B * E)/z(T)


def susceptibility(T):
    B = 1/T
    return np.abs(32*np.exp(-8*B*J) + 8)/(z(T)*T)

def cv(T):
    B = 1/T
    return np.abs(32*np.exp(-8*B*J) + 8)/(z(T)*T**2)

states = []


def produce_states():
    states = []
    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                for l in [-1,1]:
                    state = np.array([i,j,k,l])
                    states.append(state)
    states = np.array(states)
    return states



if __name__ == '__main__':


    states = produce_states()

    # # Plot probability versus temperature
    # for T in [0.1,1,2,3,10,100]:
    #     prob = []
    #     for state in states:
    #         prob.append(probability(T, state))
    #     print(np.sum(prob))
    #     print(prob)
    #     # plt.yscale('log')
    #     plt.plot(prob)
    # plt.show()


    df = pd.DataFrame(columns=['spins','Energy','Magnetization','Degeneracy'])
    for i in range(0, len(states)):
        df.loc[i] = [count(states[i]), energy(states[i]), magnetization(states[i]), count(states[i])]
    print(df)
    group = df.groupby(['spins','Energy','Magnetization']).count().reset_index().sort_values(by='spins', ascending=False)
    group.rename(columns={"spins": "Number of spins up"}, inplace=True)
    group.to_csv(DATADIR + 'analytic.csv', index=False)

    # T = np.linspace(1, 1000,1000)
    # plt.xscale('log')
    # for state in states:
    #     plt.plot(T, probability(T, state), label=state)
    # plt.show()
    #
    # def ex_energy(T):
    #     B = 1/T
    #     return (-16*J*(np.exp(8*B*J) - np.exp(-8*B*J)))/z(T)
    #
    # # z = 2*(np.exp(8*(1/T)*J) + np.exp(-8*(1/T)*J)) + 12
    # plt.xscale('log')
    # plt.plot(T, ex_energy(T), label='Energy')
    # plt.plot(T, cv(T), label='Heat capacity')
    # plt.plot(T, susceptibility(T), label='Susceptibility')
    # plt.legend()
    # plt.show()
