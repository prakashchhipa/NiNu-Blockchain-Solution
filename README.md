# NiNu-Blockchain-Solution
Educational purpose python based blockchain implementation.

**Yes, I 'm NiNu and this blockchain solution is all about my idea, please have a look :)**
![alt text](https://github.com/prakashchhipa/NiNu-Blockchain-Solution/blob/master/NiNu.jpg)

**NiNu's Blockchain:**
NiNu's blockchain is educational purpose python based blockchain implementation which demonstrate core concepts. It covers P2P network connections, transaction handling, block creation, block minng, consensus building, blockchain modification attempt and its counter effects.

**Execution Environment & Required Libraries:**
  1. Python 2.x
  2. Libraries
    - flask
    - flask.ext.cors
    - json
    - requests
    - urllib
    - uuid
    - hashlib
    - time

**Solution:**

Following are the classes developed for solution:
1) Transaction.py - Defines an entity of transaction between two parties
2) Block.py - Defines a block strcuture which contains all the required details of particular block
3) BlockchainOperation.py - All the operations of blockchain are implemented in this class
4) BlockchainNodeRunner.py - Blockchain operations are exposed as REST API

**Steps to Run All th Components With Examples**
**1) Running Nodes** - Run multiple miner nodes and check the node miner details calling API in browser mentioned below:
   1. python BlockchainNodeRunner.py -p 8080
		Command: Open browser and hit the URI: http://192.168.0.13:8080/
		Result: Chip blockchain node {'309e4a5e-92e3-4ae0-a880-cb83d59e7a3c'} running at 0.0.0.0-8080
   2. python BlockchainNodeRunner.py -p 8081
		Command: Open browser and hit the URI: http://192.168.0.13:8081/
		Result: Chip blockchain node {'bcaaa417-4022-48a7-b86f-cce4243c225a'} running at 0.0.0.0-8081
	 
	Note: node id could be different every time it is being started
	
**2) Node Registration** - Each node registers the other nodes to make P2P mesh (currently it is don thorugh RESP API manually. Later on it can be automatic using zookeeper)
	Command: Open google chrome app postman (REST API client) and call following APIs
	1. Node1 (309e4a5e-92e3-4ae0-a880-cb83d59e7a3c):
		http://192.168.0.13:8081/node/registration?nodelist=http://192.168.0.13:8080
		Result:
		{
			"message": "Following nodes are now peer to peer connected:",
			"nodes": [
			"192.168.0.13:8080"
			]
		}
	2. Node2 (bcaaa417-4022-48a7-b86f-cce4243c225a):
		http://192.168.0.13:8080/node/registration?nodelist=http://192.168.0.13:8081
		Result:
		{
			"message": "Following nodes are now peer to peer connected:",
			"nodes": [
			"192.168.0.13:8081"
			]
		}
	
**3) Making New Transaction** - Now add some transactions in each nodes using new transaction API
	Command: Open google chrome app postman (REST API client) and call following APIs
	Node1 (309e4a5e-92e3-4ae0-a880-cb83d59e7a3c):
	1. http://192.168.0.13:8080/node/transaction/new?sender=ninu&recipient=prakash&quantity=1500&message=fee
	Result:
	{
		"status": "Transaction queued successfully & will be added to Block 2 after performing mining of node 56dc0797-8244-437a-8a22-12f586fa6824",
		"transaction": {
			"message": "fee",
			"quantity": "1500",
			"recipient": "prakash",
			"sender": "ninu"
		}
	}
	2. http://192.168.0.13:8080/node/transaction/new?sender=shakar&recipient=boss&quantity=2500&message=rent
	Result:
	{
		"status": "Transaction queued successfully & will be added to Block 2 after performing mining of node 56dc0797-8244-437a-8a22-12f586fa6824",
		"transaction": {
			"message": "rent",
			"quantity": "2500",
			"recipient": "boss",
			"sender": "shakar"
		}
	}
	
	Node2 (bcaaa417-4022-48a7-b86f-cce4243c225a)
	1. http://192.168.0.13:8081/node/transaction/new?sender=prakash&recipient=meenu&quantity=46&message=moneytransfer
	Result:
	{
		"status": "Transaction queued successfully & will be added to Block 2 after performing mining of node bcaaa417-4022-48a7-b86f-cce4243c225a",
		"transaction": {
			"message": "moneytransfer",
			"quantity": "46",
			"recipient": "meenu",
			"sender": "prakash"
		}
	}
	2. http://192.168.0.13:8081/node/transaction/new?sender=meenu&recipient=prakash&quantity=146&message=shopping
	Result:
	{
		"status": "Transaction queued successfully & will be added to Block 2 after performing mining of node bcaaa417-4022-48a7-b86f-cce4243c225a",
		"transaction": {
			"message": "shopping",
			"quantity": "146",
			"recipient": "prakash",
			"sender": "meenu"
		}
	}
	
	
