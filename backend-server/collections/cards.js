const {Card} = require("../models/card");
const {suspects} = require("./suspects");
const {weaponList} = require("./weapons");
const {locations} = require("./locations");

const suspectList = suspects.map(suspect => suspect.name)
const roomList = locations.filter(location => location.suggestionsAllowed).map(location => location.name)

exports.suspectCards = suspectList.map(suspect => new Card(suspect, 'suspect'))
exports.weaponCards = weaponList.map(weapon => new Card(weapon, 'weapon'))
exports.roomCards = roomList.map(room => new Card(room, 'room'))