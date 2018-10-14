#!Transaction Class
"""
This class getsd instantiated to represent Single transaction in NiNu's blockchain.
#Code: Prakash Chandra Chhipa(prakash.chandra.chhipa@gmail.com)
"""
import json
class Transaction:
    
	def __init__(self, senderAddress, recieverAddress, quantity, message):
		self.sendorAddress = senderAddress
		self.recieverAddress = recieverAddress
		self.quantity = quantity
		self.message = message
		
		
	def getTransactionData(self):
		#Transaction
		transaction = {"transactiondetail" :{ "sender": self.sendorAddress, "recipient": self.recieverAddress, "quantity": self.quantity, "message": self.message}}
		return transaction
