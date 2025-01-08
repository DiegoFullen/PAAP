<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Planes</title>

        <link rel="stylesheet" href="css/main.css">
        <link rel="stylesheet" href="css/pricing.css">
        <link rel="stylesheet" href="resources/bootstrap/css/bootstrap.min.css">

        <script src="https://kit.fontawesome.com/2cdb583688.js" crossorigin="anonymous"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        
    </head>

    <style>
    </style>

    <body>
        <header>
            <nav id="links">
                <ul class="enlaces-menu">
                    <li><a href="#" class="roboto-bold" id="linkPAAP">PAAP</a></li>
                    <li><a href="index.php" id="linkInicio">Inicio</a></li>
                    <li><a href="pricing.php" class="disabled" id="linkPlanes" >Planes</a></li>
                </ul>
                <ul class="enlaces-menu">
                    <li><a href="login.php" id="linkLogin">Login</a></li>
                    <li><a href="register.php" id="btnSign" id="linkSign">Sign Up</a></li>
                </ul>
            </nav>
        </header>

        <div class="contents">

            <div id="tittle">
                <h4 class="gupter-regular">Tus necesidades, nuestra tarea</h4>
                <p class="inter-regular">Elige el plan que sea más conveniente para tus metas</p>
                <p class="inter-regular">Nosotros nos encargamos del resto</p>
            </div>

            <div id="plans">
                <div class="container1">
                    <div class="card">
                        <div class="card-body">
                            <button class="btn btn-primary imprima-regular">Integrado</button>
                            <h5 class="card-title faustina-regular">Para todos nuestros usuarios</h5>
                            <h6 class="card-subtitle mb-2 text-muted roboto-regular">Aplicable solo una vez por correo</h6>
                            <p class="card-text roboto-regular">Ideal para aquellos que desean empezar en el mundo de la IA o para probar las capacidades de la plataforma. Simple pero elegante.</p>
                            <span class="price">$0</span><span>/hora</span>
                            <hr>
                            <p>
                                <span>· 2hr de entrenamiento</span><br>
                                <span>· Entrenamiento por Árbol de decisión</span><br>
                                <span>· Acceso a recursos de usuario</span><br>
                                <span class="espaciado">· Guías de Funcionamiento</span><br>
                                <span class="espaciado">· Manual de Usuario</span><br>
                            </p>
                        </div>
                    </div>
                </div>

                <div class="container2">
                    <div class="card">
                        <div class="card-body">
                            <button class="btn btn-primary">Pro</button>
                            <h5 class="card-title faustina-regular">Desata el potencial de la IA</h5>
                            <p class="card-text roboto-regular"><br>Ideal si quieres mantener tus proyectos por venir respaldados por el potencial de la IA</p><br>
                            <span class="price">$80</span><span>/hora</span>
                            <hr>
                            <p>
                                <span>· Entrenamiento por Árbol de decisión</span><br>
                                <span>· Entrenamiento por KNN</span><br>
                                <span>· Entrenamiento por Random Forest</span><br>
                                <span>· Acceso a recursos de usuario</span><br>
                                <span class="espaciado">· Guías de Funcionamiento</span><br>
                                <span class="espaciado">· Manual de Usuario</span><br>
                            </p>
                        </div>
                    </div>
                </div>

                <div class="container3">
                    <div class="card">
                        <div class="card-body">
                            <button class="btn btn-primary">CETI</button>
                            <h5 class="card-title faustina-regular">Para inversión estudiantil</h5>
                            <p class="card-text roboto-regular"><br>Poder de una cuenta Pro al alcance del estudio. Requiere un correo insitucional vigente</p><br>
                            <span class="price">$30</span><span>/hora</span>
                            <hr>
                            <p>
                                <span>· Entrenamiento por Árbol de decisión</span><br>
                                <span>· Entrenamiento por KNN</span><br>
                                <span>· Entrenamiento por Random Forest</span><br>
                                <span>· Acceso a recursos de usuario</span><br>
                                <span class="espaciado">· Guías de Funcionamiento</span><br>
                                <span class="espaciado">· Manual de Usuario</span><br>
                            </p>
                        </div>
                    </div>
                </div>

            </div>

        </div>


        <script src="js/login.js"></script>
        <script src="resources/bootstrap/js/bootstrap.min.js"></script>
    </body>
</html>