import scipy.stats as stats
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

ms_1 = [47, 47, 49, 45, 42, 43, 39, 48, 43]
ms_2 = [41,	45,	39,	48,	39,	37,	42,	47,	44,	42]
ms_3 = [47,	42, 45,	43,	47,	37,	43,	47,	41,	39]
ms_4 = [38,	38,	37,	45,	41,	41,	41,	46,	53,	45, 44]
ms_5 = [47,	47,	49,	44,	49,	46,	41,	41,	42,	46]
ms_6 = [41,	41,	45,	38,	42,	33,	45,	43,	44,	44,	46]
ms_7 = [35,	36,	44,	32,	40,	41,	43,	45,	48,	48]
ms_8 = [36,	39,	39,	38,	44,	42,	48,	38,	46,	37,	46]
ms_9 = [35,	29,	39,	37,	40,	36,	43,	48,	41,	44,	42]

data = np.rec.array([
(  47,   'ms_1'), (  47,   'ms_1'), (  49,   'ms_1'), (  45,   'ms_1'), (  42,   'ms_1'), ( 43 ,   'ms_1'), (  39,   'ms_1'), (  48,   'ms_1'), (  43,   'ms_1'),
(  41,   'ms_2'), (  45,   'ms_2'), (  39,   'ms_2'), (  48,   'ms_2'), (  39,   'ms_2'), (  37,   'ms_2'), (  42,   'ms_2'), (  47,   'ms_2'), (  44,   'ms_2'), ( 42,   'ms_2'),
(  47,   'ms_3'), (  42,   'ms_3'), (  45 ,  'ms_3'), (  43,   'ms_3'), (  47,   'ms_3'), (  37,   'ms_3'), (  43,   'ms_3'), (  47,   'ms_3'), (  41,   'ms_3'), ( 39,   'ms_3'),
(  38,   'ms_4'), (  38,   'ms_4'), (  37,   'ms_4'), (  45,   'ms_4'), (  41,   'ms_4'), (  41,   'ms_4'), (  41,   'ms_4'), (  46,   'ms_4'), (  53,   'ms_4'), (  45,   'ms_4'), (  44,   'ms_4'),
(  47,   'ms_5'), (  47,   'ms_5'), (  49,   'ms_5'), (  44,   'ms_5'), (  49,   'ms_5'), (  46,   'ms_5'), (  41,   'ms_5'), (  41,   'ms_5'), (  42,   'ms_5'), (  46,   'ms_5'),
(  41,   'ms_6'), (  41,   'ms_6'), (  45,   'ms_6'), (  38,   'ms_6'), (  42,   'ms_6'), (  33,   'ms_6'), (  45,   'ms_6'), (  43,   'ms_6'), (  44,   'ms_6'), (  44,   'ms_6'), (  46,   'ms_6'),
(  35,   'ms_7'), (  36,   'ms_7'), (  44,   'ms_7'), (  32,   'ms_7'), (  40,   'ms_7'), (  41,   'ms_7'), (  43,   'ms_7'), (  45,   'ms_7'), (  48,   'ms_7'), (  48,   'ms_7'),
(  36,   'ms_8'), (  39,   'ms_8'), (  39,   'ms_8'), (  38,   'ms_8'), (  44,   'ms_8'), (  42,   'ms_8'), (  48,   'ms_8'), (  38,   'ms_8'), (  46,   'ms_8'), (  37,   'ms_8'), (  46,   'ms_8'),
(  35,   'ms_9'), (  29,   'ms_9'), (  39,   'ms_9'), (  37,   'ms_9'), (  40,   'ms_9'), (  36,   'ms_9'), (  43,   'ms_9'), (  48,   'ms_9'), (  41,   'ms_9'), (  44,   'ms_9'), (  42,   'ms_9')],
dtype = [('score', '<i4'), ('student', '|S8')])


print("Results from Levene's test, dealing with homogeneity of variance:")
print(stats.levene(ms_1, ms_2, ms_3, ms_4, ms_5, ms_6, ms_7, ms_8, ms_9))

print("Results from one-way ANOVA:")
print(stats.f_oneway(ms_1, ms_2, ms_3, ms_4, ms_5, ms_6, ms_7, ms_8, ms_9))

print("Results of the Kruskla Wallis Test:")
print(stats.mstats.kruskalwallis(ms_1, ms_2, ms_3, ms_4, ms_5, ms_6, ms_7, ms_8, ms_9))

mc = MultiComparison(data['score'], data['student'])
results = mc.tukeyhsd(alpha=0.1)


print(results)
