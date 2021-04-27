const {Card} = require('../models/card');
const {suspects} = require('./suspects');
const {weaponList} = require('./weapons');
const {locations} = require('./locations');

const suspectList = suspects.map((suspect) => suspect.name);
const roomList = locations.filter((location) => {
  return location.suggestionsAllowed;
}).map((location) => location.name);

exports.suspectCards = suspectList.map((suspect) => {
  return new Card(suspect, 'suspect');
});
exports.weaponCards = weaponList.map((weapon) => {
  return new Card(weapon, 'weapon');
});
exports.roomCards = roomList.map((room) => {
  return new Card(room, 'room');
});
