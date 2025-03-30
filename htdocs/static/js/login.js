//Alinear el captcha con el resto de la interfaz
window.onload = function () {
    const recaptcha = document.querySelector(".g-recaptcha iframe");
    if (recaptcha) {
        recaptcha.style.maxWidth = "100%";
        recaptcha.style.height = "auto";
    }
};

const inputEmail = document.getElementById("email")
const labelEmail = document.getElementById("labelEmail");
const inputPassword = document.getElementById("password")
const labelPassword = document.getElementById("labelPassword");

const passwordClear = document.getElementById("passwordClear");

inputEmail.addEventListener("input", function(){
    /*labelEmail.style.color = "blue";*/
    if (inputEmail.value.trim() !== "") {
        labelEmail.style.fontSize = "xx-small";
        /*labelEmail.style.display = "none";*/ 
    } else {
        labelEmail.style.fontSize = ""; 
    }
});

inputPassword.addEventListener("input", function(){
    /*labelEmail.style.color = "blue";*/
    if (inputPassword.value.trim() !== "") {
        labelPassword.style.fontSize = "xx-small";
    } else {
        labelPassword.style.fontSize = ""; 
    }
});

passwordClear.addEventListener("click", () => {
    inputPassword.type = inputPassword.type === "password" ? "text" : "password";
});
    
