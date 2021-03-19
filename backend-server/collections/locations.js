exports.locations = [
  {
    name: 'Ballroom',
    suggestions: true,
    navigationOptions: [
      'Ballroom-Billiard Room-Hallway',
      'Ballroom-Conservatory-Hallway',
      'Ballroom-Kitchen-Hallway'
    ]
  }, {
    name: 'Ballroom-Billiard Room-Hallway',
    suggestions: false,
    navigationOptions: [
      'Ballroom',
      'Billiard Room',
    ]
  }, {
    name: 'Ballroom-Conservatory-Hallway',
    suggestions: false,
    navigationOptions: [
      'Ballroom',
      'Conservatory',
    ]
  }, {
    name: 'Ballroom-Kitchen-Hallway',
    suggestions: false,
    navigationOptions: [
      'Ballroom',
      'Kitchen',
    ]
  }, {
    name: 'Billiard Room',
    suggestions: true,
    navigationOptions: [
      'Billiard Room-Dining Room-Hallway',
      'Billiard Room-Hall-Hallway',
      'Billiard Room-Library-Hallway',
    ]
  }, {
    name: 'Billiard Room-Dining Room-Hallway',
    suggestions: false,
    navigationOptions: [
      'Billiard Room',
      'Dining Room'
    ]
  }, {
    name: 'Billiard Room-Hall-Hallway',
    suggestions: false,
    navigationOptions: [
      'Billiard Room',
      'Hall'
    ]
  }, {
    name: 'Billiard Room-Library-Hallway',
    suggestions: false,
    navigationOptions: [
      'Billiard Room',
      'Library'
    ]
  }, {
    name: 'Conservatory',
    suggestions: true,
    navigationOptions: [
      'Lounge',
      'Ballroom-Conservatory-Hallway',
      'Conservatory-Library-Hallway'
    ]
  }, {
    name: 'Conservatory-Library-Hallway',
    suggestions: false,
    navigationOptions: [
      'Conservatory',
      'Library'
    ]
  }, {
    name: 'Dining Room',
    suggestions: true,
    navigationOptions: [
      'Billiard Room-Dining Room-Hallway',
      'Dining Room-Kitchen-Hallway',
      'Dining Room-Lounge-Hallway'
    ]
  }, {
    name: 'Dining Room-Kitchen-Hallway',
    suggestions: false,
    navigationOptions: [
      'Dining Room',
      'Kitchen'
    ]
  }, {
    name: 'Dining Room-Lounge-Hallway',
    suggestions: false,
    navigationOptions: [
      'Dining Room',
      'Lounge'
    ]
  }, {
    name: 'Hall',
    suggestions: true,
    navigationOptions: [
      'Billiard Room-Hall-Hallway',
      'Hall-Lounge-Hallway',
      'Hall-Study-Hallway'
    ]
  }, {
    name: 'Hall-Lounge-Hallway',
    suggestions: false,
    navigationOptions: [
      'Hall',
      'Lounge'
    ]
  }, {
    name: 'Hall-Study',
    suggestions: false,
    navigationOptions: [
      'Hall',
      'Study'
    ]
  }, {
    name: 'Kitchen',
    suggestions: true,
    navigationOptions: [
      'Study',
      'Ballroom-Kitchen-Hallway',
      'Dining Room-Kitchen-Hallway'
    ]
  }, {
    name: 'Library',
    suggestions: true,
    navigationOptions: [
      'Billiard Room-Library-Hallway',
      'Conservatory-Library-Hallway',
      'Library-Study-Hallway'
    ]
  }, {
    name: 'Library-Study-Hallway',
    suggestions: false,
    navigationOptions: [
      'Library',
      'Study'
    ]
  }, {
    name: 'Lounge',
    suggestions: true,
    navigationOptions: [
      'Conservatory',
      'Dining Room-Lounge-Hallway',
      'Hall-Lounge-Hallway'
    ]
  }, {
    name: 'Study',
    suggestions: true,
    navigationOptions: [
      'Kitchen',
      'Hall-Study-Hallway',
      'Library-Study-Hallway'
    ]
  }
]