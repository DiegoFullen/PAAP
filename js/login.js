const inputEmail = document.getElementById("email")
const labelEmail = document.getElementById("labelEmail");
const inputPassword = document.getElementById("password")
const labelPassword = document.getElementById("labelPassword");

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

    