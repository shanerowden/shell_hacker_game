// let date = new Date;
// let currentHour = date.getCurrentHours;
//
// let bodyElem = document.querySelector('#test-div');
//
// let newDiv = document.createElement('div');
// newDiv.classList.add('center');
//
// let newH1 = document.createElement('h1');
//
// let createTxtMessage;
//
// if (currentHour >= 4 && currentHour < 10) {
//   createTxtMessage = "Good morning.";
// } else if (currentHour >= 11 && currentHour < 18) {
//   createTxtMessage = "Good afternoon";
// } else {
//   createTxtMessage = "Goodnight."
// }
//
// newH1.innerHTML = createTxtMessage.toLowerCase();
// newH1.setAttribute("class", "text-right");
//
// newH1.style.cssText = "font-size: 60px; font-family: Times New Roman;";
//
// bodyElem.append(newH1);


// Menu Toggle
// let menuBtn = document.querySelector('#menu-btn');
// let menu = document.querySelector('.menu');
// let menuStatus = false;
//
// function menuToggle() {
//   if (!menuStatus) {
//     console.log("!menuStatus");
//     menu.style.margin = "0px";
//     menuStatus = true;
//   } else if (menuStatus) {
//     console.log("menuStatus");
//     menu.style.margin = "-900px";
//     menuStatus = false;
//   }
// }
//
// menuBtn.onclick = menuToggle;
//
//
// // Form Shit
// let testForm = document.querySelector('#test-form');
// let testBtn = document.querySelector('#test-btn');
//
// function first(e, name) {
//   e.preventDefault();
//   testBtn.innerHTML = `My penis is ${name}.`;
// }
//
// function second() {
//   testBtn.style.backgroundColor = "red";
// }
//
// testBtn.addEventListener('click', function(e) {
//   first(e, "Daniel");
// });
//
// testBtn.addEventListener('click', function() {
//   testBtn.style.backgroundColor = 'blue';
// });

// const devices = [
//   document.querySelector('#device-one'),
//   document.querySelector('#device-two'),
//   document.querySelector('#device-three'),
//   document.querySelector('#device-four')
// ];


class ToggleDiv{
    constructor(elem, toggableClass, titleElem) {
      this.elem = elem;
      this.toggleClass = toggableClass;
      this.titleElem = titleElem;
    }

    highlight() {
        this.elem.classList.toggle(this.toggleClass);
        this.titleElem.classList.toggle("text-info");
    }

    bindEventListener() {
        this.elem.addEventListener('click', () => this.highlight())
    }
}

const devices = document.querySelectorAll('.devices');
const deviceTitles = document.querySelectorAll('.card-title');

let div;
let toggleDivs = [];
for (let idx in devices) {
  div = new ToggleDiv(devices[idx], 'border-info', deviceTitles[idx]);
  div.bindEventListener();
  toggleDivs.push(div);
}

// let div;
// for (let div of toggleDivs) {
//   toggleDivs.h
// }


// class ToggleDiv{
//   constructor(elem) {
//     this.elem = elem;
//     this.switch = false;
//   }
// }
//
// function highlightDiv(div) {
//   div.elem.classList.add('border-purple');
//   if (!div.switch) {
//     div.switch = true;
//   } else {
//     div.elem.classList.remove('border-purple');
//     div.switch = false;
//   }
// }
//
// let div;
// let toggleDivs = [];
// const devices = document.querySelectorAll('.devices');
// for(let dev of devices) {
//   div = new ToggleDiv(dev, 'border-purple');
//   toggleDivs.push(div);
// }
//
// for(let div of toggleDivs) {
//   div.elem.addEventListener("click", function(){
//     highlightDiv(div)
//   });
// }
