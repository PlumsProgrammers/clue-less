const {locations} = require('./locations');
exports.suspects = [
  {
    name: 'Miss Scarlet',
    startingLocation: locations.find((location) => {
      return location.name === 'Hall-Lounge-Hallway';
    }),
    color: 'red',
  }, {
    name: 'Mr. Green',
    startingLocation: locations.find((location) => {
      return location.name === 'Ballroom-Conservatory-Hallway';
    }),
    color: 'green',
  }, {
    name: 'Colonel Mustard',
    startingLocation: locations.find((location) => {
      return location.name === 'Dining Room-Lounge-Hallway';
    }),
    color: 'yellow',
  }, {
    name: 'Professor Plum',
    startingLocation: locations.find((location) => {
      return location.name === 'Library-Study-Hallway';
    }),
    color: 'purple',
  }, {
    name: 'Mrs. Peacock',
    startingLocation: locations.find((location) => {
      return location.name === 'Conservatory-Library-Hallway';
    }),
    color: 'blue',
  }, {
    name: 'Dr. Orchid',
    startingLocation: locations.find((location) => {
      return location.name === 'Ballroom-Kitchen-Hallway';
    }),
    color: 'pink',
  },
];
