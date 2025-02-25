# kuhn-poker-cfr

## Overview
An implementation of the the Counterfactual Regret Minization (CFR) algorithm in Python to find the Nash equilibria in Kuhn Poker.
Uses iterative self-play through our engine to minimize regret over training iterations to compute a near-optimal strategy for Kuhn Poker.

## Introduction
Kuhn Poker is a simplified version of poker that is valuable for studying poker strategy.
* The deck consists only of three cards: J, Q, K
* Each player is dealt one card and antes 1 dollar to play 
* Players take turns betting or folding
* Winner is determined by the highest card if the game reaches a showdown
* Betting mechanics are very simple: each player starts with a initial bet

## Algorithm (Counterfactual Regret Minimization)
* CFR is an iterative self-play algorithm used to compute Nash equilibria in imperfect information games.
* At each iteration, regret values are updated for each decision based on how much better an alternative action would have been.
* To read more on the theory, please read [this](https://drive.google.com/file/d/1RNVHA5PbgQGHAJjFnWxb3SKcdmVc6rDb/view?usp=sharing) written by Anna Zhao, Caroline Guerra, and Ingrid Yeung

## Usage
To train the algorithm:

1. Make sure you are in the main project directory. Then use 
   ```bash
   cd /path/to/main-directory
2. Run the following:
    ```bash
    python3 src/kuhn_trainer.py
    