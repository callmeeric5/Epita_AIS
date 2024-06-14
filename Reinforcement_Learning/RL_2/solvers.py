import numpy as np
import time
from scipy.stats import beta

from bandits import BernoulliBandit


class Solver(object):
    def __init__(self, bandit):
        """
        bandit (Bandit): the target bandit to solve.
        """

        np.random.seed(int(time.time()))

        self.bandit = bandit
        self.counts = [0] * self.bandit.n
        self.actions = []  # A list of machine ids, 0 to bandit.n-1.
        self.regret = 0.0  # Cumulative regret.
        self.regrets = [0.0]  # History of cumulative regret.

    def update_regret(self, i):
        # i (int): index of the selected machine.
        self.regret += self.bandit.best_proba - self.bandit.probas[i]
        self.regrets.append(self.regret)

    @property
    def estimated_probas(self):
        raise NotImplementedError

    def run_one_step(self):
        """Return the machine index to take action on."""
        raise NotImplementedError

    def run(self, num_steps):
        assert self.bandit is not None
        for _ in range(num_steps):
            i = self.run_one_step()

            self.counts[i] += 1
            self.actions.append(i)
            self.update_regret(i)


class EpsilonGreedy(Solver):
    def __init__(self, bandit, eps, init_proba=1.0):
        """
        eps (float): the probability to explore at each time step.
        init_proba (float): default to be 1.0; optimistic initialization
        """
        super(EpsilonGreedy, self).__init__(bandit)

        assert 0.0 <= eps <= 1.0
        self.eps = eps

        self.estimates = [init_proba] * self.bandit.n  # Optimistic initialization

    @property
    def estimated_probas(self):
        return self.estimates

    def run_one_step(self):

        # return the chosen arm and update the estimated reward value of the returned arm

        if np.random.rand() < self.eps:
            chosen_arm = np.random.randint(self.bandit.n)
        else:
            chosen_arm = np.argmax(self.estimates)
        reward = self.bandit.generate_reward(chosen_arm)
        self.estimates[chosen_arm] = (
            self.estimates[chosen_arm] * self.counts[chosen_arm] + reward
        ) / (self.counts[chosen_arm] + 1)
        self.counts[chosen_arm] += 1
        return chosen_arm


class UCB1(Solver):
    def __init__(self, bandit, init_proba=1.0):
        super(UCB1, self).__init__(bandit)
        self.t = 0
        self.estimates = [init_proba] * self.bandit.n

    @property
    def estimated_probas(self):
        return self.estimates

    def run_one_step(self):
        self.t += 1
        ucb_values = [
            self.estimates[chosen_arm]
            + 2 * np.sqrt(np.log(self.t) / (self.counts[chosen_arm] + 1))
            for chosen_arm in range(self.bandit.n)
        ]
        chosen_arm = np.argmax(ucb_values)
        reward = self.bandit.generate_reward(chosen_arm)
        self.estimates[chosen_arm] = (
            self.counts[chosen_arm] * self.estimates[chosen_arm] + reward
        ) / (self.counts[chosen_arm] + 1)
        self.counts[chosen_arm] += 1
        return chosen_arm


class BayesianUCB(Solver):
    """Assuming Beta prior."""

    def __init__(self, bandit, c=3, init_a=1, init_b=1):
        """
        c (float): how many standard dev to consider as upper confidence bound.
        init_a (int): initial value of a in Beta(a, b).
        init_b (int): initial value of b in Beta(a, b).
        """
        super(BayesianUCB, self).__init__(bandit)
        self.c = c
        self._as = [init_a] * self.bandit.n
        self._bs = [init_b] * self.bandit.n

    @property
    def estimated_probas(self):
        return [
            self._as[i] / float(self._as[i] + self._bs[i]) for i in range(self.bandit.n)
        ]

    def run_one_step(self):
        ucb_values = [
            self._as[i] / float(self._as[i] + self._bs[i])
            + self.c
            * np.sqrt(np.log(self.counts[i] + 1) / float(self._as[i] + self._bs[i]))
            for i in range(self.bandit.n)
        ]
        i = np.argmax(ucb_values)
        reward = self.bandit.generate_reward(i)
        self._as[i] += reward
        self._bs[i] += 1 - reward
        self.counts[i] += 1
        return i


class ThompsonSampling(Solver):
    def __init__(self, bandit, init_a=1, init_b=1):
        """
        init_a (int): initial value of a in Beta(a, b).
        init_b (int): initial value of b in Beta(a, b).
        """
        super(ThompsonSampling, self).__init__(bandit)

        self._as = [init_a] * self.bandit.n
        self._bs = [init_b] * self.bandit.n

    @property
    def estimated_probas(self):
        return [self._as[i] / (self._as[i] + self._bs[i]) for i in range(self.bandit.n)]

    def run_one_step(self):

        probas = [
            self._as[i] / float(self._as[i] + self._bs[i]) for i in range(self.bandit.n)
        ]
        probas = np.array(probas)
        probas = probas / np.sum(probas)
        i = np.random.choice(self.bandit.n, p=probas)
        reward = self.bandit.generate_reward(i)
        self._as[i] += reward
        self._bs[i] += 1 - reward
        return i
