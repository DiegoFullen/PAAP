const $d = document;

const inputEmail = $d.getElementById("email");
const labelEmail = $d.getElementById("labelEmail");
const inputRetrieve = $d.getElementById("retrieveEmail");
const labelRetrieve = $d.getElementById("labelRetrieve");

const btnSend = $d.getElementById("btnSendMail");
const btnCancel = $d.getElementById("btnCancel");

inputEmail.addEventListener("input", function(){
    /*labelEmail.style.color = "blue";*/
    if (inputEmail.value.trim() !== "") {
        labelEmail.style.fontSize = "xx-small";
        /*labelEmail.style.display = "none";*/ 
    } else {
        labelEmail.style.fontSize = ""; 
    }
});

inputRetrieve.addEventListener("input", function(){
    /*labelEmail.style.color = "blue";*/
    if (inputRetrieve.value.trim() !== "") {
        labelRetrieve.style.fontSize = "xx-small";
    } else {
        labelRetrieve.style.fontSize = ""; 
    }
});

document.getElementById("btnSendMail").addEventListener("click", function(){
    const inputEmail = $d.getElementById("email").value;
    const inputRetrieve = $d.getElementById("retrieveEmail").value;

    //const newEmail = sanitizeInput(inputEmail);
    //const newRetrieve = sanitizeInput(inputRetrieve);
    if(isNotEmpty(inputEmail) && isNotEmpty(inputRetrieve)){

        if(isValidEmail(inputEmail) && isValidEmail(inputRetrieve)){
            window.location = '/gestion_usuarios/emailRetrieve/recoverPassword/';
        }else{
            window.alert("Ingrese un correo valido");
        }
    }else{
        window.alert("No deje campos vacios");
    }
});

document.getElementById("btnCancel").addEventListener("click", function(){
    window.location = '/login/';
});

function sendMail(){
}


    

function isValidEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

function isNotEmpty(cadena) {
    if (typeof cadena === "string" && cadena.length === 0 || cadena === null) {
        return false;
    } else{
        return true;
    }
}