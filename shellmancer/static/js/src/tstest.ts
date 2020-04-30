const maxTotalPoints = 10;
const maxAttrRank = 7;
const minAttrRank = 1;
let startingAttrValue = 1;
let personalityTab = document.querySelector('#personality-tab')!;
let pointsRemaining: Attribute;

function checkTotalPoints() {
    console.log(+pointsRemaining.value <= 0);
    
    return +pointsRemaining.value <= 0;
}

let getWizardBar1 = document.querySelector('#wizardBar1');
let getWizardBar2 = document.querySelector('#wizardBar2');
let getWizardBar3 = document.querySelector('#wizardBar3');


class CharacterStats{
    public loadout: string[] = [];

  constructor(private readonly attr1: number, 
              private readonly attr2: number, 
              private readonly attr3: number) {
    this.attr1 = attr1;
    this.attr2 = attr2;
    this.attr3 = attr3;
    this.loadout = [];
  }
}
let character: CharacterStats;

class Attribute {
    constructor(public readonly elem: HTMLSpanElement,
                public value: number = startingAttrValue) {
        if (!elem) {
          throw new Error('HTML element must exist');
        }
        this.elem = elem;
        this.value = value;
        this.setHTMLToValue();
    }

    protected setHTMLToValue() {
        this.elem.innerHTML = this.value.toString();
    }

    protected reducePoints(bar: HTMLElement) {
        if (this.value > minAttrRank) {
            
            const currentWidth = parseInt(bar.style.width.slice(0, -1));
            bar.style.width = currentWidth - 10 + "%";
            
            pointsRemaining.value++
            pointsRemaining.setHTMLToValue()
            this.value--
      
            this.setHTMLToValue()
            if (!checkTotalPoints()) {
                document.querySelector('#personality-tab')!.classList.add('disabled');
            } else {
                return
            }
        }
    }

    protected increasePoints(bar: HTMLElement) {
        if (this.value < maxAttrRank) {
            const currentWidth = parseInt(bar.style.width.slice(0, -1));
            bar.style.width = currentWidth + 10 + "%";

            pointsRemaining.value--
            pointsRemaining.setHTMLToValue()
            this.value++

            this.setHTMLToValue()
            if (checkTotalPoints()) {
                document.querySelector('#personality-tab')!.classList.add('disabled');
            } else {
                return
            }
        }
    }
}


pointsRemaining = new Attribute(document.querySelector('#remaining-points') as HTMLSpanElement, maxTotalPoints)

let meat = new Attribute(document.querySelector('#attribute-one') as HTMLSpanElement)
let leet = new Attribute(document.querySelector('#attribute-two') as HTMLSpanElement)
let street = new Attribute(document.querySelector('#attribute-three') as HTMLSpanElement)


// toggle div
let toggleSlots = 2;
let submitBtn = document.querySelector('#character-submit') as HTMLElement;

class ToggleDiv{
    private readonly toggleClass: string;
    private switch: boolean;

    constructor(public readonly elem: any, 
                private readonly toggableClass: string, 
                public readonly titleElem: any) {
    this.elem = elem;
    this.toggleClass = toggableClass;
    this.titleElem = titleElem;
    this.switch = false;
  }

  adjustPoints() {
    if (!this.switch && toggleSlots > 0) {
      this.switch = true;

      toggleSlots--;
      this.checkToggleSlots();
      return true;

    } else if (this.switch && toggleSlots <= 2) {
      this.switch = false;
      toggleSlots++;
      this.checkToggleSlots();
      return true;

    } else {
      return false;
    }
  }

  checkToggleSlots() {
    if (toggleSlots === 0) {
      submitBtn.style.display = "block";
      for (let option of toggleDivs) {
        if (option.switch) {
          character.loadout.push(option.titleElem.innerHTML);
        }
      }
    } else {
      submitBtn.style.display = "none";
      character.loadout = [];
    }
  }

  highlight() {
      if (this.adjustPoints()) {
        this.elem.classList.toggle(this.toggleClass);
        this.titleElem.classList.toggle("text-info");
      } else {
        alert("Cant do it");
      }
  }

  bindEventListener() {
      this.elem.addEventListener('click', () => this.highlight())
  }
}

const options = document.querySelectorAll('.options');
const optionTitles = document.querySelectorAll('.option-title');

let div;
let toggleDivs: any[] = [];
for (let idx in options) {
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
