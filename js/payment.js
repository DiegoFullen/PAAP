const $inputHoras = document.getElementById("horasAlquiler");
const $inputAlquiler = document.getElementById("presupuesto");

$inputHoras.addEventListener("input", ()=> {
    var aux = $inputHoras.value;
    aux = aux * 80;
    
    $inputAlquiler.value = '$' + aux;
});