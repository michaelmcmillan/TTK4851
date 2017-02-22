#Class for the Generic search node used in the A* algorithm
class GenericSearchNode:	
	state = None								#State of the node, should be unique to that node(e-g- coordinates in a grid)	
	g = None									#the cost of the next node
	h = None									#heuristic, the minimal cost-estimate from thos ndoe to the goal, should never be overestimated
	f = None									#f+g	
	parent = None								#the best parent node of this node	
	kids = None									#all successors of this node
									
	def __init__(self, state):					#Initialising the search node				
		self.g = 0									
		self.h = 0									
		self.f = 0									
		self.state = state									
		self.kids = []									
									
									
	def calc_f(self):							#calculate f = g+h		
		return self.h + self.g									
	def is_goal(self):							#To be implemented in the spcialised case of using the A* algorithm, returns true if tou are at the goal state	
		raise NotImplementedError									
	def calc_h():								#To be implemented in the spcialised case of using the A* algorithm, calculates h
		raise NotImplementedError									
	def generate_all_successors():				#To be implemented in the spcialised case of using the A* algorithm, generates all successor nodes					
		raise NotImplementedError									
	def arc_cost(self, c):					#To be implemented in the spcialised case of using the A* algorithm, calculates the cost of getting from this node to the next					
		raise NotImplementedError									