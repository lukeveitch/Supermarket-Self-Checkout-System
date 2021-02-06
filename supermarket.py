
"""
AUTHOR
============
Student ID: 10203166

FILE
============
supermarket.py

DESCRIPTION
============
This a module that allows a self-checkout customer to list the products on stock, 
add products from the stock to a shopping basket or remove products from it, list 
all the items in the basket, and produce a bill of the basket (applying two types of promotions).

Dictionaries stock and basket take the form described in docstring of loadStockFromFile().

FUNCTIONS
===========
sortDict()
loadStockFromFile()
listItems()
searchStock()
addToBasket()
prepareCheckout()
getBill()
main()
applyPromotions()

"""

import csv

def sortDict(dct):
    """
    DESCRIPTION
    -----------
    Function which sorts in ascending order a stock dictionary by its ident number.
    (The ident number is the first key of the nested stock dictionary)
        
    Parameter(s):
    -----------
    argument1 (dict): stock
        
    Returns:
    -----------
    dict: stock      
    """
    temp_list = sorted(dct.items(), key = lambda x:x[0])
    
    return dict(temp_list)


# ------- Task 1 ----------
def loadStockFromFile(filepath = 'stock.csv'):
    """   
    DESCRIPTION
    -----------
    Function which reads a .csv file in the same directory and creates a nested dictionary.
    If file is not specified default filename is stock.csv.
    If the file is outside the directory, the function returns an error message.
    
    Function needs to import csv to work.
    
    #The innerkeys are the identifying numbers 'indent'.
    
    #The outerkeys are of the following:
        name: a string representing the name of a product (e.g., Granny Smith Apples Loose)
        price: a floating point number representing the price (in Great Britain Pounds)
        unit: a string which is either pieces or kg, indicating whether the product is costed in pieces or per kilogram weight
        promotion: the value can either be None or a string get2pay1 or get4pay3
        group: refers to the group of promotion and it can either be None or an integer (the latter only when promotion is get4pay3)
        amount: refers to the amount of a product being available on stock; it can either be an integer (in case unit takes the value pieces) or a floating point number (in case unit takes the value kg).
    
    Parameter(s):
    -----------
    argument1 (dict): stock
        
    Returns:
    -----------
    string: error message
    dict: stock      
    """
    
    try:
        with open(filepath,'r') as f:
            reader = csv.reader(f)
            
            stock = {}
        
            for line in reader:
                data = line[0].split('|')    
                
                for pointer in range(len(data)):
                    if data[pointer] == 'None':
                        data[pointer] = None
                
                if data[5] == None:
                    pass
                else:           
                    data[5] = int(data[5])
                        
                try:        
                    if data[3] == 'kg':
                        data[6] = float(data[6]) 
                    elif data[3] == 'pieces':
                        data[6] = int(data[6])
                except ValueError:
                    continue
                stock[data[0]] = {'name': data[1], 
                                  'price': float(data[2]),
                                  'unit': data[3],
                                  'promotion': data[4], 
                                  'group': data[5],
                                  'amount': data[6]
                                  }    
            return stock
    except FileNotFoundError:
        return 'The .csv file you wish to read is not in the directory'



# ------- Task 2 ----------

def listItems(dct):
    """
    DESCRIPTION
    -----------
    Function which takes a dictionary as an input and returns a formatted table
    with the ident number, product name, price and amount from the stock.
    
    Parameter(s):
    -----------
    argument1 (dict): stock or basket
            
    Returns:
    -----------
    string: string formatted as a table      
    """
    dct = sortDict(dct)
    
    table = "\n {0:^8} | {1:<40} |  {2:^8} | {3:^11}".format("Ident", "Product", "Price", "Amount")
    table += ("\n-"+"-" * 9 + "+" + "-" * 42 + "+" + "-" * 11 + "+" + "-" * 12)
    
    for key, value in dct.items():
        table += ("\n  " + str(key) + " "*3 + "|" + " {name:<40} |  £{price:^7.2f} | {amount:^5}%s ".format(**value) %(dct[key]['unit']))
        
    return table

# ------- Task 3 ----------