**4. Performing Mining Operation** - It adds up latest block into the node's it own version of blockchain  
    Command: Open google chrome browser and call following APIs
	1. Node1 (309e4a5e-92e3-4ae0-a880-cb83d59e7a3c):
   	 http://192.168.0.13:8080/node/mine
	Result:
	{
	  "block": "{\"blocknumber\": 3, \"previousBlockHash\": \"4198e72a85275918b5f8c4f8982e1f66190058ea0903eaf6e92d0f19f135707f\", \"proof\": 23596, \"timestamp\": 1526198142.2666097, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"56dc0797-8244-437a-8a22-12f586fa6824\", \"sender\": 0}}]}", 
	  "blocknumber": 2, 
	  "nodeId": "56dc0797-8244-437a-8a22-12f586fa6824"
	}
	2. Node2 (bcaaa417-4022-48a7-b86f-cce4243c225a):
	 http://192.168.0.13:8081/node/mine
	Result:
	{
	  "block": "{\"blocknumber\": 2, \"previousBlockHash\": \"e86cf0c857ac5554b165cc1751c80da0505c48d9e47463bd0f71f26438fd32fe\", \"proof\": 26289, \"timestamp\": 1526198071.6225345, \"transactions\": [{\"transactiondetail\": {\"message\": \"moneytransfer\", \"quantity\": \"46\", \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"shopping\", \"quantity\": \"146\", \"recipient\": \"prakash\", \"sender\": \"meenu\"}}, {\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"bcaaa417-4022-48a7-b86f-cce4243c225a\", \"sender\": 0}}]}", 
	  "blocknumber": 2, 
	  "nodeId": "bcaaa417-4022-48a7-b86f-cce4243c225a"
	}
	
	Note: Repeat step 3 & 4 multiple times, preferably in odd fashion that one miner get more block mining than others.

	
