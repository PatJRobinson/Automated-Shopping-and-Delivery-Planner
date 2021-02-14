import csv
from copy import copy
import os
import sys

#Student number: 19026717
class Household:

    def __init__(self, name):
        self.shoppingList = []
        self.solutionList = []
        self.name = name
        self.deliveryDay = None


    def schedule(self, permutation, day):
        # construct a new solution
        candidateSolution = Solution(permutation, self)
        # attempt to buy each item needed from 1st shop
        if candidateSolution.shoppingCompletable(permutation.shops[day]) == True:
            if (len(candidateSolution.itemsNeeded) == 0):
                candidateSolution.deliveryDay = day
                self.solutionList.append(candidateSolution)

        # attempt to buy each item needed from 1st shop
        elif (candidateSolution.shoppingCompletable(permutation.shops[day + 1]) == True):
            if (len(candidateSolution.itemsNeeded) == 0):
                candidateSolution.deliveryDay = day + 1
                self.solutionList.append(candidateSolution)

        else:
        # make substitutions for all items which could not be bought at first or second shop, record number of substitutions to quantify solution's quality
            candidateSolution.makeSubstitutions(permutation.shops[day], permutation.shops[day + 1])
            if (len(candidateSolution.itemsNeeded) == 0):
                candidateSolution.deliveryDay = day + 1
                self.solutionList.append(candidateSolution)
                #print("substitution " + self.name + " " + str(len(candidateSolution.itemsNeeded)))
        candidateSolution.store1 = permutation.shops[day]
        candidateSolution.store2 = permutation.shops[day + 1]

class Itineary:
    def __init__(self, shop, day):
        self.shop = shop
        self.items = []
        self.day = day

class Solution:

    def __init__(self, permutation, household):
        self.permutation = permutation
        self.itemsBought = [] #item, shop bought at
        self.household = household
        self.itemsNeeded = household.shoppingList.copy()
        self.numSubstitutions = 0
        #probs dont need
        self.deliveryDay = None

    def shoppingCompletable(self, shop):
        
        completable = True
        should_remove = []
        # cycle through each item remaining on items needed
        for itemNeeded in self.itemsNeeded:
            itemFound = False
            for itemAvailable in shop.stock_list:    
                if (itemAvailable.name == itemNeeded.name):
                    should_remove.append(itemNeeded)
                    # keep record of item bought and which shop is bought at (not which day?)
                    item = copy(itemAvailable)
                    item.store = shop
                    self.itemsBought.append(item)
                    itemFound = True
            if itemFound != True:
                    completable = False
            # remove item from needed
        for item in should_remove:
            self.itemsNeeded.remove(item)
        return completable

    def makeSubstitutions(self, shop1, shop2):
        
        for itemNeeded in self.itemsNeeded:
            should_remove = False
            for itemAvailable in shop1.stock_list:
                if ((itemAvailable.main_type == itemNeeded.main_type) and (itemAvailable.sub_type == itemNeeded.sub_type)):
                    should_remove = True
                    item = copy(itemAvailable)
                    item.store = shop1
                    item.substitution = True
                    item.subbedItem = itemNeeded
                    self.itemsBought.append(item)
                    self.numSubstitutions += 1
            if should_remove:
                self.itemsNeeded.remove(itemNeeded)

        for itemNeeded in self.itemsNeeded:
            for itemAvailable in shop2.stock_list:
                if ((itemAvailable.main_type == itemNeeded.main_type) and (itemAvailable.sub_type == itemNeeded.sub_type)):
                    should_remove = True
                    item = copy(itemAvailable)
                    item.store = shop2
                    item.substitution = True
                    item.subbedItem = itemNeeded
                    self.itemsBought.append(item)
                    self.numSubstitutions += 1
            if should_remove:
                self.itemsNeeded.remove(itemNeeded)
           # in case no items of same sub-type, or item has no sub_types, try same main_type

        for itemNeeded in self.itemsNeeded:
            for itemAvailable in shop1.stock_list:
                if (itemAvailable.main_type == itemNeeded.main_type):
                    should_remove = True
                    item = copy(itemAvailable)
                    item.store = shop1
                    item.substitution = True
                    item.subbedItem = itemNeeded
                    self.itemsBought.append(item)
                    self.numSubstitutions += 1
            if should_remove:
                self.itemsNeeded.remove(itemNeeded)

        for itemNeeded in self.itemsNeeded:
            for itemAvailable in shop2.stock_list:
                if (itemAvailable.main_type == itemNeeded.main_type):
                    should_remove = True
                    item = copy(itemAvailable)
                    item.store = shop2
                    item.substitution = True
                    item.subbedItem = itemNeeded
                    self.itemsBought.append(item)
                    self.numSubstitutions += 1
            if should_remove:
                self.itemsNeeded.remove(itemNeeded)

