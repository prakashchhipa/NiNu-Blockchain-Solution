#!BlockchainNodeRunner Class
"""
This class serves as service API for each blockchain node. It is Flask based REST APIs provider which runs as server.
It exposes APIS forthe following:
1) Node Registration - This post API allows peer to peer node registration whereas each node manages its own copy of block chain
2) New Transaction - This API used to perform a new transation in blockchain
3) Mining - Perfoms mining operation using proof of work to add new block in blockchain. Miner always build consensus first to make sure to have longest 
   proven blockchain before mining and adding new block.
4) consensus Building - Build consenses among peer to peer connected nodes and make sure to have most authoritive copy of blockchain
5) Blockchain details - List out blockchain completely

Note: Multiple BlockchainNodeRunner needs to be run on different ports to articulate different nodes of blockchains

#Code: Prakash Chandra Chhipa(prakash.chandra.chhipa@gmail.com)
"""
from BlockchainOperation import BlockchainOperation

from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request
from flask.ext.cors import CORS, cross_origin
import json
        
class BlockchainNodeRunner:
        
        def __init__(self):
                #Different active miners node list
                self.blockchainNodeList = set()
                self.blockchainOpr = BlockchainOperation()
                self.minerId = str(uuid4())
                self.host = None
                self.port = 0
                #Genesis block added at starting of node
                self.blockchainOpr.initiateGenesisBlock()


bNodeRunner = BlockchainNodeRunner()
app = Flask(__name__)		
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
                