**5. Checking Individual Node's Blockchain** - until consensus is build each node will have their own version of blockchain
   	Command: Open google chrome browser and call following APIs
	1. Node1 (309e4a5e-92e3-4ae0-a880-cb83d59e7a3c):
	http://192.168.0.13:8080/node/blockchain
	Result:
	{
		"nodeid": "56dc0797-8244-437a-8a22-12f586fa6824",
		"blockchainlength": 6,
		"blockchain": [{
			"block": {
				"blocknumber": 0,
				"previousBlockHash": 23051989,
				"proof": 16,
				"timestamp": 0,
				"transactions": [{
					"transactiondetail": {
						"message": "genesis",
						"quantity": 0,
						"recipient": "demoreciever",
						"sender": "demosender"
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 2,
				"previousBlockHash": "e86cf0c857ac5554b165cc1751c80da0505c48d9e47463bd0f71f26438fd32fe",
				"proof": 26289,
				"timestamp": 1526198088.1780443,
				"transactions": [{
					"transactiondetail": {
						"message": "fee",
						"quantity": "1500",
						"recipient": "prakash",
						"sender": "ninu"
					}
				}, {
					"transactiondetail": {
						"message": "rent",
						"quantity": "2500",
						"recipient": "boss",
						"sender": "shakar"
					}
				}, {
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "56dc0797-8244-437a-8a22-12f586fa6824",
						"sender": 0
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 3,
				"previousBlockHash": "4198e72a85275918b5f8c4f8982e1f66190058ea0903eaf6e92d0f19f135707f",
				"proof": 23596,
				"timestamp": 1526198142.2666097,
				"transactions": [{
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "56dc0797-8244-437a-8a22-12f586fa6824",
						"sender": 0
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 4,
				"previousBlockHash": "4d4badd5c7d2c4ca6372db2bf8d6fd703b2b66dcfd6b7f7fa51a79e0ae62cfa3",
				"proof": 48731,
				"timestamp": 1526198835.568169,
				"transactions": [{
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "56dc0797-8244-437a-8a22-12f586fa6824",
						"sender": 0
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 5,
				"previousBlockHash": "9fe8cf0851770c681b33849dccf824d44f4b183f22d6c843740c8fbc43cecac7",
				"proof": 185561,
				"timestamp": 1526198836.2646298,
				"transactions": [{
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "56dc0797-8244-437a-8a22-12f586fa6824",
						"sender": 0
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 6,
				"previousBlockHash": "503f0b53b2925da0b1d5e59f605f87629b376c835ef79428d859905af6931599",
				"proof": 123367,
				"timestamp": 1526198840.9420302,
				"transactions": [{
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "56dc0797-8244-437a-8a22-12f586fa6824",
						"sender": 0
					}
				}]
			}
		}]
    }
	
	2. Node2 (bcaaa417-4022-48a7-b86f-cce4243c225a):
	http://192.168.0.13:8081/node/blockchain
	Result:
	{
		"nodeid": "bcaaa417-4022-48a7-b86f-cce4243c225a",
		"blockchainlength": 4,
		"blockchain": [{
			"block": {
				"blocknumber": 0,
				"previousBlockHash": 23051989,
				"proof": 16,
				"timestamp": 0,
				"transactions": [{
					"transactiondetail": {
						"message": "genesis",
						"quantity": 0,
						"recipient": "demoreciever",
						"sender": "demosender"
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 2,
				"previousBlockHash": "e86cf0c857ac5554b165cc1751c80da0505c48d9e47463bd0f71f26438fd32fe",
				"proof": 26289,
				"timestamp": 1526198071.6225345,
				"transactions": [{
					"transactiondetail": {
						"message": "moneytransfer",
						"quantity": "46",
						"recipient": "meenu",
						"sender": "prakash"
					}
				}, {
					"transactiondetail": {
						"message": "shopping",
						"quantity": "146",
						"recipient": "prakash",
						"sender": "meenu"
					}
				}, {
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "bcaaa417-4022-48a7-b86f-cce4243c225a",
						"sender": 0
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 3,
				"previousBlockHash": "19849d2d3afb907ac202478a683b60c27703e5f983eec083cd9602fe169af228",
				"proof": 42091,
				"timestamp": 1526198437.8842072,
				"transactions": [{
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "bcaaa417-4022-48a7-b86f-cce4243c225a",
						"sender": 0
					}
				}]
			}
		}, {
			"block": {
				"blocknumber": 4,
				"previousBlockHash": "944fb994f6ec8513ac5a8c53ed35280ba85502fc1c4a435df9285848eef9a491",
				"proof": 164211,
				"timestamp": 1526198442.502223,
				"transactions": [{
					"transactiondetail": {
						"message": "generated new coin as reward",
						"quantity": 1,
						"recipient": "bcaaa417-4022-48a7-b86f-cce4243c225a",
						"sender": 0
					}
				}]
			}
		}]
	}
	
**5. Consensus Building** - Simple rule is made for consensus, miner who has longer and valid chain will become global chain and to be adapted by other miners.
 -Call consensus API to any of one node (preferably the node which has less number of blocks becuase there we can observe blockchain replacement by the node which has biggest valid blockchain for now.)
 Command: http://192.168.0.13:8081/node/consensus
 Result(observe status field):
 {
  "blockchain": "{\"nodeid\": \"17217bcf-ad17-443b-8f0f-d07ad9dc6595\",\"blockchainlength\":10,\"blockchain\":[{\"block\":{\"blocknumber\": 1, \"previousBlockHash\": \"e86cf0c857ac5554b16gkc1751c80da0za5c48d9e47463bd0f71f26438fd32fe\", \"proof\": 161616, \"timestamp\": 1526100000.5, \"transactions\": [{\"transactiondetail\": {\"message\": \"genesis\", \"quantity\": 0, \"recipient\": \"demoreciever\", \"sender\": \"demosender\"}}]}},{\"block\":{\"blocknumber\": 2, \"previousBlockHash\": \"98910675ee2ca8d78c2d8608150f155d7cc82faea87103df1bfadd3c0af622fb\", \"proof\": 5146, \"timestamp\": 1526210980.114253, \"transactions\": [{\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 3, \"previousBlockHash\": \"0bc2cad278524f372ecd41da3d9b563f22106d1e32ba2505af55f75a824ffa8e\", \"proof\": 10453, \"timestamp\": 1526210982.5810392, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 4, \"previousBlockHash\": \"fa0e5a842aa04e92326fc552a554b11e5e147876003850432cd97a02388927cd\", \"proof\": 72860, \"timestamp\": 1526210983.4766116, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 5, \"previousBlockHash\": \"fe0763325e5965cf0541ec6802857ed798f3eda7219b527d620b26d33ed82e97\", \"proof\": 9466, \"timestamp\": 1526210983.9555817, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 6, \"previousBlockHash\": \"d378795f7a9732f01c098c0d1afc90193ccd287f5d442728e083f8b23b830524\", \"proof\": 6874, \"timestamp\": 1526210984.677862, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 7, \"previousBlockHash\": \"6a3ca3bd73efe73fd2d82e5584bb397c312aaf8bc6b2757a1edfaa10f5138270\", \"proof\": 79098, \"timestamp\": 1526210985.5609827, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 8, \"previousBlockHash\": \"78bf3bd92e686c16737acf7e2f8b4cc93d2dfdb07de43f99df7cf1a866ff20fe\", \"proof\": 21619, \"timestamp\": 1526210986.1302407, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 9, \"previousBlockHash\": \"74a953359d0b6fbab5db41befb59842538ea5f4352b1cc028fefc06d366417be\", \"proof\": 158230, \"timestamp\": 1526210987.5034947, \"transactions\": [{\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}},{\"block\":{\"blocknumber\": 10, \"previousBlockHash\": \"03d8ae480e793322f9f74158ac0570885ddd5f77e08f105c888538c4ac6c3282\", \"proof\": 12598, \"timestamp\": 1526211011.9985268, \"transactions\": [{\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"lbutoo\", \"quantity\": 46, \"recipient\": \"meenu\", \"sender\": \"prakash\"}}, {\"transactiondetail\": {\"message\": \"generated new coin as reward\", \"quantity\": 1, \"recipient\": \"1ef0d0b4-347d-46d6-b55c-0e1fa965793f\", \"sender\": \"system\"}}]}}]}", 
  "status": "Node 17217bcf-ad17-443b-8f0f-d07ad9dc6595 blockchain replaced by node 1ef0d0b4-347d-46d6-b55c-0e1fa965793f blockchain"
 }
 Additional Observation(Server command lines shows that blockchain hashes are validated):
 Stored Hash for 1:
	98910675ee2ca8d78c2d8608150f155d7cc82faea87103df1bfadd3c0af622fb
	calculated Hash for 1:
	98910675ee2ca8d78c2d8608150f155d7cc82faea87103df1bfadd3c0af622fb
	Stored Hash for 2:
	0bc2cad278524f372ecd41da3d9b563f22106d1e32ba2505af55f75a824ffa8e
	calculated Hash for 2:
	0bc2cad278524f372ecd41da3d9b563f22106d1e32ba2505af55f75a824ffa8e
	Stored Hash for 3:
	fa0e5a842aa04e92326fc552a554b11e5e147876003850432cd97a02388927cd
	calculated Hash for 3:
	fa0e5a842aa04e92326fc552a554b11e5e147876003850432cd97a02388927cd
	Stored Hash for 4:
	fe0763325e5965cf0541ec6802857ed798f3eda7219b527d620b26d33ed82e97
	calculated Hash for 4:
	fe0763325e5965cf0541ec6802857ed798f3eda7219b527d620b26d33ed82e97
	Stored Hash for 5:
	d378795f7a9732f01c098c0d1afc90193ccd287f5d442728e083f8b23b830524
	calculated Hash for 5:
	d378795f7a9732f01c098c0d1afc90193ccd287f5d442728e083f8b23b830524
	Stored Hash for 6:
	6a3ca3bd73efe73fd2d82e5584bb397c312aaf8bc6b2757a1edfaa10f5138270
	calculated Hash for 6:
	6a3ca3bd73efe73fd2d82e5584bb397c312aaf8bc6b2757a1edfaa10f5138270
	Stored Hash for 7:
	78bf3bd92e686c16737acf7e2f8b4cc93d2dfdb07de43f99df7cf1a866ff20fe
	calculated Hash for 7:
	78bf3bd92e686c16737acf7e2f8b4cc93d2dfdb07de43f99df7cf1a866ff20fe
	Stored Hash for 8:
	74a953359d0b6fbab5db41befb59842538ea5f4352b1cc028fefc06d366417be
	calculated Hash for 8:
	74a953359d0b6fbab5db41befb59842538ea5f4352b1cc028fefc06d366417be
	Stored Hash for 9:
	03d8ae480e793322f9f74158ac0570885ddd5f77e08f105c888538c4ac6c3282
	calculated Hash for 9:
	03d8ae480e793322f9f74158ac0570885ddd5f77e08f105c888538c4ac6c3282

	Note: Even a node recieves longer blockchain but status of blockchain is invalid due to modification then during consensus this type of blockchain is not considered.
	
**6. Adding Transaction in Previous Block(Attempting to modify the blockchain)** - During validation and consensus building a modified blokchain will be treated as invalid blockchain	
 Command(POST API in Google Chrome POSTMAN): http://192.168.0.13:8080/node/addinvalidtransaction?sender=prakash&recipient=meenu&quantity=46&message=lbutoo&blocknumber=2
 Result:
 {
    "status": "Transaction added in specified block",
    "transaction": {
        "blocknumber": "2",
        "message": "lbutoo",
        "quantity": "46",
        "recipient": "meenu",
        "sender": "prakash"
    }
}
**Note:** After attemping above operation, do not forget to check validity of blockchain

**7. Blockchain Validation** - As blockchain was modified so result shows invalidate blockchain
 Command(Google Browser): http://192.168.0.13:8080/node/validate-blockchain
 Result:
 {
  "status": "Invalid blockchain"
 }
	
**Note for other Enthusiastic Contributor:**

Geeks are welcome to further contribute and improvise this educational purpose blockchain ecosystem in following area:
1) Auto discovery and registration process to make system better 
2) Transactions could be shared across the nodes to add them in their individual blokchain and which mine first will win the race.
3) Consensus mechanism could be more comprehensive in which voting of other nodes can be introduced to validate mining/proof of work.
4) A UI to perform all the operations which are currently demonstrated through API calls
5) Anything you find towards betterment

**Queries?...Connect with me at:**
 1) LinkedIn: https://linkedin.com/in/prakash-chandra-chhipa
 2) Email: prakash.chandra.chhipa@gmail.com
