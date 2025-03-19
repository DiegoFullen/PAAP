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
  
  if(selectedType === null){
    console.clear();
    console.warn("Element received null");
  }else{
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

function hideHyper(){
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


//Árbol
const $classWeightRange = $d.getElementById("classWeight-Tree_range");
const $classWeightValue = $d.getElementById("classWeight-Tree_value");


//Árbol
$classWeightRange.addEventListener("input", () => {
  $classWeightValue.textContent = $classWeightRange.value;
});

