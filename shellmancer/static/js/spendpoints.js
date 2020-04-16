
const maxTotalPoints = 10;
const maxAttrRank = 7;
const minAttrRank = 1;
let startingAttrValue = 1;

let pointsRemaining = document.querySelector('#remaining-points');
pointsRemaining.innerHTML = maxTotalPoints;

let attr1 = {
  elem: document.querySelector('#attribute-one'),
  value: startingAttrValue
}
attr1.elem.innerHTML = attr1.value

let attr2 = {
  elem: document.querySelector('#attribute-two'),
  value: startingAttrValue
}
attr2.elem.innerHTML = attr2.value

let attr3 = {
  elem: document.querySelector('#attribute-three'),
  value: startingAttrValue
}
attr3.elem.innerHTML = attr3.value

let getWizardBar1 = document.querySelector('#wizardBar1');
let getWizardBar2 = document.querySelector('#wizardBar2');
let getWizardBar3 = document.querySelector('#wizardBar3');

function setHTMLToValue() {
  attr1.elem.innerHTML = attr1.value;
  attr2.elem.innerHTML = attr2.value;
  attr3.elem.innerHTML = attr3.value;
}

function checkTotalPoints() {
  return pointsRemaining.innerHTML <= 0;
}

function reducePoints(bar, attr) {
  if (attr.value > minAttrRank) {
    console.log(attr.value);

    let currentWidth = parseInt(bar.style.width.slice(0, -1));
    bar.style.width = currentWidth - 10 + "%"

    pointsRemaining.innerHTML++
    attr.value--

    setHTMLToValue()
  } else {
    return
  }
}

function increasePoints(bar, attr) {
  if (attr.value < maxAttrRank) {
    if (checkTotalPoints()) {
      return
    }
    console.log(attr.value);

    let currentWidth = parseInt(bar.style.width.slice(0, -1));
    bar.style.width = currentWidth + 10 + "%"

    pointsRemaining.innerHTML--
    attr.value++

    setHTMLToValue()
  } else {
    return
  }
}
