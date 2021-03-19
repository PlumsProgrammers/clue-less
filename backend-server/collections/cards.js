const {Card} = require("../models/card");
const {suspects} = require("./suspects");
const {locations} = require("./locations");

const suspectList = suspects.map(suspect => suspect.name)
const roomList = locations.filter(location => location.suggestions).map(location => location.name)
const weaponList = ['Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench']

exports.suspectCards = suspectList.map(suspect => new Card(suspect, 'suspect'))
exports.weaponCards = weaponList.map(weapon => new Card(weapon, 'weapon'))
exports.roomCards = roomList.map(room => new Card(room, 'room'))