class Permutation:
    def __init__(self, number, shops):
        self.shops = shops
        self.totalSubstitutions = 0
        self.permutationNumber = number
        self.solutionList = []

class Item:
    #constructor
    def __init__(self, item_no, name, price):
        self.item_no = item_no
        self.name = name
        self.price = price
        self.stores = []
        self.main_type = None
        self.sub_type = None
        self.substitution = False
        self.subbedItem = None
        self.store = None

    #return item no
    def get_item_no(self):
        return self.item_no

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_stores(self):
        return self.stores
    
    def add_store(self, store_name):
        self.stores.append(store_name)

    def __str__(self):
        return "PRODUCT = " + self.name + ", PRICE = " + ", AVAILABLE IN THE STORES = " + str(self.stores)

class Shop:
    def __init__(self, name):
        self.name = name
        self.stock_list = []

class HouseholdList:

    def __init__(self):
        self.households = []

    def getHousehold(self, index):
        return self.households[index]

class DeliveryService:
    #constructor
    def __init__(self, main_types, sub_types):
        #the list of items and associated shops with stock
        self.stock_list = []
        #the shopping lists
        self.shopping_lists = []
        #categories for making substitutions - sub_types prioritised for more accurate substitutions
        self.main_types = main_types
        self.sub_types = sub_types
        self.households = []
        self.shops = []
        self.permutations = []
        self.dailyItineary = []

    # Generates all permutations of the shops  
    def generate_permutations(self):
        i = 0
        for permutation in self.permutate(self.shops):
            newPermutation = Permutation(i, permutation)
            self.permutations.append(newPermutation)
            i += 1

    def permutate(self,lst):


        # If lst is empty then there are no permutations 
        if len(lst) == 0: 
            return [] 
    
        # If there is only one element in lst then, only 
        # one permuatation is possible 
        if len(lst) == 1: 
            return [lst] 
    
        # Find the permutations for lst if there are 
        # more than 1 characters 
    
        l = [] # empty list that will store current permutation 
    
        # Iterate the input(lst) and calculate the permutation 
        for i in range(len(lst)): 
            m = lst[i] 
        
            # Extract lst[i] or m from the list.  remLst is 
            # remaining list 
            remLst = lst[:i] + lst[i+1:] 
        
            # Generating all permutations where m is first 
            # element 
            for p in self.permutate(remLst): 
                l.append([m] + p) 
        return l 

    def generate_solutions(self):

        #for i in range (1, len(self.permutations)):
            #permutation = self.permutations[i]
            for permutation in self.permutations:
                for household in self.households:
                    for x in range (0, len(permutation.shops) - 1):
                        # we only need solutions for n - 1 days, since each solution evaluates pair of shop, shop following 
                        household.schedule(permutation, x)

    # finds the best solution for each household, per permutation. This is because all solutions chosen will need to belong to the same
    # permutation. We will select the permutation with the lowest overall substitutions
    def evaluate_solutions(self):
        
        for permutation in self.permutations:
            for household in self.households:
                # dummy solution to start comparison
                bestSoFar = Solution(0, self.households[0])
                # High number to start comparison
                bestSoFar.numSubstitutions = 10000
                for solution in household.solutionList:
                    if ((len(solution.itemsNeeded) == 0) and (solution.numSubstitutions < bestSoFar.numSubstitutions) and (solution.permutation == permutation)):
                        bestSoFar = solution
                permutation.solutionList.append(bestSoFar)
                permutation.totalSubstitutions += bestSoFar.numSubstitutions

        # dummy permutation to start comparison
        bestPermutationSoFar = Permutation(15, [])
        # High number to start comparison
        bestPermutationSoFar.totalSubstitutions = 1000

        # find and return permutation with lowest substitutions
        for permutation in self.permutations:
            if (permutation.totalSubstitutions < bestPermutationSoFar.totalSubstitutions):
                bestPermutationSoFar = permutation
        
        return bestPermutationSoFar

    # Permutation now has list of solutions - 1 for each household. Data from solution, e.g. items, store bought from, needs to be transferred
    # into Itineary to allow desired output format
    def generate_shopping_and_delivery_schedule(self, permutation):
        
        for i in range (0, len(permutation.shops)):
            day = Itineary(permutation.shops[i], i)
            for solution in permutation.solutionList:
                for item in solution.itemsBought:
                    if (item.store == permutation.shops[i]):
                        day.items.append(item)
            self.dailyItineary.append(day)

    # resets all necessary fields in delivery service and households so 2nd week data can be read
    def resetData(self):
        #re-initialize delivery_service data
        self.permutations = []
        self.dailyItineary = []

            # re-initialize household data
        for household in self.households:
            household.shoppingList = []
            household.solutionList = []
            household.number = 0
            household.bestSolutions = []
            household.totalPermutationSubs = []
            household.deliveryDay = None
            household.toBuy = []

