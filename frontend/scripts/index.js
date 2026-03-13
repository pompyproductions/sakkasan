import domalt from "./domalt/domalt.js";

async function getGreeting() {
    const res = await fetch("/api/greet");
    const data = await res.json();

    const container = document.getElementById("result");
    clearElem(container);
    document.querySelector(".vsep").classList.remove("hidden");
    container.append(domalt.newElem({
        tag: "h2",
        content: data.greeting
    }));
}

function clearElem(elem) {
    while (elem.firstChild) {
        elem.removeChild(elem.firstChild)
    }
}

function newIcon(name) {
    return domalt.newElem({
        tag: "span",
        class: "material-symbols-outlined",
        content: name
    })
}

document.getElementById("get-greeting").addEventListener("click", getGreeting);