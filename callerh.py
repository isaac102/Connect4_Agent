from controller import tester
import sys
#
#policy0_params = (.1, 0, None)
#policy1_params = (.1, .5, None, 0)

t_for_comp = float(sys.argv[1])
alpha = float(sys.argv[2])
rave = int(sys.argv[3])
if(rave == 0):
    rave = None
policy0_params = (t_for_comp, alpha, rave)
policy1_params = None
print(tester(policy0_params, policy1_params, 1, 1))


