var elements = Array.from(document.getElementsByClassName("character"))
    .filter((e) => e.style.color != "");
for (var i = 0; i < elements.length; ++i) {
    var element = elements[i];
    element.textContent = String.fromCharCode(parseInt(element.textContent));
    element.style.color = "blue";
}
