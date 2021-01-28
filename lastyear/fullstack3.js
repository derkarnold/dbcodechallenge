// This IndexGenerator isn't quite working as intended
// maybe there are some keywords missing...
function IndexGenerator(seed) {
    this.index = seed
  }
  console.log('clear')
  // Generate a new pseudo-random index each time called
  IndexGenerator.prototype.next = function() {
    this.index = this.index * 16807 % 1000;
    return this.index;
  };
  
  // We also have to do some DOM manipulation.
  // Reveal the nth child of the div with id "thesecret"...
  function revealNibble(n) {
    var secretDiv = document.getElementById('thesecret')
    var child = secretDiv.children[n]
    child.style.display = 'inline'
  }
  
  // No need to change anything below
  function doStuff() {
    var generator1 = new IndexGenerator(20);
    var generator2 = new IndexGenerator(7);
  
    for (var i = 0; i < 5; i++) {
      revealNibble(generator1.next());
      revealNibble(generator2.next());
    }
  }
  
  
  doStuff();