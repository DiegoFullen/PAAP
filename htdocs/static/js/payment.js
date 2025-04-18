const $inputHoras = document.getElementById("horasAlquiler");
const $inputAlquiler = document.getElementById("presupuesto");
const $inputPlan = document.getElementById("accountType");

$inputHoras.addEventListener("input", () => {
    var horas = parseFloat($inputHoras.value) || 0;
    horas = horas / 60;
    var total;
    if ($inputPlan.value === 'Escolar') {
        total = horas * 30;
    } else {
        total = horas * 80;
    }
    $inputAlquiler.style.fontSize = "1.4rem";
    $inputAlquiler.value = '$' + total.toFixed(2) + ' MXN';

    if(horas === 0) {
        $inputAlquiler.style.fontSize = "1rem";
        $inputAlquiler.value = "";
    }
});

if (typeof paypal !== 'undefined') {
    paypal.Buttons({
        style: {
            color: 'blue',
            shape: 'pill',
            label: 'pay',
        },
        createOrder: function(data, actions) {
            const horas = parseFloat($inputHoras.value) || 0;
            var total = (horas / 60) * 80;
            if ($inputPlan.value === 'Escolar') {
                total = (horas / 60) * 30;
            }
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: total.toFixed(2)
                    }
                }]
            });
        },
        onApprove: function(data, actions) {
            actions.order.capture().then(function(detalles) {
                console.log(detalles);
                const horas = $inputHoras.value || 0;
                window.location.href = `/gestion_usuarios/dashboard/payment/hours/?horas=${horas}`;
                alert("Pago Realizado");
            });
        },
        onCancel: function(data) {
            alert("Pago Cancelado");
        }
    }).render('#paypal-button-container');
} else {
    console.error("El SDK de PayPal no está cargado. Verifica la referencia en tu HTML.");
}
