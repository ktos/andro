function speak() {
    ipa = this.dataset.ipa;

    ipa = ipa.replaceAll(".", "");
    ipa = ipa.replaceAll("ˈ", "");
    ipa = ipa.replaceAll("ɔ", "o");
    ipa = ipa.replaceAll("ɛ", "e");
    ipa = ipa.replaceAll("ʐ", "ż");
    ipa = ipa.replaceAll("t͡ʂ", "cz");
    ipa = ipa.replaceAll("x", "h");
    ipa = ipa.replaceAll("w", "ł");
    ipa = ipa.replaceAll("ʏ", "y");

    var utter = new SpeechSynthesisUtterance(ipa);
    utter.lang = "pl-PL";
    window.speechSynthesis.speak(utter);
}

function toZaha(word) {
    return word.toLowerCase().normalize("NFD").replaceAll("ch", "c").replaceAll("yi", "q");
}

function toChiwo(word) {
    return word.toLowerCase().normalize("NFD").replaceAll("ch", "c").replaceAll("yi", "y");
}