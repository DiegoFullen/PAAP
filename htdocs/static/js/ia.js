const $d = document;
const $main = $d.querySelector("main");
const $dropZone = $d.querySelector(".dropZone");


const $linknav = $d.getElementById("linknav");
const $fileinfo = $d.getElementById("fileInfo");

$linknav.addEventListener("click", function(e){
  e.preventDefault();

  $('#file').click();
});

$('#file').change(function(){
  var filename = (this.files[0].name).toString(); //Puesto así ya que el objeto files pasa toda la ruta y con ".name" ya no
  $('#fileInfo').text(filename);  //Esto es jQuery, por eso se usa así 
  $('#fileInfo').css('color', 'blue');
});

function showHyper(){
const selectedValue = $d.getElementById("selectAlgorithm").value;
$d.querySelectorAll(".hiper").forEach(div => {
  div.classList.add("hidden");
});

if(selectedValue){
  $d.getElementById(selectedValue).classList.remove("hidden");
}

}

//Árbol
const $nodosRange = $d.getElementById("nodosRange");
const $nodosValue = $d.getElementById("nodosValue");

const $divisorRange = $d.getElementById("divisorRange");
const $divisorValue = $d.getElementById("divisorValue");

const $hojasRange = $d.getElementById("hojasRange");
const $hojasValue = $d.getElementById("hojasValue");

const $ccpRange = $d.getElementById("ccpRange");
const $ccpValue = $d.getElementById("ccpValue");

const $max_hojasValue = $d.getElementById("max-hojasValue");
const $max_hojasRange = $d.getElementById("max-hojasRange");

const $reduccionValue = $d.getElementById("reduccionValue");
const $reduccionRange = $d.getElementById("reduccionRange");

//KNN
const $nodosRange_KNN = $d.getElementById("nodosRange-KNN");
const $nodosValue_KNN = $d.getElementById("nodosValue-KNN");

const $divisorRange_KNN = $d.getElementById("divisorRange-KNN");
const $divisorValue_KNN = $d.getElementById("divisorValue-KNN");

const $hojasRange_KNN = $d.getElementById("hojasRange-KNN");
const $hojasValue_KNN = $d.getElementById("hojasValue-KNN");

const $ccpRange_KNN = $d.getElementById("ccpRange-KNN");
const $ccpValue_KNN = $d.getElementById("ccpValue-KNN");

const $max_hojasValue_KNN = $d.getElementById("max-hojasValue-KNN");
const $max_hojasRange_KNN = $d.getElementById("max-hojasRange-KNN");

const $reduccionValue_KNN = $d.getElementById("reduccionValue-KNN");
const $reduccionRange_KNN = $d.getElementById("reduccionRange-KNN");

//RF
const $nodosRange_RF = $d.getElementById("nodosRange-RF");
const $nodosValue_RF = $d.getElementById("nodosValue-RF");

const $divisorRange_RF = $d.getElementById("divisorRange-RF");
const $divisorValue_RF = $d.getElementById("divisorValue-RF");

const $hojasRange_RF = $d.getElementById("hojasRange-RF");
const $hojasValue_RF = $d.getElementById("hojasValue-RF");

const $ccpRange_RF = $d.getElementById("ccpRange-RF");
const $ccpValue_RF = $d.getElementById("ccpValue-RF");

const $max_hojasValue_RF = $d.getElementById("max-hojasValue-RF");
const $max_hojasRange_RF = $d.getElementById("max-hojasRange-RF");

const $reduccionValue_RF = $d.getElementById("reduccionValue-RF");
const $reduccionRange_RF = $d.getElementById("reduccionRange-RF");
 
//Árbol
$nodosRange.addEventListener("input", () => {
  $nodosValue.textContent = $nodosRange.value;
});

$divisorRange.addEventListener("input", () => {
  $divisorValue.textContent = '(' + $divisorRange.value + ')';
});

$hojasRange.addEventListener("input", () => {
  $hojasValue.textContent = '(' + $hojasRange.value + ')';
});

$ccpRange.addEventListener("input",  () => {
  $ccpValue.textContent = '(' + $ccpRange.value + ')';
});

$max_hojasRange.addEventListener("input", () => {
  $max_hojasValue.textContent = '(' + $max_hojasRange.value + ')';
});

