import math
var = 44
mod = 5

result = var - (var % mod)
xpos_ref = 10
xpos_robot = 0
ypos_ref = 10
ypos_robot = 0
THREASHOLD_COORDINATES = 5

if math.fabs(xpos_ref - xpos_robot) < THREASHOLD_COORDINATES:
    dist = math.fabs(ypos_ref - ypos_robot)
    print("1")

elif math.fabs(ypos_ref - ypos_robot) < THREASHOLD_COORDINATES:
    dist = math.fabs(xpos_ref - xpos_robot)
    print("2")
else:
    adj = xpos_ref - xpos_robot
    opp = ypos_ref - ypos_robot
    dist = math.sqrt(math.pow(adj, 2) + math.pow(opp, 2))
    print("3")
print dist