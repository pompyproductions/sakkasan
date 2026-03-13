import "./resize.js";
import domalt from "./domalt/domalt.js"

function clearElem(elem) {
    while (elem.firstChild) {
        elem.removeChild(elem.firstChild)
    }
}

function newIconInline(name) {
    return domalt.newElem({
        tag: "span",
        class: "material-symbols-outlined",
        content: name
    })
}

console.log("hey");