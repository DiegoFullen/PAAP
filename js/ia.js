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