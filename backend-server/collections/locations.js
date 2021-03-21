const {Location} = require('../models/location')

const locations = [
  new Location('Ballroom', true, [
    'Ballroom-Billiard Room-Hallway',
    'Ballroom-Conservatory-Hallway',
    'Ballroom-Kitchen-Hallway'
  ]),
  new Location('Ballroom-Billiard Room-Hallway', false, [
    'Ballroom',
    'Billiard Room',
  ]),
  new Location('Ballroom-Conservatory-Hallway', false, [
    'Ballroom',
    'Conservatory',
  ]),
  new Location('Ballroom-Kitchen-Hallway', false, [
    'Ballroom',
    'Kitchen',
  ]),
  new Location('Billiard Room', true, [
    'Billiard Room-Dining Room-Hallway',
    'Billiard Room-Hall-Hallway',
    'Billiard Room-Library-Hallway',
  ]),
  new Location('Billiard Room-Dining Room-Hallway', false, [
    'Billiard Room',
    'Dining Room'
  ]),
  new Location('Billiard Room-Hall-Hallway', false, [
    'Billiard Room',
    'Hall'
  ]),
  new Location('Billiard Room-Library-Hallway', false, [
    'Billiard Room',
    'Library'
  ]),
  new Location('Conservatory', true, [
    'Lounge',
    'Ballroom-Conservatory-Hallway',
    'Conservatory-Library-Hallway'
  ]),
  new Location('Conservatory-Library-Hallway', false, [
    'Conservatory',
    'Library'
  ]),
  new Location('Dining Room', true, [
    'Billiard Room-Dining Room-Hallway',
    'Dining Room-Kitchen-Hallway',
    'Dining Room-Lounge-Hallway'
  ]),
  new Location('Dining Room-Kitchen-Hallway', false, [
    'Dining Room',
    'Kitchen'
  ]),
  new Location('Dining Room-Lounge-Hallway', false, [
    'Dining Room',
    'Lounge'
  ]),
  new Location('Hall', true, [
    'Billiard Room-Hall-Hallway',
    'Hall-Lounge-Hallway',
    'Hall-Study-Hallway'
  ]),
  new Location('Hall-Lounge-Hallway', false, [
    'Hall',
    'Lounge'
  ]),
  new Location('Hall-Study', false, [
    'Hall',
    'Study'
  ]),
  new Location('Kitchen', true, [
    'Study',
    'Ballroom-Kitchen-Hallway',
    'Dining Room-Kitchen-Hallway'
  ]),
  new Location('Library', true, [
    'Billiard Room-Library-Hallway',
    'Conservatory-Library-Hallway',
    'Library-Study-Hallway'
  ]),
  new Location('Library-Study-Hallway', false, [
    'Library',
    'Study'
  ]),
  new Location('Lounge', true, [
    'Conservatory',
    'Dining Room-Lounge-Hallway',
    'Hall-Lounge-Hallway'
  ]),
  new Location('Study', true, [
    'Kitchen',
    'Hall-Study-Hallway',
    'Library-Study-Hallway'
  ])
]
exports.locations = locations
exports.getLocationByName = (name) => locations.find(location => location.name === name)
