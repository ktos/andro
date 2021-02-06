// consts
const main = document.querySelector("main");
const listElement = document.getElementById("word-list");
const options = {
   valueNames: ["word", "translation", "id"],
   indexAsync: true,
   item: listElement.children[0].outerHTML
};

let speechAvailable;
let voice = null;
if (typeof speechSynthesis !== 'undefined') {
   speechAvailable = true;
   let voices = speechSynthesis.getVoices();

   // find the voice for pl-PL
   for (let i = 0; i < voices.length; i++) {
      if (voices[i].lang == 'pl-PL') {
         voice = voices[i];
         break;
      }
   }

   if (voice === null)
      speechAvailable = false;
} else {
   speechAvailable = false;
}

// language constants
const searchPlaceholder = { pl: 'Szukaj...', en: 'Search...' };
const header = {
   pl: 'Słownik Andro-Polski <a href="#en" title="Change language to English">[EN]</a>',
   en: 'Andro-English Dictionary <a href="#pl" title="Zmień język na polski">[PL]</a>'
}

const pageTitle = { pl: 'Andro — Słownik', en: 'Andro — Dictionary' }
const notesTitle = { pl: 'Uwagi:', en: 'Notes:' }
const examplesTitle = { pl: 'Przykłady użycia:', en: 'Examples:' }

const scTitlesPL = { pl: 'W formie liczby mnogiej', en: 'Plural form' }
const scTitlesFEM = { pl: 'W formie rodzaju żeńskiego', en: 'Female grammatical gender form' }
const scTitlesFEMOnly = { pl: 'To słowo występuje tylko w rodzaju żeńskim', en: 'This word is only in the female grammatical gender' }
const scTitlesPST = { pl: 'W formie czasu przeszłego', en: 'Past tense form' }
const scTitlesCOMP = { pl: 'W stopniu wyższym', en: 'Comparative form' }
const scTitlesSUPL = { pl: 'W stopniu najwyższym', en: 'Superlative form' }

// current language and current wordList
let currentLang = 'pl';
let wordList;

// load language if there is # in URL
if (window.location.hash != '') {
   currentLang = window.location.hash.substring(1);
   updateDescriptions();

   if (currentLang == 'pl')
      wordList = new List("wrapper", options, words_pl);
   else if (currentLang == 'en')
      wordList = new List("wrapper", options, words_en);

   selectWord(0);
} else {
   wordList = new List("wrapper", options, words_pl);
}

// select first word
listElement.children[0].remove();
selectWord(0);

document.querySelector("h1 a").addEventListener("click", e => changeLang(e));

listElement.addEventListener("click", e => {
   if (e.target.tagName == "UL") return;

   let id = "";
   if (e.target.tagName == "LI")
      id = e.target.querySelector(".id").innerHTML;
   else id = e.target.parentElement.querySelector(".id").innerHTML;
   selectWord(id);
});

function updateDescriptions() {
   document.querySelector("input.search").placeholder = searchPlaceholder[currentLang];
   document.querySelector("header h1").innerHTML = header[currentLang];
   document.querySelector("main h3.notes-title").innerHTML = notesTitle[currentLang];
   document.querySelector("main h3.examples-title").innerHTML = examplesTitle[currentLang];
   document.querySelector("h1 a").addEventListener("click", e => changeLang(e));
   document.title = pageTitle[currentLang];
}

function changeLang(e) {
   currentLang = e.target.hash.substring(1);

   updateDescriptions();

   listElement.innerHTML = '';
   if (currentLang == 'pl')
      wordList = new List("wrapper", options, words_pl);
   else if (currentLang == 'en')
      wordList = new List("wrapper", options, words_en);

   selectWord(0);
}

// go to another word's linked reference
function goToReference() {
   let result;

   if (currentLang == 'pl') {
      result = words_pl.find(x => x.word == this.innerHTML);
   } else {
      result = words_en.find(x => x.word == this.innerHTML);
   }

   if (result !== undefined)
      selectWord(result.id)

   return false;
}

function speak() {
   let ipa = this.dataset.ipa;
   ipa = ipa.replaceAll(".", "");
   ipa = ipa.replace("ˈ", "");
   ipa = ipa.replace("ɔ", "o");
   ipa = ipa.replace("ɛ", "e");
   ipa = ipa.replace("ʐ", "ż");
   ipa = ipa.replace("t͡ʂ", "cz");
   ipa = ipa.replace("x", "h");
   ipa = ipa.replace("w", "ł");
   ipa = ipa.replace("ʏ", "y");

   var utter = new SpeechSynthesisUtterance(ipa);
   utter.lang = "pl-PL";
   window.speechSynthesis.speak(utter);
}

