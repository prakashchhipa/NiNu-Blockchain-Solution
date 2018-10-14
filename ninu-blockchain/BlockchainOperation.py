#!BlockchainOperation Class
"""
This class contains all the NiNu's blockchain methods to support blockchain node which inludes trancations handlng, block addition
, proof of work and proof validation
#Code: Prakash Chandra Chhipa(prakash.chandra.chhipa@gmail.com)
"""

from Block import Block
from Transaction import Transaction
import hashlib as h
from time import time
import json

class BlockchainOperation:
        def __init__(self):
                #Unconfirmed Transaction list, yet to be added in block by miner
                self.unConfirmedTransactionList=[]
                #Ultimate chain which keeps block after proof of work
                self.blockchain=[]
                #Difficulty rule
                self.difficulty = "0000"
        
                
        def initiateGenesisBlock(self):
                genesisTransaction= Transaction("demosender", "demoreciever",0,"genesis") 
                genesisBlock = Block(1, 1526100000.50, [genesisTransaction.getTransactionData()], "e86cf0c857ac5554b16gkc1751c80da0za5c48d9e47463bd0f71f26438fd32fe", 161616)
                self.blockchain.append(genesisBlock)
        
        def getLatestBlock(self):
                return self.blockchain[-1]
                
        def getPendingTransactionList(self):
                return self.unConfirmedTransactionList
                
        def resetPendingTransactionList(self):
                self.unConfirmedTransactionList = []
                
        def getIndexForNewBlock(self):
                return len(self.blockchain) + 1

        def addUnconfirmedTransaction(self, senderAddress, recieverAddress, quantity, message):
                
                """
        Creates a new transaction to go into the next mined Block
        :param senderAddress: Address of the Sender
        :param recieverAddress: Address of the Recipient
        :param quantity: quantity to get exchanged from sender to reciever
        :return: The index of the Future Block which will hold this transaction
        """
                
                transaction = Transaction(senderAddress, recieverAddress, int(quantity), message)
                self.unConfirmedTransactionList.append(transaction.getTransactionData())
                #Future block index = length of blockchain + 1
                return len(self.blockchain) + 1
                
        def computeBlockHash(self, blockData):
                
                #computing hash over current block data
                return h.sha256(blockData).hexdigest() 
        
        def performProofOfWork(self, latestBlockProof, latestBlockHash):
                
                """
                this operations meant to be validate the generated hash value against the set difficulty level.
                :param latestBlockProof: latest block's proof value
                :param latestBlockHash: latest block's hash value
                :return prrof: valid proof value for new block to be added
                """
                #Intial proof value for block to be added
                newBlockProof = 0
                while self.checkNewBlockProofValidity(newBlockProof, latestBlockProof, latestBlockHash) is False:
                        newBlockProof = newBlockProof + 1
                
                #Returning legitimate value of proof which statisfy the difficulty level of PoW
                return newBlockProof
                
        def checkNewBlockProofValidity(self, newBlockProof, latestBlockProof, latestBlockHash):
                
                """
                Checks proof validaity against difficulty rule
                :param latestBlockProof: latest block's proof value
                :param latestBlockHash: latest block's hash value
                :param newBlockProof: new block proof value - incremnetally advised
                :return validity in terms of TRUE/FALSE
                """
                #Seed prepartion
                seed = f'{newBlockProof}{latestBlockProof}{latestBlockHash}'.encode()
                seedHash = self.computeBlockHash(seed)
                seedHashInitials = seedHash[:4]
                #Successful if difficultylevel matched or not
                return seedHashInitials == self.difficulty
                
        def addNewBlock(self, minerId):
        
                """
                Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
                #Computing hash- SHA256 for previous block
                latestBlockHash = self.computeBlockHash(self.getLatestBlock().getBlockData())
                #Computing proof of work for previous block 
                newBlockProof = self.performProofOfWork(self.getLatestBlock().getProof(), latestBlockHash)
                
                #Add reward for correct proof of work than others
                self.addUnconfirmedTransaction("system", minerId, 1, "generated new coin as reward")
                
                #Creating new block and adding pending transactions

                newBlock = Block(self.getIndexForNewBlock(), time(), self.getPendingTransactionList(), latestBlockHash, newBlockProof)
                
        #Emptying pending transaction list as those trancations are going to be added into new block
                self.resetPendingTransactionList()
                
                #Adding newly created block to ultimate chain
                self.blockchain.append(newBlock)
                return newBlock	
                
                
        def chainValidation(self, bchain, length):
        
                """
        Performs bockchain validatation
        :return: validity of blockchain True/False
        """
                
                previousBlock = bchain[0]
                chainLength = length
                idx = 1
                
                while chainLength > idx:
                        currentBlock = bchain[idx]
                        hashStored = currentBlock["block"]["previousBlockHash"]
                        hashCalculated = self.computeBlockHash(json.dumps(previousBlock["block"], sort_keys=True).encode())
                        print ("Stored Hash for " + str(previousBlock["block"]["blocknumber"]) + ":\n" + str(hashStored))
                        print ("calculated Hash for " + str(previousBlock["block"]["blocknumber"]) + ":\n" + str(hashCalculated))
                        #Check hash then Proof of Work correction
                        if hashStored == hashCalculated:
                                if True == self.checkNewBlockProofValidity(currentBlock["block"]["proof"], previousBlock["block"]["proof"], currentBlock["block"]["previousBlockHash"]):
                                        previousBlock = currentBlock
                                        idx = idx +  1
                                        continue
                                else:
                                        return False
                        else:
                                return False
                        
                        
                #All blocks validate so blockchain is validated
                return True
        
        def loadBlockchainInMemoryFromJSON(self, bchain, length):
        
                """
        Loads blockchain JSON into blockchain data strucutre in memory
        :return: blockchain list
        """
                idx = 0
                bchainList = []
                while length > idx:
                        block = bchain[idx]
                        prevBlockHash = block["block"]["previousBlockHash"]
                        blocknumber = int(block["block"]["blocknumber"])
                        proof = int(block["block"]["proof"])
                        timestamp = float(block["block"]["timestamp"])
                        transactions = block["block"]["transactions"]
                        tranLen = len(transactions)
                        tranListObj = []
                        for i in range(0,tranLen):
                                trx = transactions[i]["transactiondetail"]
                                trxMsg = trx["message"]
                                trxQ = int(trx["quantity"])
                                trxRec = trx["recipient"]
                                trxSender = trx["sender"]
                                trxObj = Transaction(trxSender, trxRec,  trxQ, trxMsg)
                                tranListObj.append(trxObj.getTransactionData())
                        block = Block(blocknumber, timestamp, tranListObj,  prevBlockHash, proof)
                        bchainList.append(block)
                        idx = idx + 1
                return bchainList

        def addTransactionInConfirmedBlock(self, senderAddress, recieverAddress, quantity, message, blocknumber):
                
                """
        Creates a new transaction to go into the next mined Block
        :param senderAddress: Address of the Sender
        :param recieverAddress: Address of the Recipient
        :param quantity: quantity to get exchanged from sender to reciever
        :param message: message in text
        :blocknumber: block in which new transaction is going to be added
        :return: True
        """
                
                transaction = Transaction(senderAddress, recieverAddress, int(quantity), message)
                listt = self.blockchain[blocknumber - 1].transactionList
                listt.append(transaction.getTransactionData())
                self.blockchain[blocknumber - 1].transactionList = listt
                return True
