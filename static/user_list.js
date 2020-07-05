// Get the delete button:
remove_word = document.querySelectorAll('.delete')
console.log(remove_word)
remove_word.forEach(btn => {
    // hook the button with the function
    btn.addEventListener('click', RemoveWordFromList)
})

flash = document.getElementById('flash')
// ############################################################################################################

// functions that works with HTML Elements
async function RemoveWordFromList() {
    def = findSibling(this, '#definition')
    element = this
    if (def) {
        //
        def = def.innerHTML.slice(12, def.innerHTML.length)
        data = { 'definition': def}
        let res = await axios.post('/delete-word', data)
        console.log(res)


        if (res.status == 200) {
            // you want to flash successfuly here
            flashTheUser('Deleted succssefuly', 'success')
            setTimeout(function () {
                removeFlash('success')
            }, 3500)
            setTimeout(function () {
                removeParent(element)
            },4500)

        }
        else {
            flashTheUser( 'something went wrong...', 'danger')
            setTimeout(function () {
                removeFlash('danger')
            }, 3500)

            setTimeout(function () {
                removeParent(element)
            },4500)
        }
    }

}
// ############################################################################################################
// traverse the dom
function findSibling(ele, selector) {
    " Traverses the dom to find the sibling that matches the selector "
    sibling = ele.previousElementSibling
    if (!selector) return null
    while (sibling) {
        if (sibling.matches(selector)) return sibling;
        sibling = sibling.previousElementSibling
    }
}
// ############################################################################################################
// remove parents
function removeParent(ele) {
    ele.parentElement.remove()
    window.location.reload()

}
// ############################################################################################################
        // flashTheUser
function flashTheUser( msg, cat) {
    setTimeout(function () {
        flash.classList.add('alert', `alert-${cat}`)
        flash.innerHTML = msg

    }, 500)


}
function removeFlash(cat) {
        flash.innerHTML = ''
        flash.classList.remove('alert', `alert-${cat}`)
}
