from controller import tester
import sys

t_for_comp = float(sys.argv[1])
alpha = float(sys.argv[2])
rave = int(sys.argv[3])
if(rave == 0):
    rave = None


t_for_comp1 = float(sys.argv[4])
alpha1 = float(sys.argv[5])
rave1 = int(sys.argv[6])
if(rave1 == 0):
    rave1 = None

num_iter = int(sys.argv[7])
policy0_params = (t_for_comp, alpha, rave)
policy1_params = (t_for_comp1, alpha1, rave1)
print(tester(policy0_params, policy1_params, num_iter))


