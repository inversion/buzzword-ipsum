//TODO 
//- maybe make a duplicate of MyBuzz for each paragraph, and remove items as we use them to prevent duplicates. Or - remove items and add them in again after a few words, to prevent the same word appearing really close to itself.
//find a more value-added stock photo

$(document).ready(function() {
    for (var p = 0; p < numberOfParagraphs; p++) {
        var numberOfSentences = Math.floor((Math.random() * 4 + 4));
        
        $('#test').append('<p>');
        for (var s = 0; s < numberOfSentences; s++) {    
            $('#test').append(pickRandom(sentenceMakingFunctions)() + " ");
        }
        $('#test').append('</p>');
    }
});

//code mk 2

//NB: verbs must make sense as -ing and -e, i.e. "calibrating/calibrate" is fine but not "growing/growe"
//could fix with a second array (painful) or making an array of pairs, i.e. {[growing, grow], virtualising, virtualise])
var verbs = new Array("virtualising", "synergising", "calibrating", /*"growing", "impacting",*/ "leveraging", /*"transforming",*/ "revolutionizing", /*"relaying",*/ "deep diving", "offshoring");

var nouns = new Array("cloud", "dot-bomb", "user experience", "milestones", "organic growth", "alignment", "ballpark figure", "synergy", "big data", "bandwidth", "brand", "core competency", "enterprise", "holistic", "low hanging fruit", "visibility", "diversity", "capability", "platform", "core assets", "best practice");

var adjectives = new Array("value-added", "mission critical", "immersive", "customer-focused");

var adverbs = new Array("virtually", "strategically", "reliably", "globally", "proactively", "iteratively", "ethically", "intelligently");


var sentenceMakingFunctions = [makeSentenceOne, makeSentenceTwo, makeSentenceThree];

//would come from user input
var numberOfParagraphs = 3;



//makeSentenceOne();
//$('#test').append(makeSentenceThree());

function makeSentenceOne() {
    return "We aim to " + pickRandom(adverbs) + " " + convertINGtoE(pickRandom(verbs)) + " our " + pickRandom(nouns) + " by " + pickRandom(adverbs) + " " + pickRandom(verbs) + " the " + pickRandom(adjectives) + " " + pickRandom(adjectives) + " " + pickRandom(nouns) + ".";
}

function makeSentenceTwo() {
    return "Our business " + convertINGtoE(pickRandom(verbs)) + "s our " + pickRandom(nouns) + " to " + pickRandom(adverbs) + " and " + pickRandom(adverbs) + " " + convertINGtoE(pickRandom(verbs)) + " our " + pickRandom(adjectives) + " " + pickRandom(nouns) + ".";
}

function makeSentenceThree() {
    return capitaliseFirstLetter(pickRandom(adverbs)) + " " + pickRandom(verbs) + " the " + pickRandom(adverbs) + " " + pickRandom(adjectives) + " " + pickRandom(nouns) + " is crucial to our " + pickRandom(adjectives) + " " + pickRandom(nouns) + ".";
}

function convertINGtoE(ing) {
    return ing.slice(0, ing.length - 3) + "e";
}

function pickRandom(arr) {
    return arr[Math.floor((Math.random() * arr.length))];
}

function capitaliseFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/*
var myBuzz = new Array("ballpark figure", "best-of-breed", "brick-and-mortar", "enterprise", "holistic", "novel", "mission critical", "new economy", "shift left", "value-added", "big data", "cloud", "clickthrough", "deep dive", "dot-bomb", "HTML5", "innovative", "PaaS", "SaaS", "AaaS", "real-time", "skeuomorphic", "virtualized", "synergy");

//would come from user input
var numberOfParagraphs = 3;

for (var p = 0; p < numberOfParagraphs; p++) {

    var numberOfSentences = Math.floor((Math.random() * 6 + 5));

    for (var s = 0; s < numberOfSentences; s++) {

        var numberOfWords = Math.floor((Math.random() * 3 + 5));

        var missionCriticalString = "";

        for (var i = 0; i < numberOfWords; i++) {
            missionCriticalString += deepDiveToEnterpriseBuzzword() + " ";
        }

        missionCriticalString = virtuallySentencify(missionCriticalString);

        $('#test').append(missionCriticalString);

    }

    $('#test').append("<br><br>");

}

function deepDiveToEnterpriseBuzzword() {
    return myBuzz[Math.floor((Math.random() * myBuzz.length))];
}

//remove last space, add full stop, and capitalise first letter.
function virtuallySentencify(string) {
    return string.charAt(0).toUpperCase() + string.slice(1, string.length - 1) + ". ";
}*/



