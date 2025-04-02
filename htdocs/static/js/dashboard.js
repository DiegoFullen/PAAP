(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
    
    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

const btnErase = document.getElementById("btnErase");
const confirmErase = document.querySelector("dialog.alertDialog");
const eraseAccept = document.getElementById("eraseAccept");
const eraseDeny = document.getElementById("eraseDeny");

btnCancelar.addEventListener("click", () => {
  dialogElem.close();
});

btnErase.addEventListener("click", () => {
  confirmErase.showModal();
});

eraseAccept.addEventListener("click", () => {
  confirmErase.close();
});

eraseDeny.addEventListener("click", () => {
  confirmErase.close();
});

document.getElementById('selectModel').addEventListener('change', function() {
  const selectedOption = this.options[this.selectedIndex];
  if (!selectedOption.value) {
      document.getElementById('displayModelName').textContent = '';
      document.getElementById('displayDatasetName').textContent = 'Dataset';
      document.getElementById('displayModelType').textContent = 'Algoritmo';
      document.getElementById('displayModelTypeTraining').textContent = 'Reg/Cla';
      return;
  }
  const modelName= selectedOption.getAttribute('data-model-name');
  const datasetName = selectedOption.getAttribute('data-dataset-name');
  const modelType = selectedOption.getAttribute('data-model-type');
  const modelTypeTraining = selectedOption.getAttribute('data-model-training');
  document.getElementById('displayModelName').textContent = modelName;
  document.getElementById('displayDatasetName').textContent = datasetName;
  document.getElementById('displayModelType').textContent = modelType;
  document.getElementById('displayModelTypeTraining').textContent = modelTypeTraining;
  const modelId = selectedOption.value;
  console.log("Modelo seleccionado ID:", modelId);
});

document.getElementById('btnErase').addEventListener('click', function() {
  const selectedOption = document.getElementById('selectModel').selectedOptions[0];
  if (!selectedOption || !selectedOption.value) {
    alert('Por favor selecciona un modelo primero');
    return;
  }

  const modelId = selectedOption.getAttribute('data-model-id');
  const datasetId = selectedOption.getAttribute('data-dataset-id');
  const eraseDialog = document.querySelector('.alertDialog');
  eraseDialog.showModal();
  const eraseAccept = document.getElementById('eraseAccept');
  const eraseDeny = document.getElementById('eraseDeny');
  
  eraseAccept.onclick = null;
  eraseDeny.onclick = null;

  eraseAccept.addEventListener('click', function() {
    const deleteUrl = `/gestion_usuarios/delete_model/${modelId}/${datasetId}/`;
    window.location.href = deleteUrl;
    eraseDialog.close();
  });

  eraseDeny.addEventListener('click', function() {
    eraseDialog.close();
  });
});