def searchStock(stock, s): 
    """
    DESCRIPTION
    -----------
    The function searches the stock dictionary for the string input and returns a substock dictionary with the parts of the stock containing the string. 
    The substock dictionary takes the same format as the stock dictionary.
    
    The string s can be lower or uppercase with added spaces.
    The string cannot take spaces between the letters of a word or take special characters.
    If there is no such string within the stock, the function return an error message.
    
    Parameter(s):
    -----------
    argument1 (dict): stock (from loadStockFromFile())
    argument2 (string): s - what that you wish to lookup
        
    Returns:
    -----------
    dict: substock  
    string: error message    
    """
    substock = {}
    s = s.lower().strip()

    try:
        for ident in stock:
            
            names = stock[ident]['name'].lower()
            if s in names:
                substock[ident] = stock[ident]
        if substock != {}:
            return substock
        return 'The item you are searching for does not exist'
    except AttributeError:
        return 'Please insert a valid string'

    
# ------- Task 4 ----------    
    
def addToBasket(stock, basket, ident, amount):
    """ 
    DESCRIPTION
    -----------
    Function which adds or removes amount units of the product with identifier ident from the stock 
    to the basket and vice versa without promotions. The function returns a message, which can either be None or a string.
    
    Parameter(s):
    -----------
    argument1 (dict): stock (from loadStockFromFile())
    argument2 (dict): basket
    argument3 (string): identifier numer ident
    argument4 (float or int): amount of each product
    
    Returns:
    -----------
    NoneType: None
    String: message or error message
    """
    
    # 1st part if amount is positive
    if amount == 0:
        return 'Please insert an amount other than zero'
    try:
        if amount > 0:
            for outer in stock:
                for inner in stock[outer]:
                    #check ident number against stock
                    if outer == ident:
                       stock_amount = stock[ident]['amount']
                       
                       if stock_amount >= amount:
                           stock_amount -= amount # delete the amount from stock               
                           stock[ident]['amount'] = round(stock_amount,3) # update stock
                               
                           basket[ident] = dict(stock[ident]) #copy substock to basket       
                           basket[ident]['amount'] = amount   #update basket amount            
                           return None
                       if amount > stock_amount:
                          basket[ident] = dict(stock[ident]) #add amount of stock to basket
                          stock[ident]['amount'] = 0
                          return '\nCannot add this many %s to the basket, only added %s %s.' %(stock[ident]['unit'], stock_amount, stock[ident]['unit'] )
        if amount < 0:
            if not basket:
                return '\nYour basket is empty. So you cannot take from it. Apologies.'
            basket_amount = basket[ident]['amount']     
            if basket_amount > abs(amount):
                stock[ident]['amount'] -= amount
                basket[ident]['amount'] += amount
                return None
            elif basket_amount == abs(amount):
                del basket[ident]
                stock[ident]['amount'] -= amount
                return None
            elif basket_amount < abs(amount):
               stock[ident]['amount'] += basket_amount
               del basket[ident]
               return 'Cannot remove this many %s from the basket, only removed %s %s.' %(stock[ident]['unit'], basket_amount, stock[ident]['unit'])   
        return 'not enough in stock'
    except TypeError:
        return
# ------- Task 5 ----------
def prepareCheckout(basket):
    """ 
    DESCRIPTION
    -----------
    Function that returns a basket with an added value of amountPayable to each ident in the basket.
    AmountPayable is given the same value as amount.
    
    Parameter(s):
    -----------
    argument1 (dict): basket
    
    Returns:
    -----------
    dict: basket with an added value 'amountPayable' for each ident
    """
    for idents in basket:
        basket[idents]['amountPayable'] = basket[idents]['amount']
    return basket

# ------- Task 6 ----------

def getBill(basket):
    """ 
    DESCRIPTION
    -----------
    Function that returns a list nicely formatted as a table with the bill of the items in your basket.
    It adds the total cost of the items in your basket. Total is the sum of the price*amountPayable values in basket.
    
    Parameter(s):
    -----------
    argument1 (dict): basket
    
    Returns:
    -----------
    string: Displays the items in your basket and the total bill.
    """
    table = "\n  {0:<40} |  {1:^8} | {2:^11}|  {3:^8} ".format("Product", "Price", "Amount", "Payable")
    table += ("\n-"+"-" * 42 + "+" + "-" * 11 + "+" + "-" * 12 + "+" + "-" * 12)
    total = 0
    for key, value in basket.items():
        total += (basket[key]['amountPayable'])*(basket[key]['price'])
        if basket[key]['unit'] == 'pieces':
            table += ("\n  {name:<40} |  £{price:^7.2f} |{amount:^5}%s |".format(**value) %('pieces') + " £"+" "*2+str((basket[key]['amountPayable'])*(basket[key]['price'])))        
        else:
            table += ("\n  {name:<40} |  £{price:^7.2f} |{amount:^8}%s  |".format(**value) %('kg') + " £"+" "*2+str((basket[key]['amountPayable'])*(basket[key]['price'])))
    table += ("\n-"+"-" * 42 + "+" + "-" * 11 + "+" + "-" * 12 + "+" + "-" * 12)        
    table += ("\n  TOTAL: " + " "*61 + "£"+" "*2 +str(total))
    return table