# loads shop data from CSV - shops, items available - stores in delivery_service
def load_shop_data(delivery_service, file_name):

    ITEM_NUMBER = 0
    NAME = 1
    COST = 2
    path = sys.path[0] + "\\.vscode\\"
    with open(os.path.join(path, file_name), "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter= ",")
        line_count = 0
        for row in csv_reader:
            #ignore the first row
            if line_count != 0:
                #construct a new item
                item = Item(row[ITEM_NUMBER], row[NAME], row[COST])
                #add the stores with stock
                for i in range(3,len(row)):
                    #if not empty. eg does contain a Y
                    if row[i] != "":
                        #use the index to identify the store name in the array
                        #item.add_store(get_store_name(i - 3))
                        delivery_service.shops[i - 3].stock_list.append(item)


                # add type and sub_types (if applicable) attributes to item to establish substitution priority
                # e.g. prioritise sub_type, if not available/not applicable sub with same type
                for main_type in delivery_service.main_types:
                    if (main_type in item.name):
                        item.main_type = main_type

                for sub_type in delivery_service.sub_types:
                    if (sub_type in item.name):
                        item.sub_type = sub_type
                # add item to the stock list
                delivery_service.stock_list.append(item)
            else:   # 1st line: column headers
                # populate shops[]
                i = 3
                # fixed bug - week 7 data reading empty cells as new shops
                while i < len(row) and row[i] != "":
                    newShop = Shop(row[i])
                    delivery_service.shops.append(newShop)
                    i += 1
            line_count += 1
    csv_file.close()

# loads household data from CSV - households, items needed - stores household in delivery_service.households and items needed in household.shoppingList
def load_week1_household_data(delivery_service, file_name):
    NAME = 0
    COST = 1
    path = sys.path[0] + "\\.vscode\\"
    with open(os.path.join(path, file_name), "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter= ",")
        line_count = 0
        for row in csv_reader:
            #ignore the first row
            if line_count > 1:
                #construct a new item
                item = Item(0, row[NAME], row[COST])
                #add the stores with stock
                for i in range(2,len(row)):
                    #if not empty. eg does contain a quantity
                    if row[i] != "":
                        #add item to household's shopping list, times its quantity
                        x = 0
                        while (x < int(row[i])) and (i < len(delivery_service.households) + 2):                      
                            delivery_service.households[i - 2].shoppingList.append(item)
                            x += 1


                # add type and sub_types (if applicable) attributes to item to establish substitution priority
                # e.g. prioritise sub_type, if not available/not applicable sub with same type
                for main_type in delivery_service.main_types:
                    if (main_type in item.name):
                        item.main_type = main_type

                for sub_type in delivery_service.sub_types:
                    if (sub_type in item.name):
                        item.sub_type = sub_type
                # add item to the stock list
                delivery_service.stock_list.append(item)
            elif line_count == 0:   # 1st line: column headers
                # populate households[]
                i = 2
                while i < len(row):
                    isNew = True
                    for household in delivery_service.households:
                        if (household.name == row[i]):
                            isNew = False
                    if (isNew):
                        newHousehold = Household(row[i])
                        delivery_service.households.append(newHousehold)
                    i += 1
            line_count += 1
    csv_file.close()
# The same, but for the following week
def load_week2_household_data(delivery_service, file_name):
    NAME = 0
    COST = 1
    path = sys.path[0] + "\\.vscode\\"
    with open(os.path.join(path, file_name), "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter= ",")
        line_count = 0
        for row in csv_reader:
            #ignore the first two rows
            if line_count > 1:
                #construct a new item
                item = Item(0, row[NAME], row[COST])
                #add the stores with stock
                for i in range(2 + len(delivery_service.households),len(row)):
                    #if not empty. eg does contain a quantity
                    if row[i] != "":
                        #add item to household's shopping list, times its quantity
                        x = 0
                        while (x < int(row[i])) and (i < (len(delivery_service.households) * 2) + 2):                      
                            delivery_service.households[i - 2 - len(delivery_service.households)].shoppingList.append(item)
                            x += 1


                # add type and sub_types (if applicable) attributes to item to establish substitution priority
                # e.g. prioritise sub_type, if not available/not applicable sub with same type
                for main_type in delivery_service.main_types:
                    if (main_type in item.name):
                        item.main_type = main_type

                for sub_type in delivery_service.sub_types:
                    if (sub_type in item.name):
                        item.sub_type = sub_type
                # add item to the stock list
            line_count += 1
    csv_file.close()

def main():
    print("SHOPPING DELIVERY SERVICE")

    #hard code the types and sub-types so system can make accurate substitutions
    main_types = ["Bread", "Milk", "Cheese", "Tomatoes", "Carrots", "Potatoes", "Rice", "Butter", "Spread", "Bacon", "Ham", "Eggs", "Apples", "Frozen peas", "Onions", "Oranges", "Kiwi", "Kitchen Roll", "Toilet roll", "Tea bags", "Coffee"]
    sub_types = ["White", "Brown", "canned", "Red", "Green", "Fresh"]

    fileA = "wk4DataA.csv"
    fileB = "wk4DataB.csv"

    #singleton delivery service
    delivery_service = DeliveryService(main_types, sub_types)

    #load in the csv file data for week 1
    load_week1_household_data(delivery_service, fileB)
    load_shop_data(delivery_service, fileA)
    
    #generate the permutations
    delivery_service.generate_permutations()
    # generate the solutions
    delivery_service.generate_solutions()
    # find the best solutions per permutation, best permutation 
    best = delivery_service.evaluate_solutions()
    # format data for outputting
    delivery_service.generate_shopping_and_delivery_schedule(best)
    
    # driver prints data into shopping schedule - shopping list per shop, 1 shop per day - and delivery schedule - households per shop/day, items per household
    print("WEEK 1")
    input("Press Enter for Shopping Schedule")
    print("Shopping Schedule")
    print("")
    totalItems = 0
    for shoppingDay in delivery_service.dailyItineary:
        print ("day " + str(shoppingDay.day + 1) + ": " + shoppingDay.shop.name)
        print ("")
        itemsToday = 0
        myArgs = []
        for item in shoppingDay.items:
            if (item.substitution):
                myArgs.append(item.name + " (substitution for " + item.subbedItem.name + ")")
            else:
                myArgs.append(item.name)
            totalItems += 1
            itemsToday += 1
        myString = "%s" % ", ".join(myArgs)
        print(myString)
        print("Items " + str(itemsToday))
        print("total " + str(totalItems))
        print(" ")
        input("Press Enter to continue")
    print("Total substitustions " + str(best.totalSubstitutions))

    input("Press Enter for Delivery Schedule")
    print("WEEK 1")
    print("Delivery Schedule")
    print(" ")

    for itineary in delivery_service.dailyItineary:
        

        print("Day " + str(itineary.day + 1))
        for solution in best.solutionList:
            if (solution.deliveryDay == itineary.day):
                myArgs = []
                for item in solution.itemsBought:
                    if (item.substitution):
                        myArgs.append(item.name + " (sub)")
                    else:
                        myArgs.append(item.name)
                print("House " + solution.household.name + ": ")
                myString = "%s" % ", ".join(myArgs)
                print (myString)
                print(" ")
        print(" ")
        input("Press Enter to Continue")

    # re-initialize critical data fields to allow reading of new data, replacing week1 data 
    delivery_service.resetData()

    #load in the csv file data for week 2
    load_week2_household_data(delivery_service, fileB)


    #generate the permutations
    delivery_service.generate_permutations()
    # generate the solutions
    delivery_service.generate_solutions()
    # find the best solutions per permutation, best permutation 
    best = delivery_service.evaluate_solutions()
    # format data for outputting
    delivery_service.generate_shopping_and_delivery_schedule(best)
    
    # driver prints data into shopping schedule - shopping list per shop, 1 shop per day - and delivery schedule - households per shop/day, items per household
    print("WEEK 2")
    input("Press Enter for Shopping Schedule")
    print("Shopping Schedule")
    print("")
    totalItems = 0
    for shoppingDay in delivery_service.dailyItineary:
        print ("day " + str(shoppingDay.day + 1) + ": " + shoppingDay.shop.name)
        print ("")
        itemsToday = 0
        myArgs = []
        for item in shoppingDay.items:
            if (item.substitution):
                myArgs.append(item.name + " (substitution for " + item.subbedItem.name + ")")
            else:
                myArgs.append(item.name)
            totalItems += 1
            itemsToday += 1
        myString = "%s" % ", ".join(myArgs)
        print(myString)
        print("Items " + str(itemsToday))
        print("total " + str(totalItems))
        print(" ")
        input("Press Enter to continue")
    print("Total substitustions " + str(best.totalSubstitutions))

    input("Press Enter for Delivery Schedule")
    print("WEEK 1")
    print("Delivery Schedule")
    print(" ")

    for itineary in delivery_service.dailyItineary:
        

        print("Day " + str(itineary.day + 1))
        for solution in best.solutionList:
            if (solution.deliveryDay == itineary.day):
                myArgs = []
                for item in solution.itemsBought:
                    if (item.substitution):
                        myArgs.append(item.name + " (sub)")
                    else:
                        myArgs.append(item.name)
                print("House " + solution.household.name + ": ")
                myString = "%s" % ", ".join(myArgs)
                print (myString)
                print(" ")
        print(" ")
        input("Press Enter to Continue")


    print("End of Program")


if __name__ == "__main__":
    main()
 