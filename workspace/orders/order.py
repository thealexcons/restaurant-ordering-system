import time

# generates a unique ID from the current timestamp and takes 5 digits
def generate_unique_id():
    return str(int(time.time()*10000000))[10:15]

class Order:
    
    def __init__(self, orderContents, orderCategory, custID, orderID="", orderTime=0):
        if not orderID:
            self.id = generate_unique_id()
        else:
            self.id = orderID
        if orderTime == 0:
            self.timestamp = int(time.time())
        else:
            self.timestamp = orderTime
            
        self.contents = orderContents
        self.category = orderCategory
        self.customerId = custID
        