# ------- Task 7 ----------

def main():
    """ 
    DESCRIPTION
    -----------
    Function that uses all the above functions to mimic a self-checkout system 
    which allows the customer to list the products on stock, add (remove) products 
    from the stock to their shopping basket, list the items in the basket, and display 
    a bill for the basket. It asks for an input from the user and displays any relevant messages.
    
    Parameter(s):
    -----------
    None
    
    Returns:
    -----------
    n/a
    """
    
    
    print("*"*75)
    print("*"*15+" "*10+"WELCOME TO NISA LOCAL"+" "*10+"*"*17)
    print("*"*75,"\n")
    
    try:
        while True:
            s = input("Input product-Ident, search string, 0 to display basket, 1 to check out: ").lower()
            occurences = 0 # variable to know how many of each item is in substock for addToBasket function
            
            if s == '0':
                if not basket:
                    print('\nYour basket is empty. Try another input.')
                    continue
                else:
                    print('\nYour current shopping basket:\n', listItems(basket))
                    continue
            elif s == '1':
                print(getBill(prepareCheckout(basket)))
                print('\nThank you for shopping with us! Come back soon.')
                break
            for idents in stock:
                names = stock[idents]['name'].lower()
                if s in names:
                    occurences +=1
                if s == idents:
                    try: 
                        numb_of_product = float(input(('How many {} of {} do you want to add to your basket? ').format(stock[s]['unit'], stock[s]['name'])))
                        if stock[idents]['unit'] == 'pieces':
                            numb_of_product = int(numb_of_product)
                            print(addToBasket(stock, basket, s, numb_of_product))
                        else:
                            print(addToBasket(stock, basket, s, numb_of_product))
                    
                    except ValueError:
                        numb_of_product = input(('Please insert an integer or a floating point number.\nHow many {} of {} do you want to add to your basket? ').format(stock[s]['unit'], stock[s]['name']))
                        print(addToBasket(stock, basket, s, numb_of_product))
                    break
            else:
                print('\nThere were %s search results for \'%s\' in the stock.' %(occurences, s))
                if occurences == 0:
                    print('Please try again.')
                    continue
                print(listItems(searchStock(stock, s)))
                
    except AttributeError:
        print('\nThere is no instance of this input in the stock. Please try again.')
        pass
if __name__ == '__main__':
    stock = loadStockFromFile('stock.csv')
    basket = { }
    main()



def applyPromotions(basket):
    
    """   
    DESCRIPTION
    -----------
    Function that applies the a discount if there is a promotion on that product.
    Applies the promotions get2for1 or get4for3.
    
    Parameter(s):
    -----------
    argument1 (dict): Basket

    Returns:
    -----------
    dict: Updated Basket with promotions added
   
    """
    
    for idents in basket:
       if basket[idents]['promotion'] == 'get2pay1': 
           if basket[idents]['amount'] == 2:
                basket[idents]['amountPayable'] = 1
                continue
           elif basket[idents]['amount'] % 2 == 0:
               basket[idents]['amountPayable'] //= 2 
               continue
           else:
             basket[idents]['amountPayable'] //= 2
             basket[idents]['amountPayable'] += 1
             continue
       if basket[idents]['promotion'] == 'get4pay3':
           for x in range(basket[idents]['amount']):
               if basket[idents]['amount'] % 4 == 0:
                   if 4*x == basket[idents]['amount']:
                       basket[idents]['amountPayable'] = 3*x 
                       continue
               if basket[idents]['amount'] %4 == 1:
                   if 4*x +1 == basket[idents]['amount']:
                       basket[idents]['amountPayable'] = 3*x+1 
                       continue
               if basket[idents]['amount'] %4 == 2:
                   if 4*x +2 == basket[idents]['amount']:
                       basket[idents]['amountPayable'] = 3*x+2 
                       continue
               if basket[idents]['amount'] %4 == 3:
                   if 4*x +1 == basket[idents]['amount']:
                       basket[idents]['amountPayable'] = 3*x+1 
                       continue
    return basket

