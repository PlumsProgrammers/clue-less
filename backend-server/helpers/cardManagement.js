exports.shuffle = (unshuffledDeck) => {
  let deck = [...unshuffledDeck]
  let m = deck.length, t, i;

  while (m) {
    i = Math.floor(Math.random() * m--);

    t = deck[m];
    deck[m] = deck[i];
    deck[i] = t;
  }

  return deck;
}
