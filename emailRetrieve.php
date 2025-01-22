<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recuperación de Contraseña</title>

        <link rel="stylesheet" href="css/main.css">
        <link rel="stylesheet" href="css/emailRetrieve.css">
        <link rel="stylesheet" href="resources/bootstrap/css/bootstrap.min.css">

        <script src="https://kit.fontawesome.com/2cdb583688.js" crossorigin="anonymous"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        
    </head>

    <style>
        body{
            background:url('resources/img/fondo.png') repeat center center fixed;
        }
    </style>

    <body>
        <header>
        </header>

        <section class="vh-80 gradient-custom">
            <div class="container py-5 h-80 mt-5">
                <div class="row d-flex justify-content-center align-items-center h-90">
                <div class="col-12 col-md-8 col-lg-6 col-xl-4">
                    <div class="card bg-white text-black" style="border-radius: 1rem;">
                        <div class="card-body text-center mx-auto" id="cardLogin">

                            <img src="resources/img/logotipoColor.png" class="img-fluid rounded" style="max-width: 50%;" alt="...">
                            <p class="mt-3">Ingrese la cuenta y correo de recuperación correspondientes para continuar</p>
                            <div class="container cajaLimite px-5">
                                <form>
                                    <label for="email" class="toplabel mt-4 mb-2">Email de Cuenta</label>
                                    <div class="form-floating mb-3">
                                        <input type="email" class="form-control" name="email" id="email" placeholder="example15@example.com" required>
                                        <label for="email" id="labelEmail">example15@example.com</label>
                                    </div>
                                    <label for="password" class="toplabel mt-4 mb-2">Email de Recuperación</label>
                                    <div class="form-floating mb-4">

                                        <input type="email" class="form-control" name="retrieveEmail" id="retrieveEmail" placeholder="example16@example.com" required  >
                                        <label for="retrieveEmail" id="labelRetrieve">example16@example.com</label>
                                    </div>

                                    <button type="button" class="btn btn-light w-100 mt-4 mb-2" id="btnSendMail" onclick="sendMail()">Enviar Correo</button>
                                    <button type="button" class="btn btn-outline-danger w-100 mb-3" id="btnCancel" onclick="goBack()">Cancelar</button>
                                </form>
                            
                            </div>
                            
                        </div>
                    </div>
                </div>
                </div>
            </div>
            </section>

        <script type="text/javascript" src="js/emailRetrieve.js"></script>
        <script src="resources/bootstrap/js/bootstrap.min.js"></script>
    </body>
</html>

