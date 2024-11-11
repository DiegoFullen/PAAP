<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>

        <link rel="stylesheet" href="css/main.css">
        <link rel="stylesheet" href="css/login.css">
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
            <nav>
                <ul class="enlaces-menu">
                    <li><a href="#" class="roboto-bold" id="linkPAAP">PAAP</a></li>
                    <li><a href="index.php" id="linkInicio">Inicio</a></li>
                    <li><a href="#" id="linkPlanes">Planes</a></li>
                </ul>
                <ul class="enlaces-menu">
                    <li><a href="#" id="linkLogin" class="disabled">Login</a></li>
                    <li><a href="#" id="btnSign" id="linkSign">Sign Up</a></li>
                </ul>
            </nav>
        </header>

        <section class="vh-80 gradient-custom">
            <div class="container py-5 h-80">
                <div class="row d-flex justify-content-center align-items-center h-90">
                <div class="col-12 col-md-8 col-lg-6 col-xl-4">
                    <div class="card bg-white text-black" style="border-radius: 1rem;">
                        <div class="card-body text-center mx-auto" id="cardLogin">

                            <img src="resources/img/logotipoColor.png" class="img-fluid rounded" style="max-width: 50%;" alt="...">
                            <div class="container cajaLimite px-5">
                                <form>
                                    <label for="email" class="toplabel mt-4 mb-2">Email</label>
                                    <div class="form-floating mb-3">
                                    <i class=" icon bi bi-envelope-at"></i>
                                        <input type="email" class="form-control" name="email" id="email" placeholder="example15@example.com" required>
                                        <label for="email" id="labelEmail">example15@example.com</label>
                                    </div>
                                    <label for="password" class="toplabel mt-4 mb-2">Password</label>
                                    <div class="form-floating mb-4">
                                        <i class="icon bi bi-person-lock"></i>
                                        <input type="password" class="form-control" name="password" id="password" placeholder="**************" required  >
                                        <label for="password" id="labelPassword">********</label>
                                    </div>

                                    <button type="button" class="btn btn-outline-light w-100 mt-4 mb-3">Iniciar Sesión</button>
                                </form>
                                
                                <a href="#" id="recovery">¿Olvidaste tu contraseña?</a>
                                <hr class="w-100 mb-5">

                                <script src="https://accounts.google.com/gsi/client" async></script>
                                <div id="g_id_onload"
                                    data-client_id="YOUR_GOOGLE_CLIENT_ID"
                                    data-login_uri="https://your.domain/your_login_endpoint"
                                    data-auto_prompt="false">
                                </div>
                                <div class="g_id_signin"
                                    data-type="standard"
                                    data-size="large"
                                    data-theme="outline"
                                    data-text="sign_in_with"
                                    data-shape="rectangular"
                                    data-logo_alignment="left">
                                </div>
                                <div class="mb-5"></div>
                                <a href="dashboard.php" class="btn btn-outline-dark w-100 mt-4 mb-3">Dashboard</a>
                            </div>
                            
                        </div>
                    </div>
                </div>
                </div>
            </div>
            </section>

        <script src="js/login.js"></script>
        <script src="resources/bootstrap/js/bootstrap.min.js"></script>
    </body>
</html>

