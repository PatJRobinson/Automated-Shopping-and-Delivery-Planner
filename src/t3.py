import csv
from copy import copy
import os
import sys

class Household:

    def __init__(self, name):
        self.shoppingList = []
        self.solutionList = []
        self.name = name
        self.deliveryDay = None



class Itineary:
    def __init__(self, shop, day):
        self.shop = shop
        self.items = []
        self.day = day

class Solution:

    def __init__(self, household):
        
        self.itemsBought = [] #item, shop bought at
        self.household = household
        self.itemsNeeded = household.shoppingList.copy()
        self.numSubstitutions = 0
        #probs dont need
        self.deliveryDay = None

    def shoppingCompletable(self, itineary, shop):

        
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
                    # putting bought into itineary to generate daily shopping list
                    itineary.items.append(item)
            if itemFound != True:
                    completable = False
            # remove item from needed
        for item in should_remove:
            self.itemsNeeded.remove(item)
        return completable



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


class Shop:
    def __init__(self, name):
        self.name = name
        self.stock_list = []


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

    def generate_solutions(self):

        # generate a single solution which buys all items needed from whichever shop stock them
        for household in self.households:
            solution = Solution(household)
            household.solution = solution

            
            i = 0
        for shop in self.shops:
            
            # copy items bought into itineary so data can be outputted in correct format
            newItineary = Itineary(shop, i)

            # for each shop, buy what can be bought from each household's shopping list, if all items can be bought, mark day for delivery
            for household in self.households:
                if (household.solution.shoppingCompletable(newItineary, shop)):
                    household.solution.deliveryDay = i
            self.dailyItineary.append(newItineary)
            i += 1
        
                

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

    #NOT USED
    main_types = ["Bread", "Milk", "Cheese", "Tomatoes", "Carrots", "Potatoes", "Rice", "Butter", "Spread", "Bacon", "Ham", "Eggs", "Apples", "Frozen peas", "Onions", "Oranges", "Kiwi", "Kitchen Roll", "Toilet roll", "Tea bags", "Coffee"]
    sub_types = ["White", "Brown", "canned", "Red", "Green", "Fresh"]

    fileA = "wk7DataA.csv"
    fileB = "wk7DataB.csv"

    #singleton delivery service
    delivery_service = DeliveryService(main_types, sub_types)

    #load in the csv file data for week 1
    load_week1_household_data(delivery_service, fileB)
    load_shop_data(delivery_service, fileA)
    
    # generate the solutions, 1 per household
    delivery_service.generate_solutions()
    
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



    input("Press Enter for Delivery Schedule")
    print("WEEK 1")
    print("Delivery Schedule")
    print(" ")

    for itineary in delivery_service.dailyItineary:

        print("Day " + str(itineary.day + 1))
        for household in delivery_service.households:
            solution = household.solution
            if (solution.deliveryDay == itineary.day):
                myArgs = []
                for item in solution.itemsBought:
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

    # generate the solutions, 1 per household
    delivery_service.generate_solutions()
    
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



    input("Press Enter for Delivery Schedule")
    print("WEEK 2")
    print("Delivery Schedule")
    print(" ")

    for itineary in delivery_service.dailyItineary:

        print("Day " + str(itineary.day + 1))
        for household in delivery_service.households:
            solution = household.solution
            if (solution.deliveryDay == itineary.day):
                myArgs = []
                for item in solution.itemsBought:
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
 