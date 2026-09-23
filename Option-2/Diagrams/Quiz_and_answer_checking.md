# Questions and game rules

| Type | Idea | Example |
| --- | --- | --- |
| Multiple choice | This could be some techincal question, rather than what does strlen(hola) returns | Having to read some code and chose between 3 options answering "what does this code do" or having to chose the right definition or the man(3) page of the function given |
| Expected output | We give some good bunch of code to read instead of *insert strlen example haha* | "10 to 20 lines of code to read and understand" |
| Fill the code | Here as the example before, we give a big function and several slots to fill, and also a expected output so the person can make the code acordingly | *same as last one* |

## Checking answers

We prepare each question with its accepted answers:
- Multiple choice: check the selected option.
- Expected output: compare the answer with the program’s expected output.
- Fill the code: check all gaps against accepted combinations. The whole answer must be correct.

We explain whether spaces, capitals, and line breaks matter. We check prepared answers without running submitted code, so questions must have clear, limited possible answers.

>Two teammates must review each exercise and its solution.

## Game rules to agree on

- Two players start with the same amount of time.
- Each answers at their own pace, with all three question types mixed together.
- A correct answer adds time to their timer.
- A wrong answer removes time from their timer.
- Skipping gives extra time to the opponent.
- When a player’s timer reaches zero, they stop answering.
- Once both finish, whoever has the most correct answers wins. Equal totals mean a draw.

We still need to choose the starting time, bonuses, and penalties. We can later give harder questions more points, we see idk.
I suggest one submission per question, then moving on. We also need a maximum match length so repeated bonuses cannot keep the game running indefinitely.
Maybe we can even do a 3 round match, best of 3.

## Fair play

- If a player disconnects, both timers stop until recconection and we blurr the screen, so the person that is still connected has no advantage.
- Show whether an answer was correct immediately, because it changes the timer. Keep full solutions hidden until the match ends.
- The server controls both timers, checks answers, and counts each submission once. Reconnecting or refreshing cannot reset time or repeat a reward.
- Both players should receive a comparable mix of question types and difficulty. We should do layers of questions, and after 3 right answers, we go up a level of dificulty (for example)
- If the timer alredy runned out for the player, and another player skips a question, this bonus is not given.

## Disconnects and results

- Allow a short reconnect window while the player’s timer keeps running.
- Leaving or failing to reconnect causes a forfeit. If both disconnect, cancel the match without a winner. Server errors must not count as wrong answers.
- Save the result and total points once. Person 4 checks answers, Person 2 handles timers and rules, and Person 3 handles storage.

>These changes still support the subject’s game and remote-player modules (p.16); they do not add module points by themselves.