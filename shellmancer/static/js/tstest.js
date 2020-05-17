"use strict";
var maxTotalPoints = 10;
var maxAttrRank = 7;
var minAttrRank = 1;
var startingAttrValue = 1;
var personalityTab = document.querySelector('#personality-tab');
var pointsRemaining;
function checkTotalPoints() {
    console.log(+pointsRemaining.value <= 0);
    return +pointsRemaining.value <= 0;
}
var getWizardBar1 = document.querySelector('#wizardBar1');
var getWizardBar2 = document.querySelector('#wizardBar2');
var getWizardBar3 = document.querySelector('#wizardBar3');
var CharacterStats = /** @class */ (function () {
    function CharacterStats(attr1, attr2, attr3) {
        this.attr1 = attr1;
        this.attr2 = attr2;
        this.attr3 = attr3;
        this.loadout = [];
        this.attr1 = attr1;
        this.attr2 = attr2;
        this.attr3 = attr3;
        this.loadout = [];
    }
    return CharacterStats;
}());
var character;
var Attribute = /** @class */ (function () {
    function Attribute(elem, value) {
        if (value === void 0) { value = startingAttrValue; }
        this.elem = elem;
        this.value = value;
        if (!elem) {
            throw new Error('HTML element must exist');
        }
        this.elem = elem;
        this.value = value;
        this.setHTMLToValue();
    }
    Attribute.prototype.setHTMLToValue = function () {
        this.elem.innerHTML = this.value.toString();
    };
    Attribute.prototype.reducePoints = function (bar) {
        if (this.value > minAttrRank) {
            var currentWidth = parseInt(bar.style.width.slice(0, -1));
            bar.style.width = currentWidth - 10 + "%";
            pointsRemaining.value++;
            pointsRemaining.setHTMLToValue();
            this.value--;
            this.setHTMLToValue();
            if (!checkTotalPoints()) {
                document.querySelector('#personality-tab').classList.add('disabled');
            }
            else {
                return;
            }
        }
    };
    Attribute.prototype.increasePoints = function (bar) {
        if (this.value < maxAttrRank) {
            var currentWidth = parseInt(bar.style.width.slice(0, -1));
            bar.style.width = currentWidth + 10 + "%";
            pointsRemaining.value--;
            pointsRemaining.setHTMLToValue();
            this.value++;
            this.setHTMLToValue();
            if (checkTotalPoints()) {
                document.querySelector('#personality-tab').classList.add('disabled');
            }
            else {
                return;
            }
        }
    };
    return Attribute;
}());
pointsRemaining = new Attribute(document.querySelector('#remaining-points'), maxTotalPoints);
var meat = new Attribute(document.querySelector('#attribute-one'));
var leet = new Attribute(document.querySelector('#attribute-two'));
var street = new Attribute(document.querySelector('#attribute-three'));
// toggle div
var toggleSlots = 2;
var submitBtn = document.querySelector('#character-submit');
var ToggleDiv = /** @class */ (function () {
    function ToggleDiv(elem, toggableClass, titleElem) {
        this.elem = elem;
        this.toggableClass = toggableClass;
        this.titleElem = titleElem;
        this.elem = elem;
        this.toggleClass = toggableClass;
        this.titleElem = titleElem;
        this.switch = false;
    }
    ToggleDiv.prototype.adjustPoints = function () {
        if (!this.switch && toggleSlots > 0) {
            this.switch = true;
            toggleSlots--;
            this.checkToggleSlots();
            return true;
        }
        else if (this.switch && toggleSlots <= 2) {
            this.switch = false;
            toggleSlots++;
            this.checkToggleSlots();
            return true;
        }
        else {
            return false;
        }
    };
    ToggleDiv.prototype.checkToggleSlots = function () {
        if (toggleSlots === 0) {
            submitBtn.style.display = "block";
            for (var _i = 0, toggleDivs_1 = toggleDivs; _i < toggleDivs_1.length; _i++) {
                var option = toggleDivs_1[_i];
                if (option.switch) {
                    character.loadout.push(option.titleElem.innerHTML);
                }
            }
        }
        else {
            submitBtn.style.display = "none";
            character.loadout = [];
        }
    };
    ToggleDiv.prototype.highlight = function () {
        if (this.adjustPoints()) {
            this.elem.classList.toggle(this.toggleClass);
            this.titleElem.classList.toggle("text-info");
        }
        else {
            alert("Cant do it");
        }
    };
    ToggleDiv.prototype.bindEventListener = function () {
        var _this = this;
        this.elem.addEventListener('click', function () { return _this.highlight(); });
    };
    return ToggleDiv;
}());
var options = document.querySelectorAll('.options');
var optionTitles = document.querySelectorAll('.option-title');
var div;
var toggleDivs = [];
for (var idx in options) {
    div = new ToggleDiv(options[idx], 'border-info', optionTitles[idx]);
    div.bindEventListener();
    toggleDivs.push(div);
}
// let personalityModalHandler = function() {
//   let click = 0;
//   console.log("Handler");
//   return function() {
//     if(click === 0) {
//       console.log(click);
//       alert('single click');
//       click++;
//     }
//   }
// }
// personalityTab.addEventListener('click', personalityModalHandler, false);
