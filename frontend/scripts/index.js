import "./resize.js";
import domalt from "./domalt/domalt.js";

async function getFullAnalysis() {
    const res = await fetch("/api/full_analysis", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ sentence: document.getElementById("user-sentence").value }) 
    });
    const data = await res.json();

    const container = document.getElementById("result");
    clearElem(container);
    document.querySelector("main").classList.add("result-displayed");
    container.append(domalt.newElem({
        tag: "h2",
        content: data.analysis
    }));
    container.append(domalt.newElem({
        tag: "p",
        content: data.received_sentence
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

document.getElementById("analyze").addEventListener("click", getFullAnalysis);