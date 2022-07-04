function compare_caseless(s1, s2) {
    return s1.toLowerCase().normalize("NFD") === s2.toLowerCase().normalize("NFD");
}

function description_to_gloss(desc, type, variant = "") {
    desc = desc.trim();

    let sc = desc.indexOf('(<span class="sc">');
    if (sc != -1)
        return desc.substring(sc + 18, desc.indexOf("</span>")).toUpperCase();

    let semi = desc.indexOf(";");
    if (semi != -1)
        desc = desc.substring(0, semi).trim()

    let comma = desc.indexOf(",");
    if (comma != -1)
        desc = desc.substring(0, comma).trim()

    let parentheses = desc.indexOf('(')
    if (parentheses != -1)
        desc = desc.substring(0, parentheses).trim()

    let to = desc.startsWith('to ');
    if (to) {
        desc = desc.substring(3)
        if (variant == 'pst')
            desc = desc + '-PST'
        else
            desc = desc + '.PRS'
    }

    if (type == 'adj')
        desc += '-ADJ'

    if (variant != 'pst' && variant != '') {
        if (variant == 'fem')
            variant = 'f'

        desc += "-" + variant.toUpperCase();
    }

    return desc.replaceAll(" ", ".")
}

function gloss_word(word) {
    results = []

    for (x of words_en) {
        if (compare_caseless(word, x['word']))
            if ('redirect' in x)
                results.push('[REDIRECT!]')
            else
                results.push(description_to_gloss(
                    x['translation'], x['type']))
        if ('pl' in x && compare_caseless(word, x['pl']))
            results.push(description_to_gloss(
                x['translation'], x['type'], 'pl'))
        if ('pst' in x && compare_caseless(word, x['pst']))
            results.push(description_to_gloss(
                x['translation'], x['type'], 'pst'))
        if ('fem' in x && x['fem'] != 'FEM' && compare_caseless(word, x['fem']))
            results.push(description_to_gloss(
                x['translation'], x['type'], 'fem'))
        if ('supl' in x && compare_caseless(word, x['supl']))
            results.push(description_to_gloss(
                x['translation'], x['type'], 'supl'))
        if ('comp' in x && compare_caseless(word, x['comp']))
            results.push(description_to_gloss(
                x['translation'], x['type'], 'comp'))

    }

    if (results.length == 1)
        return results[0]
    else if (results.length == 0) {
        return word + "[!]";
    }
    else
        return results.join("/")
}

function phonemize_word(word) {
    for (let x of words_en) {
        if (compare_caseless(word, x['word']))
            return x['ipa'];

        if ('pl' in x && compare_caseless(word, x['pl']))
            return x['pl_speech'];

        if ('pst' in x && compare_caseless(word, x['pst']))
            return x['pst_speech'];

        if ('fem' in x && x['fem'] != 'FEM' && compare_caseless(word, x['fem']))
            return x['fem_speech'];

        if ('supl' in x && compare_caseless(word, x['supl']))
            return x['supl_speech'];

        if ('comp' in x && compare_caseless(word, x['comp']))
            return x['comp_speech'];
    }

    // if everything failed, try transliteration
    vowels = { 'yi': 'ʏ', 'a': 'a', 'e': 'ɛ', 'o': 'ɔ', 'u': 'u' }
    consonants = {
        'ch': 'ʈ͡ʂ', 'b': 'b', 'p': 'p', 't': 't', 'd': 'd', 'k': 'k', 'g': 'g', 'm': 'm', 'n': 'n',
        'f': 'f', 'v': 'v', 's': 's', 'z': 'z', 'j': 'ʐ', 'h': 'x', 'y': 'j', 'l': 'l', 'w': 'w', 'r': 'r'
    }

    for (let i in vowels)
        word = word.replaceAll(i, vowels[i]);

    for (let i in consonants)
        word = word.replaceAll(i, consonants[i]);

    // returns "[!]" as a marker something went wrong
    return word + "[!]";
}

function prepare(text) {
    chars = [',', '.', ';', '?', '!'];

    for (let i of chars)
        text = text.replaceAll(i, '');

    text = text.toLowerCase().trim()

    return text.split(" ");
}

function removeLeadingAccent(word) {
    if (word[0] == "ˈ")
        return word.substring(1);
    else
        return word;
}

function phonemize(text) {
    text = prepare(text).map(x => removeLeadingAccent(phonemize_word(x))).join(" ");
    return "/" + text + "/";
}

function gloss(text) {
    return prepare(text).map(x => gloss_word(x));
}

document.getElementById("andro").onkeyup = function (e) {
    const ipa = document.getElementById("ipa");
    const zaha = document.querySelector("p.zaha");
    const chiwo = document.querySelector("p.chiwo");

    const markdown = document.getElementById("markdown");

    const gloss2 = document.getElementById("gloss_original");
    const gloss3 = document.getElementById("gloss_gloss");

    const text = document.getElementById("andro").value;

    ipa.innerText = phonemize(text);
    zaha.innerText = toZaha(text);
    chiwo.innerText = toChiwo(text);

    gloss2.innerHTML = prepare(text).map(x => `<th>${x}</th>`).join("");
    gloss3.innerHTML = prepare(text).map(x => `<td>${gloss_word(x)}</td>`).join("");

    markdown.innerText = `**${text}**\n\n${phonemize(text)}\n\n${prepare(text).join("|")}\n${prepare(text).map(x => "---").join("|")}\n${prepare(text).map(x => gloss_word(x)).join("|")}\n\n*TRANSLATION*`;
}