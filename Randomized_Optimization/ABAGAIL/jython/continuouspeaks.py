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
import opt.example.ContinuousPeaksEvaluationFunction as ContinuousPeaksEvaluationFunction
from array import array
import csv
import time

"""
Commandline parameter(s):
   none
"""

T = [20, 50, 100]
iterationsVec = [10000, 20000, 30000]


# csv file for RHC
data_RHC = open("ContinuousPeaks_RHC.csv",'w')
wr_RHC = csv.writer(data_RHC, delimiter=",")

# csv file for SA
data_SA = open("ContinuousPeaks_SA.csv",'w')
wr_SA = csv.writer(data_SA, delimiter=",")

# csv file for GA
data_GA = open("ContinuousPeaks_GA.csv",'w')
wr_GA = csv.writer(data_GA, delimiter=",")

# csv file for MIMIC
data_MIMIC = open("ContinuousPeaks_MIMIC.csv",'w')
wr_MIMIC = csv.writer(data_MIMIC, delimiter=",")

for t in T:

    fill = [2] * t
    ranges = array('i', fill)

    # isntanciate learners
    ef = ContinuousPeaksEvaluationFunction(t)
    odd = DiscreteUniformDistribution(ranges)
    nf = DiscreteChangeOneNeighbor(ranges)
    mf = DiscreteChangeOneMutation(ranges)
    cf = SingleCrossOver()
    df = DiscreteDependencyTree(.1, ranges)
    hcp = GenericHillClimbingProblem(ef, odd, nf)
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

    for iterations in iterationsVec:

        # RHC
        print 'training RHC\tT = ' + str(t) + '\titerations = ' + str(iterations)
        start = time.clock()
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "RHC: " + str(ef.value(rhc.getOptimal()))
        row = [t, iterations, ef.value(rhc.getOptimal()), elapsed]
        wr_RHC.writerows([row])


        # SA
        print 'training SA\tT = ' + str(t) + '\titerations = ' + str(iterations)
        start = time.clock()
        sa = SimulatedAnnealing(1E11, .95, hcp)
        fit = FixedIterationTrainer(sa, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "SA: " + str(ef.value(sa.getOptimal()))
        row = [t, iterations, ef.value(sa.getOptimal()), elapsed]
        wr_SA.writerows([row])

        # GA
        print 'training GA\tT = ' + str(t) +'\titerations = ' + str(iterations)
        start = time.clock()
        ga = StandardGeneticAlgorithm(200, 100, 10, gap)
        fit = FixedIterationTrainer(ga, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "GA: " + str(ef.value(ga.getOptimal()))
        row = [t, iterations, ef.value(ga.getOptimal()), elapsed]
        wr_GA.writerows([row])

        # MIMIC
        print 'training MIMIC\tT = ' + str(t) +'\titerations = ' + str(iterations)
        start = time.clock()
        mimic = MIMIC(200, 20, pop)
        fit = FixedIterationTrainer(mimic, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "MIMIC: " + str(ef.value(mimic.getOptimal()))
        row = [t, iterations, ef.value(mimic.getOptimal()), elapsed]
        wr_MIMIC.writerows([row])
