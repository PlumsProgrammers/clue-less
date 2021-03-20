# API Routes

## Basic

---
### About
> GET /about

#### Returns
>200   
```JSON
"\"It's like ClueTM, just less!\"\n    A simplified version of the classic board game, developed for \n    EN.605.601 Foundations of Software Engineering \n    at Johns Hopkins University."
```

---
### Test Connection
> GET /test_connection

#### Returns
> 200
```JSON
"Connected Successfully"
```

---

## Games

---

### Games List
> GET /games

#### Returns
> 200
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

Body: 
```JSON
{
  "name": "Test Game"
}
```
Optionally, password can be used

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

---
### Start Game
