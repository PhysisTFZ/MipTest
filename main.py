import scip_model as Smodel
import gurobi_model as Gmodel
import parameter as pa
M = 10
N = 2
pMax = 3
delta = 3
weight, h = pa.GenerateWH(M, N)
sused = 1
gused = 1
if sused :
    smodel = Smodel.ModelBuild(M, N, pMax, delta, h, weight)
    Smodel.ModelSolve(smodel)
    gmodel = Gmodel.ModelBuild(M, N, pMax, delta, h, weight)
    Gmodel.ModelSolve(gmodel)