// load word definition by id
function selectWord(id) {
   let word;

   if (currentLang == 'pl') {
      word = words_pl[id];
   } else {
      word = words_en[id];
   }

   main.querySelector(".word").innerHTML = word.word;
   main.querySelector(".type").innerHTML = word.type;
   main.querySelector(".ipa").innerHTML = `[${word.ipa}]`;

   main.querySelector(".translation").innerHTML = word.translation;

   if ('pl' in word) {
      main.querySelector(".pl").innerHTML = `<span class="sc" title="${scTitlesPL[currentLang]}">pl</span> ${word.pl} <span class="ipa">[${word.pl_speech}]</span>`;
   } else {
      main.querySelector(".pl").innerHTML = '';
   }

   if ('fem' in word) {
      if (word.fem != "FEM")
         main.querySelector(".fem").innerHTML = `<span class="sc" title="${scTitlesFEM[currentLang]}">fem</span> ${word.fem} <span class="ipa">[${word.fem_speech}]</span>`;
      else
         main.querySelector(".fem").innerHTML = `<span class="sc" title="${scTitlesFEMOnly[currentLang]}">fem</span>`;
   } else {
      main.querySelector(".fem").innerHTML = '';
   }

   if ('pst' in word) {
      main.querySelector(".pst").innerHTML = `<span class="sc" title="${scTitlesPST[currentLang]}">pst</span> ${word.pst} <span class="ipa">[${word.pst_speech}]</span>`;
   } else {
      main.querySelector(".pst").innerHTML = '';
   }

   if ('comp' in word) {
      main.querySelector(".comp").innerHTML = `<span class="sc" title="${scTitlesCOMP[currentLang]}">comp</span> ${word.comp} <span class="ipa">[${word.comp_speech}]</span>`;
   } else {
      main.querySelector(".comp").innerHTML = '';
   }

   if ('supl' in word) {
      main.querySelector(".supl").innerHTML = `<span class="sc" title="${scTitlesSUPL[currentLang]}">supl</span> ${word.supl} <span class="ipa">[${word.supl_speech}]</span>`;
   } else {
      main.querySelector(".supl").innerHTML = '';
   }

   // note
   const notes = word.notes;
   const noteElement = main.querySelector(".note");
   noteElement.innerHTML = "";

   for (let i = 0; i < notes.length; i++) {
      const note = word.notes[i];
      noteElement.innerHTML += `<p>${note}</p>`;
   }

   // Example
   const examples = word.examples;
   const exampleElement = main.querySelector(".examples");
   exampleElement.innerHTML = "";

   for (let i = 0; i < examples.length; i++) {
      const ex = examples[i].split(' -- ')
      exampleElement.innerHTML += `<h4>„${ex[0]}“ — ${ex[1]}</h4>`;
   }

   // hide if empty
   const isAdj = word.type == 'adj' && 'comp' in word ? '' : 'none';
   main.querySelector(".adj").style.display = isAdj;

   const isFem = word.type == 'n' && 'fem' in word ? '' : 'none';
   main.querySelector(".fem").style.display = isFem;

   const isPl = word.type == 'n' && 'pl' in word ? '' : 'none';
   main.querySelector(".pl").style.display = isPl;

   const isPst = word.type == 'v' && 'pst' in word ? '' : 'none';
   main.querySelector(".pst").style.display = isPst;

   const notesState = word.notes.length != 0 ? "" : "none";
   const examplesState = word.examples.length != 0 ? "" : "none";
   main.querySelector(".notes-title").style.display = notesState;
   main.querySelector(".examples-title").style.display = examplesState;

   // attach reference links
   const links = main.querySelectorAll("a.see");
   if (links != null) {
      for (let i = 0; i < links.length; i++) {
         links[i].addEventListener("click", goToReference);
      }
   }

   // attach speech
   if (speechAvailable) {
      const ipas = main.querySelectorAll(".ipa");
      if (ipas != null)
         for (let i = 0; i < ipas.length; i++)
            ipas[i].innerHTML += `<i class="ti ti-volume" data-ipa="${ipas[i].innerText.replace("[", "").replace("]", "")}"></i>`;

      const speech = main.querySelectorAll("i.ti-volume");
      if (speech != null)
         for (let i = 0; i < speech.length; i++)
            speech[i].addEventListener("click", speak);
   }
};
