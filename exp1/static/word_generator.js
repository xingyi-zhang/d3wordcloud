distractor_list = []
var i = 0

do {
    word = randStr(getDistractorLength([3,10,6,2]),'short')
    if (! distractor_list.ncludes(word)) {
        distractor_list.push(word)
        i++
    }
} while (i<1000)

function randStr(length, shortOrTall) {
    if (shortOrTall == 'short') {
        return randShortStr(length);
    } else if (shortOrTall == 'tall') {
        return randTallStr(length);
    }
}

function randShortStr(length, charset){
    //defining parameters
    //var length = 5, charset="acenorsuvxzcnrcnraeouaeouaeou", blacklist = ["sex", "ear", "are"];
    var blacklist = ["sex", "ear", "are"]
    if (charset == undefined) {
        charset = "acenosuvxzcncnaeouaeouaeou";
    }
    //function
    var word = "";
    var cons = charset.replace(/[aeou]/g,"");
    var vowels = charset.replace(/[cnrsvxz]/g,"");
    var countVow =0, countCon=0;
    var rand;

    do{
        for (var i=0;i<length;i++){
            rand = Math.floor(Math.random()*charset.length);
            newChar = charset[rand];
            //is the new char a vowel
            if ( vowels.indexOf(newChar)>-1) {
                countVow++;
                //do we have 2 vowel already
                if (countVow>2){
                    rand = Math.floor(Math.random()*cons.length);
                    newChar = cons[rand]
                    countCon++;
                    countVow = 0;
                }
            //or is it a consonant
            }else if (cons.indexOf(newChar)>-1){
                countCon++;
                //do we have 2 consonant already
                if( countCon>2){
                    rand = Math.floor(Math.random()*vowels.length);
                    newChar = vowels[rand]
                    countVow++;
                    countCon = 0;
                }
            }
            //concat the new char
            word=word+newChar;
        }
    }
    while(word in blacklist);

    return word;
    //end function
}

function getLetter(charset){
    var rand = Math.floor(Math.random()*charset.length);
    return charset[rand];
}
function chooseOrder(){
    var rand = Math.floor(Math.random()*2);
    return rand;
}

function randTallStr(length, charset, asc, desc){
    if (charset == undefined) {
        charset = "aeou";
    }
    if (asc == undefined) {
        asc = "bdhkhd";
    }
    if (desc == undefined) {
        desc = "gpqygp";
    }

    var word = "";
    var setOne, setTwo, index=1, one = false;

    if (chooseOrder() == 0) {
        setOne = asc;
        setTwo = desc;
    } else {
        setOne = desc;
        setTwo = asc;
    }

    do {
        index = 1;
        one = false;
        word = getLetter(setOne);
        while(index < length-2){
            if(index%2 != 0){
                word = word + getLetter(charset);
            }else{
                if(one){
                    word = word +getLetter(setOne);
                }else{
                    word = word + getLetter(setTwo);
                }
                one = !one;
            }
            index++;
        }
        word = word + getLetter(setOne);
        word = word + getLetter(setTwo);
    } while (word in blacklist);

    return word;
}


//the config array is [min,max,mean,sd]
function getDistractorLength(length_config){
    var length = 0
    do {
        length = randomGaussian(length_config[2],length_config[3])
    } while (length <length_config[0] || length >length_config[1])
    return ~~length
  }

// SOURCE: http://www.ollysco.de/2012/04/gaussian-normal-functions-in-javascript.html
function randomGaussian(mean, standardDeviation) {
    if (randomGaussian.nextGaussian !== undefined) {
        var nextGaussian = randomGaussian.nextGaussian;
        delete randomGaussian.nextGaussian;
        return (nextGaussian * standardDeviation) + mean;
    } else {
        var v1, v2, s, multiplier;
        do {
            v1 = 2 * Math.random() - 1; // between -1 and 1
            v2 = 2 * Math.random() - 1; // between -1 and 1
            s = v1 * v1 + v2 * v2;
        } while (s >= 1 || s == 0);
        multiplier = Math.sqrt(-2 * Math.log(s) / s);
        randomGaussian.nextGaussian = v2 * multiplier;
        return (v1 * multiplier * standardDeviation) + mean;
    }
  };