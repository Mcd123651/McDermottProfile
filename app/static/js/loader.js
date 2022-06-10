

let loader = document.querySelector(".loader")

function hidePage() {
    loader.style.display = "block";
    document.getElementById("main").style.display = "none";
}

function showPage() {
    loader.style.display = "none";
    document.getElementById("main").style.display = "block";
}

hidePage();
window.addEventListener('load', () => {
  showPage()
});
