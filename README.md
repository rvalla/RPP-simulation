![icon](https://gitlab.com/matedulab/matedulab.gitlab.io/-/raw/master/public/assets/img/icon_64.png)

# Rock, Paper & Probabilities

Here is a software written in *python* to simulate the game **Rock, Paper & Probabilites**, a game we use to
introduce probability related concepts in mid-school classes. This tool may be useful to think about randomness
and how it affects the matches result.

### the game
Two special dices are designed. They have rocks, papers and scissors in their faces. You roll the dices then.
The output face of a dice is selected randomly, but may be the odds are on your side.

### the simulations
You can configure a simulation trough a *.json* file. You have to decide how many rolls the software will simulate
and the number of iterarions to be run.

```json
{
  "oPath": "data/",			 //output path
  "name": "testing", 		 //the simulation name
	"language": "spanish", //language for charts titles and labels
	"iterations": 3,			 //number of iterations
	"rollcount": 50,			 //dice rolls in each iteration
	"matchsize": 7,				 //size of a match in rolls
	"discardtieds": true,	 //decide to discard tied rolls on matches decisions
	"computerdice": "rock,rock,paper,paper,paper,scissors",
	"playerdice": "paper,paper,paper,paper,scissors,rock"
}
```
### the charts
The results of a simulation are automatically plotted to make reading the data an easy task.

You can play on your own [here](https://matedulab.gitlab.io/scripts/ppp.html?lan=eng).
