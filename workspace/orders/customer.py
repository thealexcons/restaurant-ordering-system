import time
from .order import generate_unique_id

class Customer:
    
    def __init__(self, custName, custSurname, contactNumber, custID=""):
        if not custID:
            # add 255 to avoid clash with order id
            self.id = str(int(generate_unique_id()) + 255)        
        else:
            self.id = custID
            
        self.firstName = custName
        self.surname = custSurname
        self.telephone = contactNumber
        
    