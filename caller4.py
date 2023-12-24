from controller import tester
import sys

time_for_agents = float(sys.argv[1])
num_iter = int(sys.argv[2])
policy0_params = (time_for_agents, 0, None)
policy1_params = (time_for_agents, .5, None)
print(tester(policy0_params, policy1_params, num_iter, amaf_debug = 1))

