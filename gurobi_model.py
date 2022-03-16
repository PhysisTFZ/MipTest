"""
    created by tfz 2022.3.15, used for Mip test about the article model
    of "Deep Reinforcement Learning for Joint Channel
    Selection and Power Control in D2D Networks"
"""
import gurobipy as grb
import time
def ModelBuild(M, N, pMax, sigma, h, weight):       
    model = grb.Model("wireless_trans")
    """
    build the varibles used in the model
    """
    alpha = model.addVars(M, N, vtype = grb.GRB.BINARY, name = "alpha")
    p = model.addVars(M, vtype = grb.GRB.CONTINUOUS, name = "p")
    r = model.addVars(M, N, vtype = grb.GRB.CONTINUOUS, name = "r")
    gamma = model.addVars(M, N, vtype = grb.GRB.CONTINUOUS, name = "gamma")
    divisior = model.addVars(M, N, vtype = grb.GRB.CONTINUOUS, name = "div")
    model.update()
    for m in range(M):
        model.addConstr(grb.quicksum(alpha[m, i] for i in range(N)) <= 1, "AlphaCons(%s)"%m)
        model.addConstr(p[m] >= 0, "pmaxcons(%s)"%m)
        model.addConstr(p[m] <= pMax, "pmincons(%s)"%m)
        for n in range(N): 
            model.addConstr(sigma + grb.quicksum(alpha[i, n] * p[i] * h[i, n] for i in range(M) if i != m) == divisior[m, n])  
            model.addConstr((alpha[m, n] * p[m] * h[m, n] + divisior[m, n] - divisior[m, n] * gamma[m, n]) == 0)
            model.addGenConstrExp(r[m, n], gamma[m, n])
    model.write("ss.lp")
    model.setObjective(grb.quicksum(weight[m, n] * r[m, n] for (m, n) in r), grb.GRB.MAXIMIZE)
    model.setParam("NonConvex", 2)
    return model
  
def ModelSolve(model):         
  model.setParam('OutputFlag', 0)
  start = time.time()
  model.optimize()
  elapsed = (time.time() - start)
  print("Gurobi time used: " + str(elapsed))
  if (model.status == grb.GRB.OPTIMAL):
      print("Gurobi Model Cost %s"%model.objVal)
  else :
      print("failure")
  """for i in model.getVars():
      print('%s = %g' % (i.varName, i.x), end = " ")
  return"""