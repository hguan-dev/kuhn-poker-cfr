import time
from kuhn_game import KuhnGame
from kuhn_test import KuhnTest
from kuhn_trainer import train, nodeMap

# Train the game tree from scratch
train(iterations=10**6, saveName="kt-10M")  # Training happens here

# Initialize KuhnTest with the trained nodeMap
kt = KuhnTest()
kt.nodeMap = nodeMap

# Evaluate the trained strategy
print("Game value:", kt.gameValue())
print("Exploitability:", kt.exploitability())

# Play against the trained AI
game = KuhnGame()
game.AI = nodeMap  # Assign the trained strategy directly
game.playAI(go_first=False, bankroll=0)

