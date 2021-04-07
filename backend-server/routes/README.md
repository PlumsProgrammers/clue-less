# API Routes

_If required params are not provided, a response of 400 with a json message stating required params will be returned_

## Basic

---
### About
> GET /about

#### Returns
```JSON
"\"It's like ClueTM, just less!\"\n    A simplified version of the classic board game, developed for \n    EN.605.601 Foundations of Software Engineering \n    at Johns Hopkins University."
```

---
### Test Connection
> GET /test_connection

#### Returns
```JSON
"Connected Successfully"
```

---

## Games

---

### Games List
> GET /games

#### Returns
```JSON
[
  {
    "id": 1,
    "name": "Test Game",
    "status": "waiting",
    "players": [],
    "solution": {},
    "turn": {},
    "winner": null
  },
  {
    "id": 2,
    "name": "Another Test Game",
    "status": "waiting",
    "players": [],
    "solution": {},
    "turn": {},
    "winner": null
  }
]
```

---
### New Game
> POST /game

Creates a new game, the name doesn't need to be unique, but it can help users to find the correct game.

Required Params - `name`   
Optional Params - `password`

Body: 
```JSON
{
  "name": "Test Game"
}
```

#### Returns
```JSON
{
    "id": 1,
    "name": "Test Game",
    "status": "waiting",
    "players": [],
    "solution": {},
    "turn": {},
    "winner": null
}
```

---
### Join Game
> POST /game/join

Joins a waiting game, username must be unique with respect to the game

Required Params - `username` `gameId`

Body:
```JSON
{
  "username": "TestyMcTester",
  "gameId": 1
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`400`
```JSON
"Lobby is full."
```

`400`
```JSON
"Game has already started."
```

`400`
```JSON
"Username already in game."
```

```JSON
{
  "id": 1,
  "name": "Test Game",
  "status": "waiting",
  "players": [
    {
      "username": "TestyMcTester",
      "suspect": "",
      "location": "",
      "failed": false
    }
  ],
  "solution": {},
  "turn": {},
  "winner": null
}
```


---
### Start Game
> PUT /game/start

Starts the game:
- Players without suspects chosen will be randomly assigned one.
- Players are moved to their starting position based on suspect.
- Solution is selected.
- Remaining cards are dealt to the players.
- Turn Order is randomly assigned
- Turn starts up with the first player and allows them to move.

Required Params - `gameId`

Body:
```JSON
{
  "gameId": 1
}
```

#### Returns
`400`
```JSON
"Game not found."
```

`400`
```JSON
"Not enough players."
```

`400`
```JSON
"Game already started"
```

We do plan to provide less information in the future, this is to help with testing for now.

`201`
```JSON
{
    "id": 1,
    "name": "Test Game",
    "status": "playing",
    "players": [
        {
            "username": "TestyMcTester",
            "suspect": "Mrs. White",
            "location": {
                "name": "Ballroom-Kitchen-Hallway",
                "suggestionsAllowed": false,
                "possibleMovements": [
                    "Ballroom",
                    "Kitchen"
                ]
            },
            "failed": false
        },
        {
            "username": "TestyMcTester-second",
            "suspect": "Miss Scarlet",
            "location": {
                "name": "Hall-Lounge-Hallway",
                "suggestionsAllowed": false,
                "possibleMovements": [
                    "Hall",
                    "Lounge"
                ]
            },
            "failed": false
        },
        {
            "username": "TestyMcTester-third",
            "suspect": "Professor Plum",
            "location": {
                "name": "Library-Study-Hallway",
                "suggestionsAllowed": false,
                "possibleMovements": [
                    "Library",
                    "Study"
                ]
            },
            "failed": false
        }
    ],
    "solution": {
        "suspect": "Miss Scarlet",
        "weapon": "Candlestick",
        "room": "Hall"
    },
    "turn": {
        "turnOrder": [
            {
                "username": "TestyMcTester-second",
                "suspect": "Miss Scarlet",
                "location": {
                    "name": "Hall-Lounge-Hallway",
                    "suggestionsAllowed": false,
                    "possibleMovements": [
                        "Hall",
                        "Lounge"
                    ]
                },
                "failed": false
            },
            {
                "username": "TestyMcTester",
                "suspect": "Mrs. White",
                "location": {
                    "name": "Ballroom-Kitchen-Hallway",
                    "suggestionsAllowed": false,
                    "possibleMovements": [
                        "Ballroom",
                        "Kitchen"
                    ]
                },
                "failed": false
            },
            {
                "username": "TestyMcTester-third",
                "suspect": "Professor Plum",
                "location": {
                    "name": "Library-Study-Hallway",
                    "suggestionsAllowed": false,
                    "possibleMovements": [
                        "Library",
                        "Study"
                    ]
                },
                "failed": false
            }
        ],
        "currentPlayer": {
            "username": "TestyMcTester-second",
            "suspect": "Miss Scarlet",
            "location": {
                "name": "Hall-Lounge-Hallway",
                "suggestionsAllowed": false,
                "possibleMovements": [
                    "Hall",
                    "Lounge"
                ]
            },
            "failed": false
        },
        "phase": "movement"
    },
    "winner": null
}
```

---

## Players

---

### Select Suspect
> PUT /players/selectSuspect

Sets player's suspect, can only be used before the game is started.

Required Params - `gameId` `username` `suspect`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester",
  "suspect": "Mr. Green"
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`400`
```JSON
"Game has already started."
```

`400`
```JSON
"Not a valid suspect."
```

`400`
```JSON
"Suspect already taken."
```

`400`
```JSON
"Player not found."
```

```JSON
{
  "username": "TestyMcTester",
  "uuid": "71caf8ae-5200-4522-a2d8-8727a19978eb",
  "suspect": "Mr. Green",
  "location": "",
  "failed": false
}
```

---

## Gameplay

---

### Move
> PUT /gameplay/move

Moves the player to the location, if allowed. 

Required Params - `gameId` `username` `location`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester",
  "location": "Hall"
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`400`
```JSON
"Game is not in progress."
```

`400`
```JSON
"Not your turn."
```

`400`
```JSON
"Already moved or made a suggestion."
```

`400`
```JSON
"You can not move there. Possible movements are: []"
```

```JSON
{
  "username": "TestyMcTester",
  "uuid": "71caf8ae-5200-4522-a2d8-8727a19978eb",
  "suspect": "Mr. Green",
  "location": "Hall",
  "failed": false
}
```

---

### End Turn
> PUT /gameplay/end_turn

Ends the player's turn.

Required Params - `gameId` `username`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester"
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`400`
```JSON
"Game is not in progress."
```

`400`
```JSON
"Not your turn."
```

`200`
```JSON
"Turn has ended."
```

---


### Suggestion
> PUT /gameplay/suggestion

Player makes a suggestion.

Required Params - `gameId` `username` `suggestion`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester",
  "suggestion": {
    "suspect": "Colonel Mustard",
    "weapon": "Candlestick",
    "room": "Ballroom"
  }
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`400`
```JSON
"Game is not in progress."
```

`400`
```JSON
"Not your turn."
```

`400`
```JSON
"Not a valid location."
```

`400`
```JSON
"Not a valid suspect."
```

`400`
```JSON
"Not a valid weapon."
```

`400`
```JSON
"Must suggest the room you are in."
```

`400`
```JSON
"Already made a suggestion."
```

`200`
```JSON
"Suggestion Accepted"
```

---


### Suggestion Response
> PUT /gameplay/suggestion_response

Responds to the suggestion.

Required Params - `gameId` `username`
Optional Params - `card`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester"
}
```

