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
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
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
import opt.example.TravelingSalesmanEvaluationFunction as TravelingSalesmanEvaluationFunction
import opt.example.TravelingSalesmanRouteEvaluationFunction as TravelingSalesmanRouteEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import shared.Instance as Instance
import util.ABAGAILArrays as ABAGAILArrays

from array import array
import csv
import time

"""
Commandline parameter(s):
    none
"""

# set N value.  This is the number of points
N = [20, 50, 100]
iterationsVec = [500, 1000, 2000, 3000]
random = Random()

# csv file for RHC
data_RHC = open("TravelingSalesman_RHC.csv",'w')
wr_RHC = csv.writer(data_RHC, delimiter=",")

# csv file for SA
data_SA = open("TravelingSalesman_SA.csv",'w')
wr_SA = csv.writer(data_SA, delimiter=",")

# csv file for GA
data_GA = open("TravelingSalesman_GA.csv",'w')
wr_GA = csv.writer(data_GA, delimiter=",")

# csv file for GA
data_MIMIC = open("TravelingSalesman_MIMIC.csv",'w')
wr_MIMIC = csv.writer(data_MIMIC, delimiter=",")

for n in N:

    # Compute points
    points = [[0 for x in xrange(2)] for x in xrange(n)]
    for i in range(0, len(points)):
        points[i][0] = random.nextDouble()
        points[i][1] = random.nextDouble()

    # isntanciate learners
    ef = TravelingSalesmanRouteEvaluationFunction(points)
    odd = DiscretePermutationDistribution(n)
    nf = SwapNeighbor()
    mf = SwapMutation()
    cf = TravelingSalesmanCrossOver(ef)
    hcp = GenericHillClimbingProblem(ef, odd, nf)
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)

    for iterations in iterationsVec:

        # RHC
        print 'training RHC\tn = ' + str(n) + '\titerations = ' + str(iterations)
        start = time.clock()
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "RHC Inverse of Distance: " + str(ef.value(rhc.getOptimal()))
        # print "Route:"
        # path = []
        # for x in range(0,n):
        #     path.append(rhc.getOptimal().getDiscrete(x))
        # print path
        row = [n, iterations, ef.value(rhc.getOptimal()), elapsed]
        wr_RHC.writerows([row])

        # SA
        print 'training SA\tn = ' + str(n) + '\titerations = ' + str(iterations)
        start = time.clock()
        sa = SimulatedAnnealing(1E11, 0.95, hcp)
        fit = FixedIterationTrainer(sa, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "SA Inverse of Distance: " + str(ef.value(sa.getOptimal()))
        # print "Route:"
        # path = []
        # for x in range(0,n):
        #     path.append(sa.getOptimal().getDiscrete(x))
        # print path
        row = [n, iterations, ef.value(sa.getOptimal()), elapsed]
        wr_SA.writerows([row])

        # GA
        print 'training GA\tn = ' + str(n) +'\titerations = ' + str(iterations)
        start = time.clock()
        ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
        fit = FixedIterationTrainer(ga, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "GA Inverse of Distance: " + str(ef.value(ga.getOptimal()))
        # print "Route:"
        # path = []
        # for x in range(0,n):
        #     path.append(ga.getOptimal().getDiscrete(x))
        # print path
        row = [n, iterations, ef.value(ga.getOptimal()), elapsed]
        wr_GA.writerows([row])

        # MIMIC
        print 'training MIMIC\tn = ' + str(n) +'\titerations = ' + str(iterations)
        start = time.clock()
        ef = TravelingSalesmanSortEvaluationFunction(points);
        fill = [n] * n
        ranges = array('i', fill)
        odd = DiscreteUniformDistribution(ranges);
        df = DiscreteDependencyTree(.1, ranges);
        pop = GenericProbabilisticOptimizationProblem(ef, odd, df);

        mimic = MIMIC(500, 100, pop)
        fit = FixedIterationTrainer(mimic, iterations)
        fit.train()
        elapsed = time.clock() - start
        # print "MIMIC Inverse of Distance: " + str(ef.value(mimic.getOptimal()))
        # print "Route:"
        # path = []
        # optimal = mimic.getOptimal()
        # fill = [0] * optimal.size()
        # ddata = array('d', fill)
        # for i in range(0,len(ddata)):
        #     ddata[i] = optimal.getContinuous(i)
        # order = ABAGAILArrays.indices(optimal.size())
        # ABAGAILArrays.quicksort(ddata, order)
        # print order
        row = [n, iterations, ef.value(mimic.getOptimal()), elapsed]
        wr_MIMIC.writerows([row])
