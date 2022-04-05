const selected = document.querySelector(".selected");
const selected2 = document.querySelector(".selected-2");
const optionsContainer = document.querySelector(".options-container");
const optionsContainer2 = document.querySelector(".options-container-2");
const optionsList = document.querySelectorAll(".option");
const optionsList2 = document.querySelectorAll(".option-2");

selected.addEventListener("click", () => {
    optionsContainer.classList.toggle("active");
});

selected2.addEventListener("click", () => {
    optionsContainer2.classList.toggle("active");
});
optionsList.forEach(o => {
    o.addEventListener("click", () => {
        selected.innerHTML = o.querySelector("label").innerHTML;
        optionsContainer.classList.remove("active");
    })
});

optionsList2.forEach(o => {
    o.addEventListener("click", () => {
        selected2.innerHTML = o.querySelector("label").innerHTML;
        optionsContainer2.classList.remove("active");
    })
});