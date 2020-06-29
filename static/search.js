


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
let userListBtn  = `<button class='btn btn-warning' onClick= addWordToUserList()>Add to list</button>`
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
guest_user =  currentUrl.slice(currentUrl.length-5,currentUrl.length )
console.log(guest_user)
// console.log()



                                        // #############
                                        //###### Build #####
                                       //###### Neccesary #####
                                        //###### Functions   #####
                                        //#########################

function addWordToUserList(e) {
    console.log('hello')
    console.log(e)
}
async function fetchWord(e) {
    e.preventDefault()

    // check word.value is not empty
    if (word.value == '') {
        handleWord(word)
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
function handleWord(){
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
    // create the UL
    // you can create the ul here and make li and append them everytime
    //
    // <ul class="list-group mt-2 " id='words'>

    //         </ul>
    clearUL()
    // make an add to list button


        // add string data
        let data = `
            <section >
            <span class='d-inline'>
            <h1> ${res.data.word}</h1>
            <h3>IPA: ${res.data.pronunciation.all}</h3>
            </span>
            </section>
        `
        // extract other data
        res.data.results.forEach(result => {
            // add part of speech:
            data += `Part of Speech: ${result.partOfSpeech}`
            // add defenition:
            data += `<section> <p>
            Definition: ${result.definition}
            </p>
            `
            // </section>
            // add example:
            if (result.examples) {
                // <section>
                data += `
                    <p>
            Example: ${result.examples[0]}
            </p>
            `
            // </section>
            }

             // add synonyms
             if (result.synonyms) {
                syns = ''
                result.synonyms.forEach(syn => {
                    syns += `${syn}, `
                })
                // remove the last comma from syns
                syns = syns.slice(0, syns.length-2)
                data += `
                <section class = 'border-bottom' > <p>
            Synonyms : ${syns}.
            </p>
            </section>
            </section>
                `
             }
            // in case some result array has no synonyms, make border after the last thing added
            // from the result!
            //  else {
            //      data += `
            //      <div class = 'border-bottom m2'></div>

            //      `
            //  }

            if (guest_user == '/user') {
                data += userListBtn


            }

            append(data)
            // hook the button here after it appears in the dom

        })


}
// ############################################################################################################
function showRandomWord(res) {
    console.log(res)
    clearUL()
    data = `
    <section >
    <span class='d-inline'>
    <h1> ${res.word}</h1>
    </span>
    </section>
`
    // the api has descrepency in showing the IPA
    // add pronunciation
    if (res.pronunciation && res.pronunciation.all) {
         data += `
        <section >
        <span class='d-inline'>
        <h4> IPA: ${res.pronunciation.all}</h4>
        </span>
        </section>
    `
    }
    // add pronunciation
    else {
         data += `
        <section >
        <span class='d-inline'>
        <h4> IPA not available!</h4>
        </span>
        </section>
    `
    }

    if (res.results) {
        // extract other data
        res.results.forEach(result => {
            // add part of speech:
            data += `Part of Speech: ${result.partOfSpeech}`
            // add defenition:
            data += `<section> <p>
            Definition: ${result.definition}
            </p>
            </section>
            `
            // add example:
            if (result.examples) {
                data += `
                <section > <p>
            Example: ${result.examples[0]}
            </p>
            </section>
                `
            }



             // add synonyms
             if (result.synonyms) {
                syns = ''
                result.synonyms.forEach(syn => {
                    syns += `${syn}, `
                })
                // remove the last comma from syns
                syns = syns.slice(0, syns.length-2)
                data += `
                <section class = 'border-bottom' > <p>
            Synonyms : ${syns}.
            </p>
            </section>
                `
             }

             append(data)
            })

    }
    // Todo:-
    // add a button
    // listen for clicks on the button
    // send a word details to an api I'll make later on
    // handle it and create a resource.

}

// ############################################################################################################

function append(data) {
    // console.log(data)
    wordDataDiv.innerHTML = data;

    li.appendChild(wordDataDiv)
    list.appendChild(li)
}
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
