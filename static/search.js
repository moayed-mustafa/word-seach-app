


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
let flask_flash = document.querySelector('.welcome')



let headerLi = document.createElement('li');
headerLi.classList.add('list-group-item')

let URL = "https://wordsapiv1.p.rapidapi.com/words/"
let HEADERS =  {
    "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
    "x-rapidapi-key": "82d62a047fmsh74091241e57a04fp1b7385jsn57e8b551a5c6"
}
currentUrl = window.location.href
// you can instead of donig this, just check if user is included here because of the ? that shows up sometimes
guest_user =  currentUrl.slice(currentUrl.length-4,currentUrl.length )
console.log(guest_user)



                                        // #############
                                        //###### Build #####
                                       //###### Neccesary #####
                                        //###### Functions   #####
                                        //#########################


async function fetchWord(e) {
    // Fetchs a word defenition entered by the user.
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
                handleError(e.response.data.message)
            }
        }
    }
}
// ############################################################################################################
async function fetchRandomWord() {
    // fetches a random word.
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
function handleWordNotEntered() {
    // handles a submit without entering a word
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
function handleError(message) {
    // handles server error
    setTimeout(function () {
        let alert = `<div class="alert alert-danger mt-2" role="alert">
                    ${message}
                    </div>`
        list.innerHTML = alert
        }, 100)
        // clear the alert after 2 sec
        setTimeout(function () {
            list.innerHTML = ''
        }, 3000)
}
// ############################################################################################################

// show words on the screen
function showWords(res) {
    // draws part of the word info on the UI and calls a function that draws the rest
    console.log(res.data)

    clearUL()

    let span =  `
    <span>
    <h1> ${res.data.word}</h1>
    <h3>IPA: ${res.data.pronunciation.all}</h3>
    </span>
    `
    headerLi.innerHTML = span

    headerLi.classList.add('border-bottom', 'm2')
    list.appendChild(headerLi)
    // package word and pronuncitation in an object to send with the results

    extractData(res.data.results, res.data.pronunciation.all)
}
// ############################################################################################################
function showRandomWord(res) {
    // draws a random word on the UI and calls a function that draws the rest
    console.log(res)
    clearUL()

    let pron = null;
    let span = `
    <span>
    <h1> ${res.word}</h1>

    </span>
    `
    headerLi.innerHTML = span
    // the api has descrepency in showing the IPA
    // add pronunciation
    if (typeof(res.pronunciation) == 'string' || typeof(res.pronunciation) == 'object') {
        if (typeof (res.pronunciation) == 'string') {
            pron = res.pronunciation
            let IPA = `

           <span >
           <h4> IPA: ${res.pronunciation}</h4>
           </span>

       `
           headerLi.innerHTML += IPA
        }
        else if (typeof (res.pronunciation) == 'object') {
            pron = res.pronunciation.all
            let IPA = `

           <span >
           <h4> IPA: ${res.pronunciation.all}</h4>
           </span>

       `
           headerLi.innerHTML += IPA
        }
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
        extractData(res.results, pron)
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
function extractData(results, pronunciation) {
    // does the overlapping html drawing between the random search and ususal search
    let id =0
    results.forEach( result => {
        // craete an li here and add id to it
    my_li = document.createElement('li')

        // part of speech and defenition:
    let pos = `<p><b>Part of Speech:</b>${result.partOfSpeech}</p>`
    my_li.innerHTML= pos
    let def = `<p><b>Definition:</b>${result.definition}</p>`
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
        if (guest_user == 'user') {
            makeButton(my_li,id, result, pronunciation, results)}
            // add border
            my_li.classList.add('border', 'm2', 'p-2')

    // append to the list:
    list.appendChild(my_li)

    })

}

// ############################################################################################################
 handleAddWord  =  function (results, id, flash, pronunciation) {
    // Had to use currying since my event listener accepts parameters
     // and I want to remove it in the future.
     return async function curried() {
    data = { 'word': word.value, 'pronunciation': pronunciation, 'info': results[id] }
    let res = await axios.post('/add-word', data)
         if (res.status == 201) {
            //  flash the user
             flashUser(flash, 'success', 'Word added to list!')

        btn = document.getElementById(id)
        // remove the event listener
        btn.removeEventListener('click',curried)
        // add a new listerent and associate it with delete
        btn.addEventListener('click', handleDeleteWord(results, id, flash, pronunciation))
        btn.innerHTML = 'Remove'
        btn.classList.add('btn', 'delete')
        // build the delete route
    }
}


}
// ############################################################################################################
function handleDeleteWord(results, id,flash, pronunciation) {

    return async function curried() {
        definition = {'definition':results[id].definition}
        console.log(results[id],definition)

        let res = await axios.post('/delete-word', definition)
        console.log(res)
        if (res.status != 202) {
            btn = document.getElementById(id)
            btn.removeEventListener('click', curried)
            flashUser(flash, 'danger', 'Word Removed from list!')
            btn.innerHTML = 'Add'
            btn.classList.remove('delete')
            btn.addEventListener('click',handleAddWord(results, id, flash, pronunciation) )
        }
        else {
            flashUser(flash, 'danger',res.statusText)
        }

    }
}

// ############################################################################################################
async function makeButton(listElement,id, result, pronunciation, results) {
    let data = {"definition": result.definition}
    res = await axios.post('/find-word', data)
    let flash = document.createElement('div')
    let userListBtn = document.createElement('button')
    console.log(res)
    if (res.statusText == "OK") {
        // button should show delete and has delete eventListener
        userListBtn.innerHTML = 'Remove'
        userListBtn.setAttribute('id', id)
        userListBtn.classList.add('btn', 'btn-warning','delete')
        userListBtn.addEventListener('click',handleDeleteWord(results, id, flash, pronunciation) )

    }
    else {
        userListBtn.innerHTML = 'Add'
        userListBtn.setAttribute('id', id)

        userListBtn.classList.add('btn', 'btn-warning')

        userListBtn.addEventListener('click',handleAddWord(results, id, flash, pronunciation) )

    }

    // create a div to flash the user with:
    listElement.append(flash)
    listElement.append(userListBtn)
    id++
    // return {'flash':flash,'btn':userListBtn}
}
// ############################################################################################################

function clearUL() {
    // clear up the list
    list.innerHTML = ''
}
// ############################################################################################################
function removeGreeting() {
    // removees the flash message send by flask after 2.5 seconds
    let greet = setTimeout(function () {
        flask_flash.innerHTML = ''
        flask_flash.classList.remove('alert')
    }, 2500)


}
// ############################################################################################################
function flashUser(flash, cat, msg) {
        setTimeout(function () {
        flash.classList.add('alert', `alert-${cat}`)
        flash.innerHTML = msg

    }, 500)
    setTimeout(function () {
        flash.innerHTML = ''
        flash.classList.remove('alert', `alert-${cat}`)
    },5000)
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
if (flask_flash !== null) {
    removeGreeting()
}
