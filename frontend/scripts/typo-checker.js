import { clearElem } from "./common.js";
import domalt from "./domalt/domalt.js";

async function getTypoCheck() {
    console.log("hey");
    const res = await fetch("/api/typo-checker", {
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

document.getElementById("check").addEventListener("click", getTypoCheck);