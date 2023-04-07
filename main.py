# simple simulation configuration
# config = {
# 	"simulation": {
# 		"markets": ["Market"],
# 		"agents": ["FCNAgents"],
# 		"sessions": [
# 			{	"sessionName": 0,
# 				"iterationSteps": 100,
# 				"withOrderPlacement": True,
# 				"withOrderExecution": False,
# 				"withPrint": True,
# 				"hifreqSubmitRate": 1.0
# 			},
# 			{	"sessionName": 1,
# 				"iterationSteps": 500,
# 				"withOrderPlacement": True,
# 				"withOrderExecution": True,
# 				"withPrint": True
# 			}
# 		]
# 	},

# 	"Market": {
# 		"class": "Market",
# 		"tickSize": 0.00001,
# 		"marketPrice": 300.0
# 	},
# 	"FCNAgents": {
# 		"class": "FCNAgent",
# 		"numAgents": 100,

# 		"markets": ["Market"],
# 		"assetVolume": 50,
# 		"cashAmount": 10000,

# 		"fundamentalWeight": {"expon": [1.0]},
# 		"chartWeight": {"expon": [0.0]},
# 		"noiseWeight": {"expon": [1.0]},
# 		"meanReversionTime":{"uniform":[50,100]},
# 		"noiseScale": 0.001,
# 		"timeWindowSize": [100, 200],
# 		"orderMargin": [0.0, 0.1]
# 	}
# }

# shock transfer configuration
config = {
	"simulation": {
		"markets": ["SpotMarket-1", "SpotMarket-2", "IndexMarket-I"],
		"agents": ["FCNAgents-1", "FCNAgents-2", "FCNAgents-I", "ArbitrageAgents"],
		"sessions": [
			{	"sessionName": 0,
				"iterationSteps": 100,
				"withOrderPlacement": True,
				"withOrderExecution": False,
				"withPrint": True,
				"maxNormalOrders": 3, "MEMO": "The same number as #markets",
				"maxHifreqOrders": 0
			},
			{	"sessionName": 1,
				"iterationSteps": 500,
				"withOrderPlacement": True,
				"withOrderExecution": True,
				"withPrint": True,
				"maxNormalOrders": 3, "MEMO": "The same number as #markets",
				"maxHifreqOrders": 5,
				"events": ["FundamentalPriceShock"]
			}
		]
	},

	"FundamentalPriceShock": {
		"class": "FundamentalPriceShock",
		"target": "SpotMarket-1",
		"triggerTime": 0,
		"priceChangeRate": -0.1,
		"enabled": True
	},
	"SpotMarket": {
		"class": "Market",
		"tickSize": 0.00001,
		"marketPrice": 300.0,
		"outstandingShares": 25000
	},
	"SpotMarket-1": {
		"extends": "SpotMarket"
	},
	"SpotMarket-2": {
		"extends": "SpotMarket"
	},
	"IndexMarket-I": {
		"class": "IndexMarket",
		"tickSize": 0.00001,
		"marketPrice": 300.0,
		"outstandingShares": 25000,
		"markets": ["SpotMarket-1", "SpotMarket-2"]
	},
	"FCNAgent": {
		"class": "FCNAgent",
		"numAgents": 100,
		"markets": ["Market"],
		"assetVolume": 50,
		"cashAmount": 10000,

		"fundamentalWeight": {"expon": [1.0]},
		"chartWeight": {"expon": [0.0]},
		"noiseWeight": {"expon": [1.0]},
		"noiseScale": 0.001,
		"timeWindowSize": [100, 200],
		"orderMargin": [0.0, 0.1]
	},

	"FCNAgents-1": {
		"extends": "FCNAgent",
		"markets": ["SpotMarket-1"],
		"fundamentalWeight": {"expon": [1.0]},
		"chartWeight": {"expon": [0.0]},
		"noiseWeight": {"expon": [1.0]}
	},
	"FCNAgents-2": {
		"extends": "FCNAgent",
		"markets": ["SpotMarket-2"],
		"fundamentalWeight": {"expon": [0.0]},
		"chartWeight": {"expon": [0.0]},
		"noiseWeight": {"expon": [0.2]}
	},
	"FCNAgents-I": {
		"extends": "FCNAgent",
		"markets": ["IndexMarket-I"],
		"fundamentalWeight": {"expon": [0.5]},
		"chartWeight": {"expon": [0.0]},
		"noiseWeight": {"expon": [1.0]}
	},
	"ArbitrageAgents": {
		"class": "ArbitrageAgent",
		"numAgents": 100,
		"markets": ["IndexMarket-I", "SpotMarket-1", "SpotMarket-2"],
		"assetVolume": 50,
		"cashAmount": 150000,
		"orderVolume": 1,
		"orderThresholdPrice": 1.0
	}
}

import random
# import matplotlib.pyplot as plt
from pams.runners import SequentialRunner
from pams.logs.agent_step_loggers import AgentOrderSaver

saver = AgentOrderSaver()

runner = SequentialRunner(
    settings=config,
    prng=random.Random(43),
    logger=saver,
)

runner.main()

import csv

# list of dictionary
orderlog = saver.agent_order_logs
print('Order Logs')
print(orderlog)

# Open a csv file for writing
with open("orderlog.csv", "w", newline="") as fp:
    for i in range(len(orderlog)):
        # take a dictionary from the list
        order = orderlog[i]
        # Create a writer object
        writer = csv.DictWriter(fp, fieldnames=order.keys())

        # Write the header row
        if i == 0:
            writer.writeheader()

        # Write the data rows
        writer.writerow(order)
    print('Done writing dict to a csv file')