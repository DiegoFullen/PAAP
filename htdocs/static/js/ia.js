const $d = document;
const $main = $d.querySelector("main");
const $dropZone = $d.querySelector(".dropZone");

const $selectAlgorithm = $d.getElementById("selectAlgorithm");


const $linknav = $d.getElementById("linknav");
const $fileinfo = $d.getElementById("fileInfo");

$linknav.addEventListener("click", function (e) {
  e.preventDefault();

  $('#file').click();
});

$('#file').change(function () {
  var filename = (this.files[0].name).toString(); //Puesto así ya que el objeto files pasa toda la ruta y con ".name" ya no
  $('#fileInfo').text(filename);  //Esto es jQuery, por eso se usa así 
  $('#fileInfo').css('color', 'blue');
});

$selectAlgorithm.addEventListener("change", () => {
  const selectedValue = $d.getElementById("selectAlgorithm").value;
  var selectedType = document.querySelector('input[name="algoritmoType"]:checked');

  // Esconder divs
  hideHyper();

  if (selectedType === null) {
    console.clear();
    console.warn("Element received null");
  } else {
    var selectedType = document.querySelector('input[name="algoritmoType"]:checked').value;
    showHyper(selectedValue, selectedType);
  }
});

$d.querySelectorAll('input[name="algoritmoType"]').forEach((radio) => {
  radio.addEventListener("change", function () {

    const evt = new Event("change");
    $selectAlgorithm.dispatchEvent(evt);
  });
});

function hideHyper() {
  document.querySelectorAll(".hiper").forEach(div => {
    div.classList.add("hidden");
  });
}

function showHyper(selectedValue, selectedType) {
  // Mostrar el div correspondiente
  if (selectedValue) {
    const targetDiv = document.getElementById(`${selectedValue}_${selectedType}`);
    if (targetDiv) {
      targetDiv.classList.remove("hidden");
    } else {
      console.clear();
      console.warn(`Element with ID "${selectedValue}_${selectedType}" not found`);
    }
  }
}

//Input & Value
//Árbol
const $classWeightRange = $d.getElementById("classWeight-Tree_range");
const $classWeightValue = $d.getElementById("classWeight-Tree_value");

//Random Forest
const $activeBootstrapRadio = $d.getElementById("activadoRadio-RNF_reg");
const $deactiveBootstrapRadio = $d.getElementById("desactivadoRadio-RNF_reg");
const $maxSampleInput = $d.getElementById("max_sampleInput-RNF_reg");

const $activeBootstrapRadio_2 = $d.getElementById("activadoRadio-RNF_class");
const $deactiveBootstrapRadio_2 = $d.getElementById("desactivadoRadio-RNF_class");
const $maxSampleInput_2 = $d.getElementById("max_sampleInput-RNF_class");

//Eventos
//Árbol
$classWeightRange.addEventListener("input", () => {
  $classWeightValue.textContent = $classWeightRange.value;
});

//Random Forest
$deactiveBootstrapRadio.addEventListener("change", () => {
  $maxSampleInput.setAttribute("disabled", "disabled");
  $maxSampleInput.value = '';
});

$activeBootstrapRadio.addEventListener("change", () => {
  $maxSampleInput.removeAttribute("disabled");
  $maxSampleInput.value = '1';
});

$deactiveBootstrapRadio_2.addEventListener("change", () => {
  $maxSampleInput_2.setAttribute("disabled", "disabled");
  $maxSampleInput_2.value = '';
});

$activeBootstrapRadio_2.addEventListener("change", () => {
  $maxSampleInput_2.removeAttribute("disabled");
  $maxSampleInput_2.value = '1';
});

//Dialog confirmación Prime Stack
const valuePrimeStack = document.getElementById("primeStack");
const confirmationDialog = document.querySelector("dialog.stack");
const btnAceptar_Confirm = document.getElementById("confirmAccept");
const btnCancelar_Confirm = document.getElementById("confirmDeny");


const formAlgorithm = document.getElementById("selectionAlgorithm");
const inputFile = document.getElementById("file");
const message = document.getElementById("message");

//Evitar envío de información al presionar Enter
formAlgorithm.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
  }
});

formAlgorithm.addEventListener("submit", function(event){
  if(inputFile.files.length === 0){
    event.preventDefault();

    message.style.backgroundColor = "red";
    message.style.color = "white";
  }else{
    confirmationDialog.showModal();
    event.preventDefault();
  }
});

btnAceptar_Confirm.addEventListener("click", () => {
  confirmationDialog.close();
  formAlgorithm.submit();
});

btnCancelar_Confirm.addEventListener("click", () => {
  confirmationDialog.close();
  valuePrimeStack.value = "";
  valuePrimeStack.focus();
});

inputFile.addEventListener("change", function (event) {
  if (inputFile.files.length > 0) {
    message.classList.add("hidden");
  } else {
    
  }
});

function isNotEmpty(value) {
  if (value === null || value === undefined) {
    return false;
  }

  if (typeof value === "string") {
    return value.trim() !== "";
  }

  if (typeof value === "number") {
    return true;
  }

  return false;
}