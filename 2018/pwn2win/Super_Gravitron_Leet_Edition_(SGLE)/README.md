# Super Gravitron Leet Edition (SGLE)

## The task

```
Super Gravitron Leet Edition (SGLE)

Do you know the Super Gravitron by VVVVVV (https://www.youtube.com/watch?v=CQ-3-K1Ro2g)? Yes, Terry Cavanagh is a genius! And the bavs tasked with recruiting new programmers made a version of this game that runs on the console, and use it in their recruitment program! We're trying to infiltrate their IT sector, so we need your programming skills to beat the game, by creating a bot that can last 137 seconds in it!

Instructions:
1 - You can only move horizontally, as in the original game, using the directional keys (<- and ->);
2 - The objective is "just" to avoid the obstacles;
3 - When you hit an obstacle, it will be marked with an "X". Press or to exit;
4 - Press or " to close the game at any time;"
5 - The elapsed time and the position of the Jumper(I) are shown in the game screen;
6 - Run it in full screen mode to avoid problems;

For latency reasons, solve this challenge using the Wildcard box, inside the VPN (when you get access):
ssh sgle@10.133.70.3
Ahkae3beePhu9ooThei7

Id: sgle
Total solves: 0
Score: 500
Categories: PPC
```

## Observations and other points

- The code `run.py` used non-blocking reading.

- Every 0.02s it gets screen from the server.

- The screen is almost complete.

- Also each screen contains player's coordinates and time. `run.py` catches them by regular expression `r'(\[\d+:\d+\]).*(\[\d+.\d+\])'`.

- The enemy particles fly the same way always.

- The time may be a bit different between runs, the difference seems to be not more than 0.1s.

- So `run.py` tries to repeat good player's behaviour, then send random actions and remember the best behaviour comparing only time. So screen contents are not investigated really. The behaviour is saved into `best` file. (See more about [hill climbing algorithm](https://en.wikipedia.org/wiki/Hill_climbing).)

- `best` file contains a behaviour that got 136.25s far. (137s was the target.)

- Sometimes replaying misses the tick and everything goes wrong then. So small lags affect performance heavily.

- Wildcard box worked much faster.

- The VM for the game server was enlarged after complaint that the game has become too slow. The problem disappeared. (The organizers were very responsive.)

- `print_out.py` can print collected output from `out` file. It uses separate pexpect's ANSI object for each screen, so some screens are not correct. `out` file is not provided here.

- The output of game to terminal is disabled in the script. Also the last 1-15 moves are removed on each run. The size of tail to be revomed is randomly chosen in 1-15. It gave quite stable progress.

- For the last hour, the size of tail to be removed was changed to 1-4 and then 1-8, because we did not see progress.

- While our best result is 136.25s and we had more than hour to replay and improve this behaviour, we did not get the flag.

- Maybe in the end, we had to investigate and improve the behaviour manually.

- Also we might remove some moves from the end manually and "restart" with this beginning.

- Other approach would to be use moves that make bigger padding and remember several branches of behaviour, so we would not fail on minor lags.

- Nevertheless the task was pretty fun and interesting. Huge thanks to the orgs!

- The sources of the game/server should be [here](https://github.com/pauloklaus/sgle-game). (They were provided after the CTF.)
