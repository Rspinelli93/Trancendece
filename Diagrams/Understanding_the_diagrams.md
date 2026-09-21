# UNDERSTANDING THE DIAGRAMS

### Meaning of the arrows

**Solid arrow**: a request or information is being sent.
**Arrow in both directions**: both sides send information.
**Dotted arrow**: infrastructure starts, monitors, or maintains a service.

## IN A NUTSHELL

	- The frontend displays the application and sends user actions.

	- The backend handles accounts, normal API requests, and permanent database data.

	- The multiplayer engine controls the live match and is the authority for lives, scores, time, and winners.

	- The C runner safely compiles and tests code but does not make game decisions.

	- The LLM generates exercises offline, while the infrastructure connects and runs all services.

	- HTTP is used for normal requests, and WebSockets are used for live match updates.

## General system overview (this is diagram 00)

Nginx is the entrance of the app, it decides where each request goes:

1. Frontend req goes to react (What you see, lets say the UI)
2. API req goes to the backend with Express (this is a library of js. For example
we get the info of this particular player to render in the page, name, avatar, etc.)
3. Web socket connections for multiplayer game

## Person 1 - UI

Bref.. **Builds the UI**

What does this means? Everything the user interacts with
What do we need?

**Main pages:**

	/login

	/register

	/dashboard

	/game/:matchId

### The frontend has <ins>two ways</ins> to communicate with the system.

**1 - HTTP requests**

	Log in.

	Register.

	Load the leaderboard.

	Load the player profile.

	Delete an account.

	Run code against public tests.

> Frontend → HTTP API → Backend

**2 - WebSocket connection**

We all know what a WebSocket is, but lets clarify it a bit: a connection that stays open. It allows the server to send updates immediately. Certainly we want this for the Game!

	The player joins the matchmaking queue.

	An opponent is found.

	The match starts.

	A player loses a life.

	The opponent completes a challenge.

	The match ends.

> Frontend ↔ WebSocket server

## Person 3 — Backend, authentication, API and database

Person 3 controls data. This includes:

	Registration and login.

	OAuth authentication.

	User profiles.

	Leaderboard information.

	Exercise information.

	Match history.

	Account deletion.

	Database transactions.


The backend is divided into layers:

	HTTP controller
		↓
	Application service
		↓
	Prisma repository
		↓
	PostgreSQL

What those layers mean

    HTTP controller: receives the request.

    Application service: decides what operation must happen.

    Prisma repository: reads or writes database records.

    PostgreSQL: stores the permanent data.

*Example:*

	GET /api/v1/leaderboard
			↓
	Leaderboard service
			↓
	Prisma reads users and scores
			↓
	Backend returns the ranking

> Person 3 owns the database rules. Other people should not write random SQL directly.

## Person 2 — Multiplayer and game engine

Person 2 controls everything that happens during a live match.

<ins>**Main responsibilities:**</ins>

	Matchmaking queue.

	Creating a match.

	Selecting exercises.

	Starting the timer.

	Tracking the current challenge.

	Tracking three lives.

	Checking whether a submission is allowed.

	Calculating points.

	Deciding the winner.

	Sending match updates to both players.

> All the needed info must to be stored in the db for the Person 1 to retieve and render live in the browser

### The match manager is the official authority during the game.

For example, the frontend may show that a player has three lives, but Person 2’s game engine stores the official value.

### Communication with Person 3

The game engine needs the backend/database to:

	Find validated exercises.

	Create the match record.

	Save player submissions.

	Save the final result.

	Update total points and wins.


> Person 2 uses interfaces or transaction methods defined with Person 3. Person 2 should not independently change the database structure.

## Person 4 — C runner and challenge validation

Person 4 builds the protected environment that compiles and runs C code.

The runner receives:

	The player’s C code.

	The challenge tests.

	Compilation and execution limits.


### The process is:

	Receive code
		↓
	Create isolated environment
		↓
	Compile with gcc
		↓
	Run the tests
		↓
	Return a verdict

#### <ins>Possible verdicts include:</ins>

	COMPILE_ERROR

	WRONG_ANSWER

	TIME_LIMIT

	RUNTIME_ERROR

	ACCEPTED

> The runner does not decide points, lives, or the winner. It only reports what happened when the code was tested.

### Two runner usages

**<ins>1 - Practice execution:</ins>**

>Frontend → Backend → Runner

This uses public tests so the player can test their code.

**<ins>2 - Official match submission:</ins>**

> Frontend → Game engine → Runner

This uses hidden tests. The game engine then decides whether the player loses a life or passes the challenge.

## Person 5 — LLM and infrastructure

Person 5 has <ins>**two separate responsibilities.**</ins>

### 1 - Offline exercise generation

The local LLM creates possible exercises.

	Generation CLI
		↓
	Generator service
		↓
	Ollama local model
		↓
	C runner validates the exercise
		↓
	Approved exercise is stored

> There is no admin page so far in this first idea ...

Generation happens using a CLI command or backend script. It is not available to normal players.

#### <ins>The generator should:</ins>

	Ask the LLM for a structured exercise.

	Check the returned format.

	Send the solution and tests to the runner.

	Reject broken exercises.

	Store only approved exercises.


> The LLM is not involved during a live match. Matches use exercises that were already generated and validated.

### 2 - Infrastructure

Person 5 also configures:

	Docker Compose.

	Nginx.

	HTTPS.

	Environment variables.

	Service health checks.

	PostgreSQL container and storage.

	Ollama container.

	Runner container.

	Application startup.

> The dotted arrows mean Person 5 starts and monitors these services. They do not represent player information being sent.

---

# How we communicate with each other:

### The three main communication paths

	The player presses Find me a rival.

	Person 1 sends queue:join through the WebSocket.

	Person 2 adds the player to the matchmaking queue.

	An opponent is found.

	Person 2 asks Person 3 for validated exercises.

	Person 3 reads those exercises from PostgreSQL.

	Person 2 creates the match and sends match:started.

	Both players receive the first challenge.

	A player presses Run code.

	Person 1 sends a normal HTTP request for public testing.

	Person 3 sends the code to Person 4.

	Person 4 returns the public-test result.

	The player presses Send answer.

	Person 1 sends the official submission to Person 2.

	Person 2 sends it to Person 4 with hidden tests.

	Person 4 returns the official verdict.

	Person 2 updates the challenge, lives, score, and timer.

	Person 2 sends the new match state to both players.

	When the match finishes, Person 2 asks Person 3 to save the result.

