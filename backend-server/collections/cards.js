const {Card} = require("../models/card");

const suspectList = [
  'Miss Scarlet', 'Mr. Green', 'Colonel Mustard', 'Professor Plum', 'Mrs. Peacock', 'Mrs. White'
]
const weaponList = [
  'Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench'
]
const roomList = [
  'Kitchen', 'Ballroom', 'Conservatory', 'Dining Room', 'Billiard Room', 'Library', 'Lounge', 'Hall', 'Study'
]

exports.suspectCards = suspectList.map(suspect => new Card(suspect, 'suspect'))
exports.weaponCards = weaponList.map(weapon => new Card(weapon, 'weapon'))
exports.roomCards = roomList.map(room => new Card(room, 'room'))
