const $d = document;

const icon = $d.getElementById("clearPassword");
const inputPassword = $d.getElementById("newPassword");
const labelPassword = $d.getElementById("labelNewPassword");
const inputConfirmation = $d.getElementById("newPasswordCon");
const labelConfirmation = $d.getElementById("labelNewPasswordCon");
const btnValidate = $d.getElementById("btnValidatePassword");


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

icon.addEventListener("click", e => { 
    if(inputPassword.type === "password" && inputConfirmation.type === "password"){
        inputPassword.type = "text";
        inputConfirmation.type = "text";
    }else{
        inputPassword.type = "password";
        inputConfirmation.type = "password";
    }
 });

 btnValidate.addEventListener("click", function(event){
    const inputPassword = $d.getElementById("newPassword").value;
    const inputConfirmation = $d.getElementById("newPasswordCon").value;

    //const newEmail = sanitizeInput(inputEmail);
    //const newRetrieve = sanitizeInput(inputRetrieve);
    if(isNotEmpty(inputPassword) && isNotEmpty(inputConfirmation)){

        if(isValidPassword(inputPassword)){
            if(inputPassword === inputConfirmation){
                alert("Contraseña Actualizada con Exito");
                window.location = '/gitPAAP/PAAP/';
            }else{
                alert("Las contraseñas no son las mismas. Favor de revisar las contraseñas");
            }
        }else{
            window.alert("Ingrese una contraseña valida");
        }
    }else{
        window.alert("No deje campos vacios");
    }
 });

    

function isValidPassword(password) {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return regex.test(password);
}

function isNotEmpty(cadena) {
    if (typeof cadena === "string" && cadena.length === 0 || cadena === null) {
        return false;
    } else{
        return true;
    }
}