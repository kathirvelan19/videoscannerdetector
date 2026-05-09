function addEvent(text) {
    const timeline = document.getElementById("timeline");

    const div = document.createElement("div");
    div.className = "event";
    div.innerText = text;

    timeline.prepend(div);
}