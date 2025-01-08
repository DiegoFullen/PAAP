<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro</title>

    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/register.css">
    <link rel="stylesheet" href="resources/bootstrap/css/bootstrap.min.css">

    <link href="js/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">
    <link href="css/sb-admin-2.min.css" rel="stylesheet">
</head>

<style>
</style>

<body>
    <header>
        <nav id="links">
            <ul class="enlaces-menu">
                <li><a href="#" class="roboto-bold" id="linkPAAP">PAAP</a></li>
                <li><a href="index.php" id="linkInicio">Inicio</a></li>
                <li><a href="pricing.php" id="linkPlanes">Planes</a></li>
            </ul>
            <ul class="enlaces-menu">
                <li><a href="login.php" id="linkLogin">Login</a></li>
                <li><a class="" href="" id="btnSign" id="linkSign">Sign Up</a></li>
            </ul>
        </nav>
    </header>

    <div class="content">
            <div class="container-fluid">
                <div class="row" id="title">
                    <div class="col"></div>
                    <div class="col">
                        <p1>Registre su información</p1><br>
                        <p>Complete el siguiente formulario para empezar a disfrutar los beneficios de nuestra plataforma </p>
                    </div>
                    <div class="col"></div>
                </div>

                <div class="row mt-5">
                    <div class="col-1"></div>
                    <div class="col">

                        <div class="card mb-4 border-box" id="accountInfo">
                            <div class="card-body border-box">
                                
                                <form action="">
                                <div class="row mt-4 ml-4">

                                    <div class="col-6">
                                        <label for="accountName" class="col-form-label">Nombre/s*</label>
                                        <input type="text" class="form-control ml-3" id="accountName" style="width: 100%;" placeholder="Héctor Mariano" value="" required pattern="[A-Za-z]+" title="Solo se permiten carácteres">
                                    </div>

                                    <div class="col">
                                        <label for="accountFLast" class="col-form-label">Primer Apellido*</label>
                                        <input type="text" class="form-control ml-3" id="accountFLast" placeholder="Padilla" value="" required pattern="[A-Za-z]+" title="Solo se permiten carácteres">
                                    </div>

                                    <div class="col">
                                        <label for="accountSLast" class="col-form-label">Segundo Apellido*</label>
                                        <input type="text" class="form-control ml-3" id="accountSLast" placeholder="Rodríguez" value="" required pattern="[A-Za-z]+" title="Solo se permiten carácteres">
                                    </div>
                                </div>

                                <div class="row mt-5 ml-4">
                                    <div class="col">
                                        <label for="accountEmail" class="col-form-label">Correo Electrónico</label>
                                        <input type="email" class="form-control ml-3" id="accountEmail" placeholder="alumnoCeti@ceti.mx" value="" style="width: 100%; cursor:default;" required>
                                    </div>

                                    <div class="col">
                                        <label for="accountEmailBack" class="col-form-label">Correo Recuperación*</label>
                                        <input type="email" class="form-control ml-3" id="accountEmailBack" placeholder="alumnoCeti@ceti.mx" value="" style="width: 100%;" required>
                                    </div>

                                </div>

                                <div class="row mt-5 ml-4">

                                    <div class="col">
                                        <label for="accountUsername" class="col-form-label">Nombre Usuario*</label>
                                        <input type="text" class="form-control ml-3" id="accountUsername" placeholder="User123" required minlength="6">
                                    </div>

                                    <div class="col">
                                        <label for="accountPassword" class="col-form-label">Contraseña*</label><i class="fas fa-solid fa-eye pl-3" style="color: black;" id="clearPassword"></i>
                                        <input type="password" class="form-control ml-3" id="accountPassword" placeholder="**********" required minlength="8">
                                    </div>

                                    <div class="col">
                                        <label for="passwordCon" class="col-form-label">Confirmación*</label>
                                        <input type="password" class="form-control ml-3" id="passwordCon" placeholder="**********" required minlength="8">
                                    </div>
                                </div>

                                <div class="row justify-content-md-end" style="margin-top: 8rem;">
                                    <div class="col-md-auto"><span>Campos Obligatorios*</span></div>
                                    <div class="col-6"></div>
                                    <div class="col-md-auto">
                                        <button class="btn btn-primary mr-3">Confirmar</button>
                                    </div>
                                </div>

                            </div>
                            </form>
                        </div>

                    </div>
                    <div class="col-1"></div>
                </div>
            </div>
        </div>


    <script src="js/main.js"></script>
    <script src="resources/bootstrap/js/bootstrap.min.js"></script>

    <script src="js/vendor/jquery/jquery.min.js"></script>
    <script src="js/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="js/vendor/jquery-easing/jquery.easing.min.js"></script>
</body>

</html>