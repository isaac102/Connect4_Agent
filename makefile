#arguments that need to be passed in to the test scripts are:
#	time_for_agent: the amount of time the agent gets per move
#	alpha: the alpha value if using a-amaf, otherwise 0
#	rave: the rave parameter (integer) if using rave, otherwise 0
#	num_iter: the number of time the agents should be played against each other

#output of teest scripts:
#	the output is a tuple with the first element being a tuple containing the parameters of the agents, and the seccond element being the number of wins for each agent
#	example: (((0.1, 0, None), (0.1, 0, 8), 10), {'mc_policy': 4, 'mc_policy1': 5, 'tie': 1})
#	in the example above, the first agent is standard mcts: the .1 means .1 secconds per move, the 0 means no amaf,a nd the None means no rave
#	the second agent is rave with parameter 8
#	mcts won 4, rave won 5, there was 1 tie

direction:
	cat directions	

analysis:
	cat project_analysis

# mcts vs mcts 
# The argements are time_for_agents, num_iter
# sample: python caller3.py .1 1
mcts-mcts:
	python caller3.py .1 1
	
# mcts vs rave of 8 
# The argements are time_for_agents, num_iter
# sample: python caller2.py .1 1
mcts-rave:
	python caller2.py .1 1
	

# mcts vs alpha-amaf with alpha of .5
# The argements are time_for_agents, num_iter
# sample: python caller1.py .1 1
mcts-amaf:
	python caller1.py .1 1
	

# Customizable call to play two computer agents against each other
# The argements are time_for_agent0, alpha0, rave0, time_for_agent1, alpha1, rave1, num_iter
# sample: python caller0.py .1 0 0 1 0 0 1
custom:
	python caller0.py .1 0 0 1 0 0 10

#to play computer vs human
# The argements are time_for_agent0, alpha0, rave0
# sample python callerh.py '.1' 0 0
human:
	python callerh.py 1 0 0

#to print out debug information to see that amaf is updated
# The argements are time_for_agents, num_iter
# sample: python caller4.py .1 1
amaf-debug:
	python caller4.py .1 1 