```JSON
{
  "gameId": 1,
  "username": "TestyMcTester",
  "card": "Candlestick"
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`400`
```JSON
"Game is not in progress."
```

`400`
```JSON
"Not your turn to respond."
```

`400`
```JSON
"You must show a card, since you can disprove the suggestion."
```

`400`
```JSON
"You can't show a card you don't have."
```

`400`
```JSON
"That card doesn't disprove the suggestion."
```

`200`
```JSON
"Response Accepted"
```

---


### Accusation
> PUT /gameplay/accusation

The player makes an accusation, if allowed.

Required Params - `gameId` `username` `accusation`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester",
  "accusation": {
    "suspect": "Colonel Mustard",
    "weapon": "Candlestick",
    "room": "Ballroom"
  }
}
```

#### Returns
`400`
```JSON
"Game not found."
```

`400`
```JSON
"Game is not in progress."
```

`400`
```JSON
"Not your turn."
```

`200`
```JSON
"TestyMcTester has won!"
```

`200`
```JSON
"TestyMcTester made a bad guess and has failed"
```

`200`
```JSON
"Everyone has failed, the game ends with no winner."
```


## Messages

---

### Game
> PUT /messages/game

Sends a message to all players in the game.

Required Params - `gameId` `username` `message`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester",
  "message": "Hi Everyone"
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`200`
```JSON
"Sent"
```

---


### Private
> PUT /gameplay/accusation

Sends a message to the player specified only.

Required Params - `gameId` `username` `targetUsername` `message`

Body:
```JSON
{
  "gameId": 1,
  "username": "TestyMcTester",
  "targetUsername": "Donald",
  "message": "Hi Donald"
}
```

#### Returns

`400`
```JSON
"Game not found."
```

`200`
```JSON
"Sent"
```
