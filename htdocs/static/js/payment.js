const $inputHoras = document.getElementById("horasAlquiler");
const $inputAlquiler = document.getElementById("presupuesto");

$inputHoras.addEventListener("input", () => {
    var horas = $inputHoras.value || 0;
    horas = horas/60;
    const total = horas * 80;

    $inputAlquiler.style.fontSize = "1.4rem";
    $inputAlquiler.value = '$' + total + ' MXN';

    if(horas === 0){
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
            const horas = $inputHoras.value || 0;
            const total = horas * 80;
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
                // Obtén el valor de las horas ingresadas
                const horas = $inputHoras.value || 0;

                // Redirecciona con las horas como un parámetro en la URL
                window.location.href = `hours/?horas=${horas}`;
                alert("Pago Realizado");
            });
        },
        onCancel: function(data) {
            alert("Pago Cancelado");
            // Redirige o realiza otra acción en caso de cancelación
            // window.location.href = "/dashboard/payment/";
        }
    }).render('#paypal-button-container');
} else {
    console.error("El SDK de PayPal no está cargado. Verifica la referencia en tu HTML.");
}

