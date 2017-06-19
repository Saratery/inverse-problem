from __future__ import print_function
from random import choice
from operator import itemgetter
import oocyte

idealGraph = open("ICurrent.txt").readlines()
idealPotential = []
for line in idealGraph:
        numbers = line.split('\t')
	idealPotential.append(numbers)

#file = open("misfitFunction.txt", 'w')
global_counter = 1

def frange(start, end=None, inc=None):
	if end == None:
		end = start + 0.0
		start = 0.0

	if inc == None:
		inc = 1.0

	L = []
	while 1:
		next = start + len(L) * inc
		if inc > 0 and next >= end:
			break
		elif inc < 0 and next <= end:
			break
		L.append(next)
        
	return L

def init_param_str():
	out_param_str = []
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str.append(str(1.0))
	out_param_str = list(out_param_str)
    
	return out_param_str

def random_param_str():
	out_param_str = []
	out_param_str.append(str(param_cases(1)))
	out_param_str.append(str(param_cases(2)))
	out_param_str.append(str(param_cases(3)))
	out_param_str.append(str(param_cases(4)))
	out_param_str.append(str(param_cases(5)))
	out_param_str.append(str(param_cases(6)))
	out_param_str.append(str(param_cases(7)))
	out_param_str.append(str(param_cases(8)))
	out_param_str.append(str(param_cases(9)))
	out_param_str.append(str(param_cases(10)))
	out_param_str.append(str(param_cases(11)))
	out_param_str.append(str(param_cases(12)))
	out_param_str.append(str(param_cases(13)))
	out_param_str.append(str(param_cases(14)))
	out_param_str.append(str(param_cases(15)))
	out_param_str.append(str(param_cases(16)))
	#out_param_str.append(str(param_cases(17)))
	out_param_str = list(out_param_str)
    
	return out_param_str


def param_cases(index):
	if index == 15:
		result = choice(frange(0.000001, 0.01, 0.000005))
	elif index == 16:
		result = choice(range(-70, 10, 1))
	else:
		result = choice(frange(0.1, 10, 0.0005))
	return result

def mutation_cases(index, value):
	koeff_direction_mut = choice(range(-1, 2, 1))
	koeff_percent_mut = choice(frange(0.005, 0.1, 0.001))
	temp_param = koeff_direction_mut * koeff_percent_mut

	if index == 15:
		left_bound = 0.000001
		right_bound = 0.01
	elif index == 16:
		left_bound = -70
		right_bound = 10
	else:
		left_bound = 0.1
		right_bound = 10

	result = help_function_result(left_bound, right_bound, value, temp_param)
	return result
  
def help_function_result(left_bound, right_bound, value, param):
	temp_value = float(value) + float(value) * param 
	if temp_value > right_bound:
		result_value = right_bound
	elif temp_value < left_bound:
		result_value = left_bound
	else:
		result_value = temp_value
	return result_value


def mutate(member):
	max_index = len(member)
	mutated_index = choice(range(1,max_index))
	mutation_param = mutation_cases(mutated_index, member[mutated_index - 1])

	output_param = member
	output_param[mutated_index - 1] = str(mutation_param)

	return output_param

def reproduce(member, k):
	output = []
	for i in range(0,k):
		mutate_member = list(mutate(member))
        #print(mutate_member)
        #print(output)
		output.append(mutate_member)
	#print(output)
	return output

def select(offsprings, size, generation_index):
	#print(offsprings)
	survival_value = []
	for member in offsprings:
		if generation_index >= 2:
			member.pop()
		member.append(RunNeuron(member))
        	#print(member)
		survival_value.append(member)
	#print(survival_value)
	for i in range(0,10):
		happy = random_param_str()
		happy.append(RunNeuron(happy))
		survival_value.append(happy)
	select = sorted(survival_value, key=itemgetter(16))[:size]
	#print(select)
	return select

# generaction is the current set of strings
# offspring_size is the number of mutations 
def next_generation(generation, offspring_size, survival_size, generation_index):
	offsprings = []
	for member in generation:
		#print(member)
		offsprings += reproduce(member, offspring_size)
	#print(offsprings)
	next_generation = select(offsprings, survival_size, generation_index)
	return next_generation

def RunNeuron(member):
	#print(member)
	vector_potential = oocyte.executing(member)
	functional = FunctionalComparisonOfGraphs(vector_potential)
	return str(functional)

def FunctionalComparisonOfGraphs(dataVector):
	functional = 0
	for line in idealPotential:
		#print(line[0])
		#print('____')
		#print(dataVector[int(float(line[0])/0.025)])
		functional += (dataVector[int(float(line[0])/0.025)]/1000 - float(line[1])) ** 2
	functional = functional ** 0.5
	return functional	

	
def isPresent(generation, index, the_best_res, save):
	best_result = float(generation[0][16])

	#file.write(str(global_counter) + ' ' + str(best_result) + '\n')
	global global_counter 
	global_counter = global_counter + 1	
	

	if (best_result < the_best_res):
		the_best_res = best_result
		save = generation[0]

	print("best on this step:")
	print(generation[0])
	print("best:")
	print(save)

	if best_result < 1.0:
		print("best last:")
		print(generation[0])
		print("best_ever:")
		print(the_best_res)
		print(save)
		return True, the_best_res, save
	else:
		if index == 200:
			print("best last:")
			print(generation[0])
			print("best_ever:")
			print(the_best_res)
			print(save)
		return False, the_best_res, save

def evolution(max_num_generations=200):

# initial generation
	initial_str = init_param_str()
	generation = []
	generation.append(initial_str)
	num_of_offsprings = 100
	num_of_select  = 10
	generation_index  = 1
	condition = False
	the_best_res = 2000
	save = []
	while True:
		generation = next_generation(generation, num_of_offsprings, num_of_select, generation_index)
		condition, the_best_res, save = isPresent(generation, generation_index, the_best_res, save) # check the minimizing functional
		if condition:	
			break
		#if (generation_index >= 2):
		#	generation = list(map(lambda x: x[1], generation))
		generation_index += 1
		if generation_index > max_num_generations:
			raise Exception("Not reached in the maximal number of generations")
	return generation[0]

    
def print_evolution(sentence):
	out = evolution(sentence)
	number_of_generations = out[1]
	best = out[0]
	print(str(number_of_generations) + ","+ best.appearance)

def print_genes(sentence):
	out = evolution(sentence)
	best = out[0]
	for gene in best.genes:
		print(gene)
		print(best.appearance)

if __name__ == '__main__':
	evolution()

