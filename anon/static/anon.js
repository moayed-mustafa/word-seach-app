


// get the stuff you want from the dom and define important variables
form = document.getElementById('form')
list = document.getElementById('words')
word = document.getElementById('wordInput')
console.log(word.value)
URL = "https://wordsapiv1.p.rapidapi.com/words"
HEADERS =  {
    "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
    "x-rapidapi-key": "82d62a047fmsh74091241e57a04fp1b7385jsn57e8b551a5c6"
}


// create the functions
async function fetchWord(e) {
    e.preventDefault()
    // clear up the list
    list.innerHTML = ''
    let res = await axios({
        method: 'GET',
        url: `${URL}/${word.value}`,
        headers:HEADERS,

    })
    // error handling:

    if (res.status === 200) {
        console.log(res)
        showWords(res)
    }




     if(res.status === 404) {
        // code breakes before I can get here!

    }
}

// show words on the screen
function showWords(res) {
    console.log(res.data)
        // craeate the li element
        let li = document.createElement('li');
        li.classList.add('list-group-item')
        // console.log(res.data.results)
        // craete the div that will have the word information
        let wordDataDiv = document.createElement('div')
        wordDataDiv.classList.add('word-data-div')

        // add string data
        let data = `
            <section >
            <span class='d-inline'>
            <h1> ${res.data.word}</h1>
            <p>IPA: ${res.data.pronunciation.all}</p>
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
             else {
                 data += `
                 <div class = 'border-bottom m2'></div>

                 `
            }


        })

        wordDataDiv.innerHTML = data;
        li.appendChild(wordDataDiv)
        list.appendChild(li)
}





// hook things up
form.addEventListener('submit', fetchWord)