@app.route('/node/mine', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def performMining():
        """
        performs mining to add new block in blockchain
        No input, it output newly aqdded block details
        """
        newBlock = bNodeRunner.blockchainOpr.addNewBlock(bNodeRunner.minerId)
        if newBlock is not None:
                return jsonify({"nodeId": bNodeRunner.minerId,"blocknumber": newBlock.index,"block" : str(newBlock.getBlockData().decode("utf-8"))}), 200
        else:
                return None, 403
                
@app.route('/node/registration', methods=['POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def nodesRegistration():
        """
        Peer to peer node registration to build network of connected nodes 
        -Advancement: This functionality could be automated using resource manager e.g. zookeeper
        :return: blockchain
        """
        params = request.args
        blockchainNodes = params['nodelist']
        if blockchainNodes is not None:
                blockchainNodeList = blockchainNodes.split(",")
                for bNode in blockchainNodeList:
                        url = urlparse(bNode)
                        if url.netloc:
                                bNodeRunner.blockchainNodeList.add(url.netloc)
                        elif url.path:
                                bNodeRunner.blockchainNodeList.add(url.path)
                        else:
                                raise ValueError('Invalid Blockchain Node Reference')
                                
        else:
                return "Blockchain node(s) not valid", 400

        return jsonify({"message": "Following nodes are now peer to peer connected:","nodes": list(bNodeRunner.blockchainNodeList),}), 201

@app.route('/node/transaction/new', methods=['POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def makeNewTransaction():
        """
        Addng transaction into current block by recieving transaction details in post request.
        :return: status message and status code
        """
        #html form purpose print(request.form)
        params = request.args
        mandatoryItems = ['sender', 'recipient', 'quantity', 'message']
        #if all(item in params for item in mandatoryItems):
                # Crreating and adding a new transaction in node's unconfirmed transactions list
        index = bNodeRunner.blockchainOpr.addUnconfirmedTransaction(params['sender'], params['recipient'], int(params['quantity']), params['message'])
        return jsonify({"status": f"Transaction queued successfuly & will be added to Block {index} after performing mining of node {bNodeRunner.minerId}", "transaction" : params}), 201
        #else:
    #    return 'Incomplete transaction details, new transaction entry fail.', 400

@app.route('/node/consensus', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def buildConsensus():
        """
        This operation ensures to have most authoritive and longest blockchain of the network for node.
        This operation should be called prior to mining new block and add it ito latest valid blockchain
        Advancement - In case of more number of nodes are there in network then consensus rule can be modified to opt out most common blockchain along wioth longest one.
        other nodes can validate the longest common blockchain before accepting as node's blockchain.
        """
        
        otherNodes = bNodeRunner.blockchainNodeList
        latestBlockchain = None
        mId = None
        status = None
        bchainlength = len(bNodeRunner.blockchainOpr.blockchain)
        for node in otherNodes:
                response = requests.get(f'http://{node}/node/blockchain')
                if response.status_code == 200:
                        #data = response.json()
                        #data=json.dumps(data, sort_keys=True).encode()
                        data=json.loads(response.json())
                        #print(data)
                        length=data['blockchainlength']
                        nodeChain = data['blockchain']
                        nodeId=data['nodeid']
                        #print(length,nodeId)
                        if length > bchainlength:
                                if bNodeRunner.blockchainOpr.chainValidation(nodeChain, length):
                                        latestBlockchain = nodeChain
                                        bchainlength = length
                                        mId = nodeId
                                        
        # Replace our chain if we discovered a new, valid chain longer than ours
        if None is not latestBlockchain:
                bNodeRunner.blockchainOpr.blockchain = bNodeRunner.blockchainOpr.loadBlockchainInMemoryFromJSON(latestBlockchain, bchainlength)
                status='Node ' + bNodeRunner.minerId + ' blockchain replaced by node ' + mId + ' blockchain'
                statusCode=201
        else:
                status='Node ' + bNodeRunner.minerId + ' blockchain is sustained'
                statusCode=200
        
        chain ="{\"nodeid\": \""+str(bNodeRunner.minerId)+"\",\"blockchainlength\":"+str(len(bNodeRunner.blockchainOpr.blockchain))+ ",\"blockchain\":["
        length = len(bNodeRunner.blockchainOpr.blockchain)
        for block in bNodeRunner.blockchainOpr.blockchain:
                chain = chain + "{\"block\":"
                chain = chain + block.getBlockData().decode("utf-8")
                chain = chain + "}"
                length = length - 1
                if length > 0:
                        chain = chain + ","
        chain = chain + "]}"
        return jsonify({"status": status, "blockchain": chain}), statusCode

@app.route('/node/blockchain', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def blockchainDetails():
        """
        Running node's blockchain
        """
        chain ="{\"nodeid\": \""+str(bNodeRunner.minerId)+"\",\"blockchainlength\":"+str(len(bNodeRunner.blockchainOpr.blockchain))+ ",\"blockchain\":["
        length = len(bNodeRunner.blockchainOpr.blockchain)
        for block in bNodeRunner.blockchainOpr.blockchain:
                chain = chain + "{\"block\":"
                chain = chain + block.getBlockData().decode("utf-8")
                chain = chain + "}"
                length = length - 1
                if length > 0:
                        chain = chain + ","
        
        chain = chain + "]}"
        print(chain)
        return jsonify(chain), 200

@app.route('/node/validate-blockchain', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def validateBlockchain():
        """
        Running node's blockchain
        """
        chain ="{\"nodeid\": \""+str(bNodeRunner.minerId)+"\",\"blockchainlength\":"+str(len(bNodeRunner.blockchainOpr.blockchain))+ ",\"blockchain\":["
        length = len(bNodeRunner.blockchainOpr.blockchain)
        for block in bNodeRunner.blockchainOpr.blockchain:
                chain = chain + "{\"block\":"
                chain = chain + block.getBlockData().decode("utf-8")
                chain = chain + "}"
                length = length - 1
                if length > 0:
                        chain = chain + ","
        
        chain = chain + "]}"
        #bchainJSON = json.dumps(chain, sort_keys=True).encode()
        data=json.loads(chain)
        length=data['blockchainlength']
        nodeChain = data['blockchain']
        if bNodeRunner.blockchainOpr.chainValidation(nodeChain, length):
                return jsonify({"status": f"Valid blockchain"}), 200
        return jsonify({"status": f"Invalid blockchain"}), 200

@app.route('/node/addinvalidtransaction', methods=['POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def addInvalidTransation():
        """
        Attempting to modify block by adding new transaction
        """
        params = request.args
        bNodeRunner.blockchainOpr.addTransactionInConfirmedBlock(params['sender'], params['recipient'], int(params['quantity']), params['message'], int(params['blocknumber']))
        return jsonify({"status": f"Transaction added in specified block", "transaction" : params}), 201
        

@app.route('/', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def startup():
        return 'NiNu blockchain node ' + str({bNodeRunner.minerId}) + ' running at ' + str(bNodeRunner.host)+ '-' + str(bNodeRunner.port)

if __name__ == '__main__':
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('-p', '--port', default=5000, type=int, help='node running on')
        args = parser.parse_args()
        bNodeRunner.port=args.port
        bNodeRunner.host='0.0.0.0'
        app.run(host=bNodeRunner.host, port=bNodeRunner.port, debug=True)

