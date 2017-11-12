I've chosen the 1triple train-set on astronauts. You can create a graph from this (or any of 1triple data) with "create_graph.py"). The graph for astronauts is available at "astronauts_graph.png".

The Q-A bot is available at "bot.py". My bot can answer questions about several astronauts and spacecrafts.

The questions the bot answers relate only to the subjects of tripples (e.g. basing on the tripple  "Alan_Bean | birthPlace | Wheeler,_Texas" bot will answer questions about Alan Bean but not about Wheeler / Texas)

If the tripple with the question's subject and relation exists, bot randomly chooses one of the answers provided in the data.

If the bot doesn't know an answer, it suggests googling the question and provides a google search link.

The questions that were tested:

- What is alma mater of Alan Bean?
- What is Alan Bean’s alma mater?
- Where did Alan Bean graduate from?
- Where did Alan Bean study?
- When was Alan Bean born?
- What is a birth name of Alan Bean?
- When did Alan Bean retire?
- What’s Alan Shepard’s occupation?
- What’s Alan Shepard’s status?
- What does Alan Shepard do?
- What’s Alan Shepard’s job?
- How much time Alan Shepard spent in space?
- When was Alan Shepard selected?
- Where's William Anders from?
- Who was the operator of Apollo 12?
- Who operated Apollo 12?
- Who was a commander of Apollo 12?