$reduccionRange.addEventListener("input", () => {
  $reduccionValue.textContent = '(' + $reduccionRange.value + ')';
});

//KNN
$nodosRange_KNN.addEventListener("input", () => {
  $nodosValue_KNN.textContent = $nodosRange_KNN.value;
});

$divisorRange_KNN.addEventListener("input", () => {
  $divisorValue_KNN.textContent = '(' + $divisorRange_KNN.value + ')';
});

$hojasRange_KNN.addEventListener("input", () => {
  $hojasValue_KNN.textContent = '(' + $hojasRange_KNN.value + ')';
});

$ccpRange_KNN.addEventListener("input",  () => {
  $ccpValue_KNN.textContent = '(' + $ccpRange_KNN.value + ')';
});

$max_hojasRange_KNN.addEventListener("input", () => {
  $max_hojasValue_KNN.textContent = '(' + $max_hojasRange_KNN.value + ')';
});

$reduccionRange_KNN.addEventListener("input", () => {
  $reduccionValue_KNN.textContent = '(' + $reduccionRange_KNN.value + ')';
});

//RF
$nodosRange_RF.addEventListener("input", () => {
  $nodosValue_RF.textContent = $nodosRange_RF.value;
});

$divisorRange_RF.addEventListener("input", () => {
  $divisorValue_RF.textContent = '(' + $divisorRange_RF.value + ')';
});

$hojasRange_RF.addEventListener("input", () => {
  $hojasValue.textContent = '(' + $hojasRange_RF.value + ')';
});

$ccpRange_RF.addEventListener("input",  () => {
  $ccpValue_RF.textContent = '(' + $ccpRange_RF.value + ')';
});

$max_hojasRange_RF.addEventListener("input", () => {
  $max_hojasValue_RF.textContent = '(' + $max_hojasRange_RF.value + ')';
});

$reduccionRange_RF.addEventListener("input", () => {
  $reduccionValue_RF.textContent = '(' + $reduccionRange_RF.value + ')';
});

const uploader = (file) => {
  const xhr = new XMLHttpRequest();
  const formData = new FormData();

  formData.append("file", file);

  xhr.addEventListener("readystatechange", e => {
    if (xhr.readyState !== 4) return;

    if (xhr.status >= 200 && xhr.status < 300) {
      let json = JSON.parse(xhr.responseText)
    } else {
      let message = xhr.statusText || "Ocurrió un error";
      console.log(`Error ${xhr.status}: ${message}`);
    }
  })
  xhr.open("POST", "assets/uploader.php");
  xhr.setRequestHeader("enc-type", "multipart/form-data");
  xhr.send(formData);
}

$dropZone.addEventListener("dragover", e => {
  e.preventDefault();
  e.stopPropagation();
  e.target.classList.add("is-active")
})

$dropZone.addEventListener("dragleave", e => {
  e.preventDefault();
  e.stopPropagation();
  e.target.classList.remove("is-active")
})

$dropZone.addEventListener("drop", e => {   //Cuando se deja "caer" el archivo en el navegador
  e.preventDefault();
  e.stopPropagation();
  const files = Array.from(e.dataTransfer.files);
  if (files.length > 1) {
    alert("Solo se permite subir un archivo");
    return;
  }

  const file = files[0];
  if (file.type !== "text/csv" && !file.name.endsWith(".csv")) {
    alert("El archivo debe ser de tipo .csv");
    return;
  }

  progressUpload(file);
  e.target.classList.remove("is-active")
})

const progressUpload = (file)=> {
  const $progress = $d.createElement("progress");
  const $span = $d.createElement("span");

  $progress.value = 0;
  $progress.max = 100;

  $main.insertAdjacentElement("beforeend", $progress);
  $main.insertAdjacentElement("beforeend", $span);

  const fileReader = new FileReader();
  fileReader.readAsDataURL(file);

  fileReader.addEventListener("progress", e => {
    let progress = parseInt((e.loaded * 100) / e.total);
    $progress.value = progress;
    $span.innerHTML = `${file.name} - ${progress}%`;

    $('#fileInfo').text(file.name);  //Esto es jQuery, por eso se usa así 
    $('#fileInfo').css('color', 'blue');
  });

  fileReader.addEventListener("loadend", e => {
    uploader(file);
    setTimeout(() => {
      $main.removeChild($progress);
      $main.removeChild($span);
    }, 2000);
  });
}