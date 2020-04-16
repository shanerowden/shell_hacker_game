let bars = {
  one: document.getElementById('wizardBar1'),
  two: document.getElementById('wizardBar2'),
  three: document.getElementById('wizardBar3')
}

function randomPercentile() {
    return Math.floor(Math.random() * 75).toString() + "%";
}

bars.one.style.width = randomPercentile()
bars.two.style.width = randomPercentile()
bars.three.style.width = randomPercentile()
