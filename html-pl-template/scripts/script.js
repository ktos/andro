const main = document.querySelector("main");
const listElement = document.getElementById("word-list");
const paginationHeight = document.querySelector(".pagination").offsetHeight;
const maxItems = listElement.offsetHeight / (listElement.children[0].offsetHeight + 4);
const options = {
   valueNames: ["word", "translation", "id"],
   page: Math.floor(maxItems),
   pagination: true,
   indexAsync: true,
   pagination: {
      innerWindow: 1,
      left: 3,
      right: 3
   },
   item: listElement.children[0].outerHTML
};

listElement.children[0].remove();

const wordList = new List("wrapper", options, words);
selectWord(0);

document.getElementById("pagPrevious").addEventListener("click", () => {
   document.querySelector(".pagination .active").previousSibling.click();
});

document.getElementById("pagNext").addEventListener("click", () => {
   document.querySelector(".pagination .active").nextSibling.click();
});

listElement.addEventListener("click", e => {
   if (e.target.tagName == "UL") return;

   let id = "";
   if (e.target.tagName == "LI")
      id = e.target.querySelector(".id").innerHTML;
   else id = e.target.parentElement.querySelector(".id").innerHTML;
   selectWord(id);
});

function goToReference() {
   const result = words.find(x => x.word == this.innerHTML);
   if (result !== undefined)
      selectWord(result.id)

   return false;
}

function selectWord(id) {
   const word = words[id];

   main.querySelector(".word").innerHTML = word.word;
   main.querySelector(".type").innerHTML = word.type;
   main.querySelector(".ipa").innerHTML = `[${word.ipa}]`;
   main.querySelector(".translation").innerHTML = word.translation;

   if ('pl' in word) {
      main.querySelector(".pl").innerHTML = `<span class="sc" title="W formie liczby mnogiej">pl</span> ${word.pl} <span class="ipa">[${word.pl_speech}]</span>`;
   } else {
      main.querySelector(".pl").innerHTML = '';
   }

   if ('fem' in word) {
      if (word.fem != "FEM")
         main.querySelector(".fem").innerHTML = `<span class="sc" title="W formie rodzaju żeńskiego">fem</span> ${word.fem} <span class="ipa">[${word.fem_speech}]</span>`;
      else
         main.querySelector(".fem").innerHTML = '<span class="sc" title="To słowo występuje tylko w rodzaju żeńskim">fem</span>';
   } else {
      main.querySelector(".fem").innerHTML = '';
   }

   if ('pst' in word) {
      main.querySelector(".pst").innerHTML = `<span class="sc" title="W formie czasu przeszłego">pst</span> ${word.pst} <span class="ipa">[${word.pst_speech}]</span>`;
   } else {
      main.querySelector(".pst").innerHTML = '';
   }

   if ('comp' in word) {
      main.querySelector(".comp").innerHTML = `<span class="sc" title="W stopniu wyższym">comp</span> ${word.comp} <span class="ipa">[${word.comp_speech}]</span>`;
   } else {
      main.querySelector(".comp").innerHTML = '';
   }

   if ('supl' in word) {
      main.querySelector(".supl").innerHTML = `<span class="sc" title="W stopniu najwyższym">supl</span> ${word.supl} <span class="ipa">[${word.supl_speech}]</span>`;
   } else {
      main.querySelector(".supl").innerHTML = '';
   }

   // note
   const notes = words[id].notes;
   const noteElement = main.querySelector(".note");
   noteElement.innerHTML = "";

   for (let i = 0; i < notes.length; i++) {
      const note = words[id].notes[i];
      noteElement.innerHTML += `<p>${note}</p>`;
   }

   // Example
   const examples = words[id].examples;
   const exampleElement = main.querySelector(".examples");
   exampleElement.innerHTML = "";

   for (let i = 0; i < examples.length; i++) {
      const ex = examples[i].split('. ')
      exampleElement.innerHTML += `<h4>„${ex[0]}“. — ${ex[1]}</h4>`;
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
};
