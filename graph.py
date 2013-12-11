import os
from matplotlib import pyplot as plt

def plot(filename, title):
	train_x = []
	train_y_spread = []
	train_y_winner = []

	test_x = []
	test_y_spread = []
	test_y_winner = []
	lines = open('results/' + filename).readlines()
	for x in range(1,len(lines),5):
		split_lines = lines[x].split(' ')
		if split_lines[1][:-1] == 'TRAIN':
			train_x.append(int(split_lines[3].strip()))
			train_y_spread.append(float(lines[x + 1].split(':')[-1].strip('][\n\t ')))
			train_y_winner.append(float(lines[x+2].split(':')[-1].strip('[]\n\t ')));
		else:
			test_x.append(int(split_lines[3].strip()))
			test_y_spread.append(float(lines[x + 1].split(':')[-1].strip('][\n\t ')))
			test_y_winner.append(float(lines[x+2].split(':')[-1].strip('][\n\t ')))
	fig = plt.figure(title + ": Avg Spread")
	fig.suptitle(title + ": Avg Spread")
	#fig.canvas.set_title(title + ": Avg Spread")
	plt.subplot()
	plt.plot(train_x,train_y_spread, label= "Train")
	plt.subplot()
	plt.plot(test_x, test_y_spread, label = "Test")
	plt.legend()
	plt.show()

	fig = plt.figure(title + ": Avg Winner")
	fig.suptitle(title + ": Avg Winner")
	plt.subplot()
	plt.plot(train_x,train_y_winner, label=title + "Train")
	plt.subplot()
	plt.plot(test_x, test_y_winner, label=title + "Test")
	plt.legend()
	plt.show()







def main():
	results = os.listdir('results')
	result_name = ['Decision Tree Past 2 Games','Decision Tree Past 3 Games', 
				   'Decision Tree Past 4 Games', 'Decision Tree Past 5 Games',
				   'Decision Tree Past 6 Games', 'Decision Tree Past 7 Games',
				   'KNN Past 2 Games', 'KNN Past 3 Games', 'KNN Past 4 Games',
				   'KNN Past 5 Games', 'KNN Past 6 Games', 'KNN Past 7 Games'
				  ]
	for i, r in enumerate(results): 
		plot(r, result_name[i])
main()
