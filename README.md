![icon](https://gitlab.com/matedulab/rpp-simulation/-/raw/master/assets/img/icon_64.png)

# Rock, Paper & Probabilities

Here is a software written in *python* to simulate the game **Rock, Paper & Probabilites**, a game we use to
introduce probability related concepts in mid-school classes. This tool may be useful to think about randomness
and how it affects the matches result.

### the game
Two special dices are designed. They have rocks, papers and scissors in their faces. You roll the dices then.
The output face of a dice is selected randomly, but the odds can be on your side.

### the simulations
You need **python3** and **pandas** and **matplotlib** libraries to run this software. Then, from the folder where
you copied the files simply run:

```python
from ppp import PPP
g = PPP("pathtojson/config.json")
```

You can configure the simulations trough a *.json* file which fields are:

- **dPath**: the folder to save data *.csv* files in.
- **cPath**: the folder to save chart *.png* files in.
- **name**: the base name for the output files.
- **language**: the language to use in the charts (English or Spanish).
- **iterations**: number of iteration for this simulation.
- **rollcount**: number of dice rolls in each iteration.
- **matchsize**: the number of rolls in a match.
- **discardtieds**: to decide if you want to discard tied rolls in match results.
- **computerdice**: the faces for the computer's dice.
- **playerdice**: the faces for the player's dice.


```json
{
	"dPath": "data/",
	"cPath": "charts/",
	"name": "testing",
	"language": "spanish",
	"iterations": 3,
	"rollcount": 50,
	"matchsize": 7,
	"discardtieds": true,
	"computerdice": "rock,rock,paper,paper,paper,scissors",
	"playerdice": "paper,paper,paper,paper,scissors,rock"
}
```

### the charts
The results of a simulation are automatically plotted to make reading the data an easy task. The charts are:

- **history**: the history or won, lost and tied rolls in each iteration.
- **difference**: won - lost rolls evolution in each iteration.
- **proportion**: the actual ratio of won, lost and tied rolls.
- **rolls and matches**: bar charts of rolls and matches total results.

![charts](https://gitlab.com/matedulab/rpp-simulation/-/raw/master/assets/img/charts.png)

You can play on your own [here](https://matedulab.gitlab.io/scripts/ppp.html?lan=eng).
