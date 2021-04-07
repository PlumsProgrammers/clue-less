exports.Location = class {
  constructor(name, suggestions, possibleMovements) {
    this.name = name
    this.suggestionsAllowed = suggestions
    this.possibleMovements = possibleMovements
  }

  canMoveTo = (location) => this.possibleMovements.includes(location)
}