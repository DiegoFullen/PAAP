const btnMensaje = document.getElementById("btnConfirmar");
const dialogElement = document.querySelector("#ms-confirm");
const btnConfirmar = document.getElementById("optConfirmar");
const btnCancel = document.getElementById("optCancelar");

const btnCerrar = document.getElementById("optCerrar");
const dialogElements = document.querySelector("#ms-correct");

btnMensaje.addEventListener("click", () => {
    dialogElement.showModal();
});

btnConfirmar.addEventListener("click", ()=> {
    dialogElements.showModal();
});

btnCancel.addEventListener("click", () => {
    dialogElement.close();
});

btnCerrar.addEventListener("click", () => {
    dialogElements.close();
});