import sys
import os
import time

import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.KnapsackEvaluationFunction as KnapsackEvaluationFunction
from array import array
import csv
import time

"""
Commandline parameter(s):
    none
"""

# set Number of items
NUM_ITEMS = [20, 50, 100]
iterationsVec = [10000, 20000, 30000]
random = Random()

# The number of copies each
COPIES_EACH = 4
# The maximum weight for a single element
MAX_WEIGHT = 50
# The maximum volume for a single element
MAX_VOLUME = 50

# csv file for RHC
data_RHC = open("Knapsack_RHC.csv",'w')
wr_RHC = csv.writer(data_RHC, delimiter=",")

# csv file for SA
data_SA = open("Knapsack_SA.csv",'w')
wr_SA = csv.writer(data_SA, delimiter=",")

# csv file for GA
data_GA = open("Knapsack_GA.csv",'w')
wr_GA = csv.writer(data_GA, delimiter=",")

# csv file for GA
data_MIMIC = open("Knapsack_MIMIC.csv",'w')
wr_MIMIC = csv.writer(data_MIMIC, delimiter=",")

for n in NUM_ITEMS:

    # The volume of the knapsack
    KNAPSACK_VOLUME = MAX_VOLUME * n * COPIES_EACH * .4

    # create copies
    fill = [COPIES_EACH] * n
    copies = array('i', fill)

    # create weights and volumes
    fill = [0] * n
    weights = array('d', fill)
    volumes = array('d', fill)

    for i in range(0, n):
        weights[i] = random.nextDouble() * MAX_WEIGHT
        volumes[i] = random.nextDouble() * MAX_VOLUME

        # create range
        fill = [COPIES_EACH + 1] * n
        ranges = array('i', fill)

        ef = KnapsackEvaluationFunction(weights, volumes, KNAPSACK_VOLUME, copies)
        odd = DiscreteUniformDistribution(ranges)
        nf = DiscreteChangeOneNeighbor(ranges)
        mf = DiscreteChangeOneMutation(ranges)
        cf = UniformCrossOver()
        df = DiscreteDependencyTree(.1, ranges)
        hcp = GenericHillClimbingProblem(ef, odd, nf)
        gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
        pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

    for iterations in iterationsVec:

        # RHC
        print 'training RHC\tn = ' + str(n) + '\titerations = ' + str(iterations)
        start = time.clock()
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "RHC: " + str(ef.value(rhc.getOptimal()))
        row = [n, iterations, ef.value(rhc.getOptimal()), elapsed]
        wr_RHC.writerows([row])

        # SA
        print 'training SA\tn = ' + str(n) + '\titerations = ' + str(iterations)
        start = time.clock()
        sa = SimulatedAnnealing(100, .95, hcp)
        fit = FixedIterationTrainer(sa, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "SA: " + str(ef.value(sa.getOptimal()))
        row = [n, iterations, ef.value(sa.getOptimal()), elapsed]
        wr_SA.writerows([row])

        print 'training GA\tn = ' + str(n) + '\titerations = ' + str(iterations)
        ga = StandardGeneticAlgorithm(200, 150, 25, gap)
        fit = FixedIterationTrainer(ga, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "GA: " + str(ef.value(ga.getOptimal()))
        row = [n, iterations, ef.value(ga.getOptimal()), elapsed]
        wr_GA.writerows([row])

        print 'training MIMIC\tn = ' + str(n) + '\titerations = ' + str(iterations)
        mimic = MIMIC(200, 100, pop)
        fit = FixedIterationTrainer(mimic, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "MIMIC: " + str(ef.value(mimic.getOptimal()))
        row = [n, iterations, ef.value(mimic.getOptimal()), elapsed]
        wr_MIMIC.writerows([row])
