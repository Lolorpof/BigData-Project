# Have these python libraries install

### Library

1. networkx
2. pandas
3. matplotlib
4. acopy and acopy[plot]
5. aco_routing

```sh
pip install networkx
pip install pandas
pip install matplotlib
pip install acopy
pip install acopy[plot]
pip install aco_routing
pip install mplcursors
```

# Don't forget to insert 'results.csv' file into your own remote repo

# About current time in 'optimizedNow.py'

- Some system may use UTC+0 time so add `timedelta(hours=7)` to `currentTime`
