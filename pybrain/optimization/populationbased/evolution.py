__author__ = 'Tom Schaul, tom@idsia.ch'

from scipy import argmax, array

from pybrain.utilities import abstractMethod
from pybrain.optimization.optimizer import BlackBoxOptimizer


class Evolution(BlackBoxOptimizer):
    """ Base class for evolutionary algorithms, seen as function optimizers. """
    
    maxgenerations = 1e6
    
    popsize = 10
    
    # evolution generally tries to maximize fitness, not minimize a function
    minimize = False
    online = False
    
    def _setInitEvaluable(self, evaluable):
        assert self.minimize == False
        BlackBoxOptimizer._setInitEvaluable(self, evaluable)
        
        # current population
        self.currentpop = []
        self.fitnesses = []
        
        # for analysis purposes, store all kinds of stuff
        self.allgenerations = []
        
    def stoppingCriterion(self):
        return self.bestEvaluation >= self.desiredEvaluation
        
    def _batchLearn(self, maxSteps):    
        """ the main loop """
        self.initPopulation()
        self.generation = 0
        while not self.stoppingCriterion():
            if self.generation > self.maxgenerations:
                break
            if self.steps > maxSteps:
                break
            self.oneGeneration()
            self.generation += 1
            if self.verbose:
                print 'Gen:', self.generation, 'fit:', self.bestEvaluation
        
    def initPopulation(self):
        """ initialize the population """
        abstractMethod()
    
    def oneGeneration(self):
        """ do one generation step """
        # evaluate fitness
        self.fitnesses = []
        for indiv in self.currentpop:
            self.fitnesses.append(self.evaluator(indiv))
            self.steps += 1
        
        # determine the best values
        best = argmax(array(self.fitnesses))
        self.bestEvaluable = self.currentpop[best]
        self.bestEvaluation = self.fitnesses[best]
        self.allgenerations.append((self.currentpop, self.fitnesses))
        
        self.produceOffspring()
        
    def produceOffspring(self):
        """ generate the new generation of offspring, given the current population, and their fitnesses """        
        abstractMethod()
    