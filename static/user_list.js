// Get the delete button:
remove_word = document.querySelectorAll('.delete')
console.log(remove_word)
remove_word.forEach(btn => {
    // hook the button with the function
    btn.addEventListener('click', RemoveWordFromList)
})
// ############################################################################################################

// functions that works with HTML Elements
async function RemoveWordFromList() {
    def = findSibling(this, '#definition')
    if (def) {
        def = def.innerHTML.slice(12, def.innerHTML.length)
        data = { 'definition': def}
        let res = await axios.post('/delete-word', data)
        console.log(res)
        if (res.status == 200) {
            removeParent(this)
            // you want to flash successfuly here
            console.log('Deleted')
        }
        else {
            console.log('something went wrong...')
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
}