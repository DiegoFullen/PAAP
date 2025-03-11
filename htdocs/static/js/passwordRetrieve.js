const $d = document;

const icon = $d.getElementById("clearPassword");
const inputPassword = $d.getElementById("newPassword");
const labelPassword = $d.getElementById("labelNewPassword");
const inputConfirmation = $d.getElementById("newPasswordCon");
const labelConfirmation = $d.getElementById("labelNewPasswordCon");
const btnValidate = $d.getElementById("btnValidatePassword");
const requiertList = $d.querySelectorAll(".requirements li");

//REGEX para contraseña segura
const requirments = [
    { regex: /.{8,}/, index: 0 },
    { regex: /[0-9]/, index: 1 },
    { regex: /[a-z]/, index: 2 },
    { regex: /[A-Z]/, index: 3 },
    { regex: /[^A-Za-z0-9]/, index: 4 },
]

//Evento para revisar cada regex al presionar una tecla
inputPassword.addEventListener("keyup", (e) => {
    requirments.forEach(item => {
        const isValid = item.regex.test(e.target.value);
        const requirementItem = requiertList[item.index];

        if (isValid) {
            requirementItem.firstElementChild.className = "fas fa-solid fa-check"
            requirementItem.classList.add("valid");
        } else {
            requirementItem.firstElementChild.className = "fas fa-solid fa-circle"
            requirementItem.classList.remove("valid");
        }
    });
});

//Validación de Contraseña
btnValidate.addEventListener("click", function (event) {
    const valuePassword = $d.getElementById("accountPassword").value;
    const valueRepeat = $d.getElementById("accountPassword2").value;

    //const newEmail = sanitizeInput(inputEmail);
    //const newRetrieve = sanitizeInput(inputRetrieve);
    if (isNotEmpty(valuePassword) && isNotEmpty(valueRepeat)) {

        if (isValidPassword(valuePassword)) {
            if (valuePassword === valueRepeat) {

            } else {
                event.preventDefault();
                alert("Las contraseñas no son las mismas. Favor de revisar las contraseñas");
            }
        } else {
            event.preventDefault();
            window.alert("Ingrese una contraseña valida");
        }
    } else {
    }
});



function isValidPassword(password) {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return regex.test(password);
}

function isNotEmpty(cadena) {
    if (typeof cadena === "string" && cadena.length === 0 || cadena === null) {
        return false;
    } else {
        return true;
    }
}

//Configuración de CSS Dinámica
inputPassword.addEventListener("input", function(){
    /*labelEmail.style.color = "blue";*/
    if (inputPassword.value.trim() !== "") {
        labelPassword.style.fontSize = "xx-small";
        /*labelEmail.style.display = "none";*/ 
    } else {
        labelPassword.style.fontSize = ""; 
    }
});

inputConfirmation.addEventListener("input", function(){
    /*labelEmail.style.color = "blue";*/
    if (inputConfirmation.value.trim() !== "") {
        labelConfirmation.style.fontSize = "xx-small";
    } else {
        labelConfirmation.style.fontSize = ""; 
    }
});

//Funcionalidad de visualización de contraseña
icon.addEventListener("click", e => { 
    if(inputPassword.type === "password" && inputConfirmation.type === "password"){
        inputPassword.type = "text";
        inputConfirmation.type = "text";
    }else{
        inputPassword.type = "password";
        inputConfirmation.type = "password";
    }
 });
