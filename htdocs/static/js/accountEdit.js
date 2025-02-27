const btnMensaje = document.getElementById("confirmButton");
const dialogElement = document.querySelector("#ms-confirm");
const btnConfirmar = document.getElementById("optConfirmar");
const btnCancel = document.getElementById("optCancelar");

const dialogElements = document.querySelector("#ms-correct");

btnMensaje.addEventListener("click", () => {
    //dialogElement.showModal();
});

btnConfirmar.addEventListener("click", ()=> {
    dialogElements.showModal();
});

btnCancel.addEventListener("click", () => {
    dialogElement.close();
});


// Funcionalidades para visulización y censura de la contraseña
document.getElementById('togglePassword').addEventListener('click', function() {
    var passwordField = document.getElementById('accountPassword');
    var icon = this;
    passwordField.type = passwordField.type === "password" ? "text" : "password";
    icon.classList.toggle('fa-eye-slash', passwordField.type === "text");
    icon.classList.toggle('fa-eye', passwordField.type === "password");
});


document.getElementById('togglePassword2').addEventListener('click', function() {
    var passwordField = document.getElementById('accountPassword2');
    var icon = this;
    passwordField.type = passwordField.type === "password" ? "text" : "password";
    icon.classList.toggle('fa-eye-slash', passwordField.type === "text");
    icon.classList.toggle('fa-eye', passwordField.type === "password");
});