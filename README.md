# Automated-Shopping-and-Delivery-Planner
An automated system that reads data in the form of customer orders and outputs a shopping and delivery schedule to satisfy certain contstraints. The implementation follows a generate and test strategy to navigate the search space and find the optimal solution. 

Instructions:


1. extract files

- You should get a folder containing project files (cwA), within this folder is the 3 python files for each of the tasks, and a sub-folder (.vscode) containing the CSV files

2. To run the code:

- Open the python file for each task and run the main method. There is code inside the files which sets the path to the .vscode folder in the current directory	
- Once opened, run the main method (or run the python file and main method will run)
	- My interpreter was set to python 3.8 and 3.9 during testing
- The code will output to the console, just press enter to progress through the outputted data  

The Problem:

Constraints:
  - shopping, once bought, can only be stored overnight, and must be dispatched the following day.
  - only one shop can be visited per day 

Considering all of the constraints that must be satisfied, it is clear that each household’s shopping must
be delivered on consecutive days. To achieve this, however, substitutions can be made if necessary. It is
implied, however, that these substitutions should only be made when necessary – a shopping trip made
entirely of substitutions, whilst possible, would probably not satisfy the customers’ needs. Since, also,
that the necessity of a given item’s substitution depends entirely on the order in which shops are visited, and
this order is determined by trying to avoid the substitutions of other items, the search space is quite
large. For this reason, I have decided to adopt a “generate and test strategy”.

The solution:

For every household, “solutions” - constituting a shopping attempt on two consecutive days - are
generated and graded by their number of substitutions – the lower the better. To generate the
solutions, all possible permutations are made of the shops, allowing the creation of solutions which visit
every unique pair of shops. We will want to pick the best solution for each household, however all
solutions must belong to the same permutation, so instead each household’s best-solution-per-permutation is stored, each permutation will contain exactly one solution per household, and the permutation with the lowest overall substitutions is selected.

Implementation:
1. Import data – the only thing hard coded is the categories in which items will be classified for
substitution if necessary. All other data (the stores, the households, the items available at each
store, the items on each household’s shopping lists and their quantities) needs to be imported
from csv files. Adapting code given in a tutorial gave me load_shop_data() and
load_household_data(), which are store all data (eventually) inside the singleton
Delivery_Service.
2. permutate() – A recursive program that generates all possible permutations for a given input
list. Works regardless of the length of the list, so perfect for the three tasks which have either 3
or 4 shops
3. Generate_solutions() – see pseudo code. Attempts a shopping trip for each unique pair of shops
per household. Uses shoppingCompletable() to determine whether all items needed can be
bought. If substitutions are necessary, make_substitutions() swaps the item with an available
item of the same type (or preferably sub-type)
4. evaluate_solutions() – see pseudo code. Cycles through solutions in each permutation, selects
best overall permutation

Conclusion: 
I chose this strategy because, although it could have a higher computational overhead that a
more logic-oriented approach, it would scale well (solution lists may require some
management/pruning) and it should find the optimal overall solution. I also think it is quite neat
and easy to understand. 
