"""
    created by tfz 2022.3.15, used for Mip test about the article model
    of "Deep Reinforcement Learning for Joint Channel
    Selection and Power Control in D2D Networks"
"""
from pyscipopt import Model, quicksum, log
import time
def ModelBuild(M, N, pMax, sigma, h, weight):       
    model = Model("wireless_trans")
    """
    build the varibles used in the model
    """
    r, p, alpha  = {}, {}, {}
    for m in range(M):
        p[m] = model.addVar(lb = 0, ub = pMax, vtype="C", name="p(%s)"%m)
        for n in range(N):
                r[m, n] = model.addVar(vtype="C", name="r(%s,%s)"%(m,n))             
                alpha[m, n] = model.addVar(vtype="B", name="alpha(%s,%s)"%(m,n))
    """
    build the varibles used in the model
    """            
    for m in range(M):
        model.addCons(quicksum(alpha[m, n] for n in range(N)) <= 1, "AlphaCons(%s)"%m)
        for n in range(N):
            model.addCons(log(1 + (alpha[m, n] * p[m] * h[m, n]) / (sigma + quicksum(alpha[i, n] * p[i] * h[i, n] for i in range(M) if i != m))) == r[m, n], "r(%s, %s) Defination"%(m, n))
    model.setObjective(quicksum(weight[m, n] * r[m, n] for (m, n) in r), 'maximize')  
    return model

def ModelSolve(model):      
    model.getObjectiveSense()
    start = time.time()
    model.optimize()
    elapsed = (time.time() - start)
    print("Scip time used: " + str(elapsed))
    cost = model.getObjVal()
    print("SCip Model Cost %s"%cost)
"""
    for v in model.getVars():
        if model.getVal(v) > 0.001:
            print(v.name, "=", model.getVal(v))"""