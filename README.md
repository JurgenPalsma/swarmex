# M.Sc Advanced Computer Science dissertation project

The goal of the project is to optimize trading strategies based on Directional Changes using nature inspired optimization algorithms. (so far: Particle Swarm Optimization (PSO))

## Running the experiment:

Step 1: run the java server which generates directional change events from the FOREX data (a sample is provided)
```
java -jar dc-server.jar data/fx-spot_EUR_GBP_10min_201308.txt:fx-spot_EUR_GBP_10min_201308:0:20:21:27 1000 35 4 0.90 0.10 0.0025 5 200 500000 -1 0.2 3 1 0.01
```

Step 2: run the PSO algorithm 
```
python main.py
```
