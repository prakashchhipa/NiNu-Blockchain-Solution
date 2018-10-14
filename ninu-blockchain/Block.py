#!Block Class
"""
This class get instantiated to represent Single block in NiNu's blockchain.
#Code: Prakash Chandra Chhipa(prakash.chandra.chhipa@gmail.com)
"""
import json
class Block:
	def __init__(self, index, timestamp, transactions, previousBlockHash, proof):
		
		self.index = index
		self.previousBlockHash = previousBlockHash
		self.transactionList = transactions
		self.timestamp = timestamp
		self.proof = proof
		
	def getBlockData(self):
	
		block = {"blocknumber":self.index, "previousBlockHash" : self.previousBlockHash, "transactions" : self.transactionList, "timestamp": self.timestamp, "proof": self.proof }
		return json.dumps(block, sort_keys=True).encode()
    
	def getProof(self):
		"""
		return proof value of block
		"""
		return self.proof
