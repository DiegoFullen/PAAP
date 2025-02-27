const $d = document;
const btnValidate = $d.getElementById("btnValidate");
const inputPassword = $d.getElementById("accountPassword");
const requiertList = $d.querySelectorAll(".requirements li")

const requirments = [
    { regex: /.{8,}/, index: 0 },
    { regex: /[0-9]/, index: 1 },
    { regex: /[a-z]/, index: 2 },
    { regex: /[A-Z]/, index: 3 },
    { regex: /[^A-Za-z0-9]/, index: 4 },
]

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


//Funcionalidad de botón para visualización y censura de contraseña
document.getElementById('togglePassword').addEventListener('click', function () {
    var passwordField = document.getElementById('accountPassword');
    var icon = this;
    passwordField.type = passwordField.type === "password" ? "text" : "password";
    icon.classList.toggle('fa-eye-slash', passwordField.type === "text");
    icon.classList.toggle('fa-eye', passwordField.type === "password");
});

document.getElementById('togglePassword2').addEventListener('click', function () {
    var passwordField = document.getElementById('accountPassword2');
    var icon = this;
    passwordField.type = passwordField.type === "password" ? "text" : "password";
    icon.classList.toggle('fa-eye-slash', passwordField.type === "text");
    icon.classList.toggle('fa-eye', passwordField.type === "password");
});