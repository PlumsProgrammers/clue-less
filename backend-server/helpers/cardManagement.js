/**
 * Takes an array and switches the elements around and returns a new array.
 * Doesn't modify the original array.
 *
 * @param {*[]} toShuffle Array to be shuffled
 * @return {*[]} New array with shuffled elements
 */
exports.shuffle = (toShuffle) => {
  const deck = [...toShuffle];
  let m = deck.length;
  let t;
  let i;

  while (m) {
    i = Math.floor(Math.random() * m--);

    t = deck[m];
    deck[m] = deck[i];
    deck[i] = t;
  }

  return deck;
};
