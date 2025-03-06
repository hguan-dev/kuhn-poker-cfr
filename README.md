# **Kuhn Poker CFR**

## **Overview**
This project implements the **Counterfactual Regret Minimization (CFR)** algorithm in Python to find **Nash equilibria** in Kuhn Poker. Using **iterative self-play**, the algorithm minimizes regret over multiple training iterations to compute a **near-optimal strategy**.

## **Introduction**
**Kuhn Poker** is a simplified version of poker that is valuable for studying poker strategy:

- The deck consists of only **three cards**: **J, Q, K**.
- Each player is dealt **one card** and antes **1 dollar** to play.
- Players take turns **betting** or **folding**.
- The winner is determined by **the highest card** if the game reaches a showdown.
- Betting mechanics are very simple: each player starts with an **initial bet**.

## **Algorithm: Counterfactual Regret Minimization (CFR)**
- **CFR** is an iterative **self-play algorithm** used to compute **Nash equilibria** in **imperfect information games**.
- In each iteration, **regret values** are updated for each decision based on how much better an alternative action would have been.
- Over time, the strategy converges toward an **optimal mixed strategy** that minimizes exploitability.

To learn more about the theory behind CFR, check out this [paper](https://drive.google.com/file/d/1RNVHA5PbgQGHAJjFnWxb3SKcdmVc6rDb/view?usp=sharing) by **Anna Zhao, Caroline Guerra, and Ingrid Yeung**.

---

## **Usage**
### **1. Install Dependencies**
Make sure you are in the **main project directory**, then run:

```bash
poetry install
```
### **2. Training the AI**
To train the AI and view the optimal strategy (without playing the game), run:

```bash
poetry run python src/main.py
```

### **3. Training and Playing the Game**
To train the AI and play against it, run:

```bash
poetry run python src/kuhn_game.py
```
This will show the trained strategy for the AI and allow you to play the game.

## **Technologies**
Python, NumPy, Poetry
