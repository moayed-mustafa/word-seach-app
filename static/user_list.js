// Get the delete button:
remove_word = document.querySelectorAll('.delete')
remove_word.forEach(btn => {
    // hook the button with the function
    btn.addEventListener('click', RemoveWordFromList)
})

flash = document.getElementById('flash')
// ############################################################################################################

// functions that works with HTML Elements
async function RemoveWordFromList() {
         /**
 * [sends a request to my api for deleting a word from the user's list]
 * @return {[type]}      [no return value]
 */
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
         /**
 * [finds a sibling with a specific selector]

 * @param  {[DOM Element]} ele [the element that is the starting point]
 * @param  {[String]} selector [the selector for the element I wish to find]
 * @return {[type]}      [no return value]
 */
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
/**
 * [removes a parent of a specific element]
 * @param  {[DOM Element]} ele [the element I wish to remove its parent]
 * @return {[type]}      [no return value]
    */
   ele.parentElement.remove()
    reloadPage()
}
// ############################################################################################################
function reloadPage() {
/**
 * [reloads the page]
 * @return {[type]}      [no return value]
*/
    window.location.reload()
}

// ############################################################################################################
        // flashTheUser
function flashTheUser(msg, cat) {
/**
 * [flashes the user]

 * @param  {[String]} msg  [the msg that is showen to the user]
 * @param  {[String]} cat [a category calss to style the flash div]
 * @return {[type]}      [no return value]
*/
    setTimeout(function () {
        flash.classList.add('alert', `alert-${cat}`)
        flash.innerHTML = msg

    }, 500)


}
function removeFlash(cat) {
    /**
 * [removes the flashe from the screen]
 * @param  {[String]} cat [a category calss to style the flash div]
 * @return {[type]}      [no return value]
*/
        flash.innerHTML = ''
        flash.classList.remove('alert', `alert-${cat}`)
}
