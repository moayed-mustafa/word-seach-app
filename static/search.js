


                                    //###### Grab #####
                                    //###### DOM Elements #####
                                    //###### And #####
                                    //######Define #####
                                    //###### Variables  #####
                                    //#########################

let form = document.getElementById('form')
let list = document.getElementById('words')
let word = document.getElementById('wordInput')
let rand = document.getElementById('random')
let name_err = document.getElementById('name-err')
let userListBtn  = `<button class='btn btn-warning mb-2' onClick= addWordToUserList()>Add to list</button>`
let headerLi = document.createElement('li');
headerLi.classList.add('list-group-item')
let li = document.createElement('li');
li.classList.add('list-group-item')
let wordDataDiv = document.createElement('div')
wordDataDiv.classList.add('word-data-div')
let URL = "https://wordsapiv1.p.rapidapi.com/words/"
let HEADERS =  {
    "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
    "x-rapidapi-key": "82d62a047fmsh74091241e57a04fp1b7385jsn57e8b551a5c6"
}
currentUrl = window.location.href
guest_user =  currentUrl.slice(currentUrl.length-4,currentUrl.length )
console.log(guest_user)



                                        // #############
                                        //###### Build #####
                                       //###### Neccesary #####
                                        //###### Functions   #####
                                        //#########################

function addWordToUserList(e) {
    console.log('hello')
    console.log(this)
}
async function fetchWord(e) {
    e.preventDefault()

    // check word.value is not empty
    if (word.value == '') {
        handleWordNotEntered(word)
    }
    else {
        try {
            let res = await axios({
                method: 'GET',
                url: `${URL}${word.value}`,
                headers:HEADERS,
            })
            // request is successful
            if (res.status === 200) { showWords(res) }
            // request is a failure
        } catch (e) {
            console.log(e)
            if (e.response.status == 404) {
                setTimeout(function () {
                    let alert = `<div class="alert alert-danger mt-2" role="alert">
                                ${e.response.data.message}
                                </div>`
                    list.innerHTML = alert
                    }, 100)
                    // clear the alert after 2 sec
                    setTimeout(function () {
                        list.innerHTML = ''
                    }, 3000)
            }
        }
    }
}
// ############################################################################################################
async function fetchRandomWord() {
    console.log('fetching random word...')
    // for some reason axios won't perform a random word request!!
    var settings = {
        "async": true,
        "crossDomain": true,

        "url": "https://wordsapiv1.p.rapidapi.com/words/?random=true",
        "method": "GET",
        "headers": {
            "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
            "x-rapidapi-key": "82d62a047fmsh74091241e57a04fp1b7385jsn57e8b551a5c6"
        }
    }
    $.ajax(settings).done(function (response) {
        showRandomWord(response);
    });
}
// ############################################################################################################

// handle word alert
function handleWordNotEntered(){
    setTimeout(function () {
        let alert = `<div class="alert alert-warning mt-2" role="alert">
                    Must enter a word!
                    </div>`
        name_err.innerHTML = alert
    }, 100)
    // clear the alert after 2 sec
    setTimeout(function () {
        name_err.innerHTML = ''
    }, 2000)
}
// ############################################################################################################

// show words on the screen
function showWords(res) {
    console.log(res.data)
    // create an li and give it an id

    clearUL()

    // let id = 1;
    let span =  `
    <span>
    <h1> ${res.data.word}</h1>
    <h3>IPA: ${res.data.pronunciation.all}</h3>
    </span>
    `
    headerLi.innerHTML = span

    headerLi.classList.add('border-bottom', 'm2')
    list.appendChild(headerLi)

    extractData(res.data.results)
}
// ############################################################################################################
function showRandomWord(res) {
    console.log(res)
    clearUL()

    // let id = 1;

    let span = `
    <span>
    <h1> ${res.word}</h1>

    </span>
    `
    headerLi.innerHTML = span
    // the api has descrepency in showing the IPA
    // add pronunciation
    if (res.pronunciation && res.pronunciation.all) {
         let IPA = `

        <span >
        <h4> IPA: ${res.pronunciation.all}</h4>
        </span>

    `
        headerLi.innerHTML += IPA
    }

    // No IPA
    else {
        let noIPA = `

        <span class='d-inline'>
        <h4> IPA not available!</h4>
        </span>

    `
    headerLi.innerHTML += noIPA
    }
    list.appendChild(headerLi)
    if (res.results) {
        extractData(res.results)
    }
    else {
        // alert that data is not availabe due to api error
        let noDataLi = document.createElement('li')
        setTimeout(function () {
            let alert = `

            <div class="alert alert-danger mt-2" role="alert">
                        API Error, Data not fully Available
                        </div>
            `
            noDataLi.innerHTML = alert
            list.append(noDataLi)
            }, 100)
            // clear the alert after 2 sec
            setTimeout(function () {
                noDataLi.innerHTML = ''
            }, 5000)
    }

}

// ############################################################################################################
function extractData(results) {
    console.log('activated!')
    let id =1
    results.forEach(result => {
        // craete an li here and add id to it
    my_li = document.createElement('li')
    my_li.setAttribute('id', id)
    id++
        // part of speech and defenition:
    pos = `<p><b>Part of Speech:</b>${result.partOfSpeech}</p>`
    my_li.innerHTML= pos
    def = `<p><b>Definition:</b>${result.definition}</p>`
    my_li.innerHTML+= def
        // add example:
    if (result.examples) {
        example = `
            <p>
            <b> Example:</b> ${result.examples[0]}
            </p>
            `
        my_li.innerHTML+= example
        }

         // add synonyms
    if (result.synonyms) {
        syns = ''
        result.synonyms.forEach(syn => {
            syns += `${syn}, `
        })
        // remove the last comma from syns
        syns = syns.slice(0, syns.length-2)
        synTag = `
            <p>
            Synonyms :<b> ${syns}</b>.
            </p>
                `
            my_li.innerHTML += synTag
    }
            // add button
            if (guest_user == 'user') { my_li.innerHTML += userListBtn }
            // add border
            my_li.classList.add('border', 'm2', 'p-2')

    // append to the list:
    list.appendChild(my_li)

    })

}

// ############################################################################################################

// ############################################################################################################

function clearUL() {
    // clear up the list
    list.innerHTML = ''
}
// ############################################################################################################

                                              // ##########################
                                                //###### Hook  #####
                                                //###### Functions #####
                                                //###### To #####
                                                //######  Events #####
                                             // ##########################



// hook things up
form.addEventListener('submit', fetchWord)
rand.addEventListener('click', fetchRandomWord)
