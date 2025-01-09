<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Inicio</title>
        
        <link rel="stylesheet" href="css/main.css">
        <link rel="stylesheet" href="css/index.css">
        <link rel="stylesheet" href="resources/bootstrap/css/bootstrap.min.css">

        <script src="https://kit.fontawesome.com/2cdb583688.js" crossorigin="anonymous"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    </head>

    <style>
        #img1{
            background: center / contain no-repeat url('resources/img/9af2eb6c-9779-405c-8aa4-90a8d6ddf2bd.jpeg');
            grid-column: 2;
            grid-row: 1;
        }

        #img2{
            background: center / contain no-repeat url('resources/img/logotipoColor.png');
            grid-column: 1;
            grid-row: 1;
            width: 100%;
            height: 100%;
        }

        #wallpaper{
            background: center / contain no-repeat url('resources/img/IAHuman.jpeg');
            opacity: 0.2;
            grid-column: 1/4;
            grid-row: 1/4;
            width: 100%;
        }
    </style>

    <body>
        <header>
            <nav id="links">
                <ul class="enlaces-menu">
                    <li><a href="#" class="roboto-bold" id="linkPAAP">PAAP</a></li>
                    <li><a href="index.php" id="linkInicio">Inicio</a></li>
                    <li><a href="pricing.php" id="linkPlanes" >Planes</a></li>
                </ul>
                <ul class="enlaces-menu">
                    <li><a href="login.php" id="linkLogin">Login</a></li>
                    <li><a href="register.php" id="btnSign">Sign Up</a></li>
                </ul>
            </nav>
        </header>

        <div class="content">

            <div id="card">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title gupter-regular">Libera el potencial de tus proyectos</h5>
                        <h6 class="card-subtitle mb-5 inter-italic">El poder de la IA en la palma de tu mano...</h6>
                        <p class="card-text inter-regular">Te presentamos PAAP, la Plataforma de Aprendizaje Automatico Personalizado diseñada para pensar en tus necesidades </p>
                        <p class="card-text inter-regular">Somos una plataforma web diseñada para ofrecer una solución tecnológica accesible. <br> La plataforma está enfocada 
                                                            en el manejo de datos numéricos y permite a los usuarios entrenar modelos utilizando algoritmos populares como 
                                                            Árboles de Decisión, K-Nearest Neighbors y Random Forest.  </p>
                        
                    </div>
                </div>

                <div class="imgHolder" id="img1" style="width: 500px; height: 500px;"></div>
            </div>

            <div id="info">
                <div class="title">
                    <h5 class="card-title gupter-medium">El mundo de la Inteligencia Artificial</h5>
                    <h6 class="card-subtitle mb-5 inter-italic">El futuro de la tecnología marcado por el futuro de la innovación</h6>
                </div>

                <div class="imgHolder" id="wallpaper"></div>

                <div id="topic1" class="topics">
                    <p class="card-text inter-regular title"> <i class="fas fa-code"></i> Matemática</p>
                    <p class="inter-regular">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elit ligula, fermentum at venenatis a, ornare quis est.
                            In placerat cursus diam vestibulum venenatis.</p>
                </div>

                <div id="topic2" class="topics">
                    <p class="card-text inter-regular title"> <i class="fas fa-code"></i> Procesamiento</p>
                    <p class="inter-regular">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elit ligula, fermentum at venenatis a, ornare quis est.
                            In placerat cursus diam vestibulum venenatis.</p>
                </div>

                <div id="topic3" class="topics">
                    <p class="card-text inter-regular title"> <i class="fas fa-code"></i> Educación</p>
                    <p class="inter-regular">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elit ligula, fermentum at venenatis a, ornare quis est.
                            In placerat cursus diam vestibulum venenatis.</p>
                </div>
                
                <div id="topic4" class="topics">
                    <p class="card-text inter-regular title"> <i class="fas fa-code"></i> Arte</p>
                    <p class="inter-regular">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elit ligula, fermentum at venenatis a, ornare quis est.
                            In placerat cursus diam vestibulum venenatis.</p>
                </div>

                <div id="topic5" class="topics">
                    <p class="card-text inter-regular title"> <i class="fas fa-code"></i> Conectividad</p>
                    <p class="inter-regular">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elit ligula, fermentum at venenatis a, ornare quis est.
                            In placerat cursus diam vestibulum venenatis.</p>
                </div>

                <div id="topic6" class="topics">
                    <p class="card-text inter-regular title"> <i class="fas fa-code"></i> Ciberseguridad</p>
                    <p class="inter-regular">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc elit ligula, fermentum at venenatis a, ornare quis est.
                            In placerat cursus diam vestibulum venenatis.</p>
                </div>


                <div class="title mt-5" id="title2">
                    <h5 class="card-title gupter-medium">¿Dónde entramos nosotros?</h5>
                    <h6 class="card-subtitle mb-5 inter-italic">Deja que PAAP te ayude a probar el poder de la Inteligencia Artificial</h6>
                </div>
                
                <div class="container1">
                    <div class="card">
                        <div class="card-body">
                            <img class="imgHolder" src="resources/img/info.png" alt=" information.png">
                            <h5 class="card-title faustina-bold">Manejo de Datos</h5>
                            <p class="card-text roboto-regular">Body text for whatever you’d like to say. Add main takeaway points, quotes, anecdotes, or even a very very short story.</p>
                        </div>
                    </div>
                </div>

                <div class="container2">
                    <div class="card">
                        <div class="card-body">
                            <img class="imgHolder" src="resources/img/brain.png" alt="brain.png">
                            <h5 class="card-title faustina-bold">Entrenamiento</h5>
                            <p class="card-text roboto-regular">Body text for whatever you’d like to say. Add main takeaway points, quotes, anecdotes, or even a very very short story.</p>
                        </div>
                    </div>
                </div>

                <div class="container3">
                    <div class="card">
                        <div class="card-body">
                            <img class="imgHolder" src="resources/img/goals.png" alt="goals.png">
                            <h5 class="card-title faustina-bold">Evaluación</h5>
                            <p class="card-text roboto-regular">Body text for whatever you’d like to say. Add main takeaway points, quotes, anecdotes, or even a very very short story.</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div id="milestones">
            <div id="card2">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title gupter-bold">La meta del esfuerzo conjunto</h5>
                        <h6 class="card-subtitle mb-5 inter ">Un modelo de Inteligencia Artificial te espera</h6>
                        <p class="card-text inter-regular">Al final de todo el proceso de la plataforma, te garantizamos la entrega de un modelo funcional
                                                            e integrable a tus desarrollos </p>
                        <p class="card-text inter-regular">La inteligencia artificial es un canvas en blanco, esperando a que diseñes sus habilidades en 
                                                            base a lo que necesitas cuando lo necesites.</p>
                        <p class="card-text inter-regular">Si te interesa saber haz click a continuación para poder Registrarte o para Iniciar Sesión dentro
                                                            de nuestra plataforma y empezar a experimentar con las herramientas que tenemos preparadas para ti</p>                                   
                        
                        <button type="button" class="btn btn-primary">Registrarme</button>
                    </div>
                </div>
                <div class="imgHolder" id="img2" style="width: 500px; height: 500px;"></div>
            </div>                
        </div>


        <footer class="bg-body-tertiary text-center">
            <!-- Grid container -->
            <div class="container p-4 pb-0">
                <!-- Section: Social media -->
                <section class="mb-4">
                <!-- Facebook -->
                <a
                data-mdb-ripple-init
                    class="btn text-white btn-floating m-1"
                    style="background-color: #3b5998;"
                    href="#!"
                    role="button"
                    ><i class="fab fa-facebook-f"></i
                ></a>

                <!-- Twitter -->
                <a
                    data-mdb-ripple-init
                    class="btn text-white btn-floating m-1"
                    style="background-color: #55acee;"
                    href="#!"
                    role="button"
                    ><i class="fab fa-twitter"></i
                ></a>

                <!-- Google -->
                <a
                    data-mdb-ripple-init
                    class="btn text-white btn-floating m-1"
                    style="background-color: #dd4b39;"
                    href="#!"
                    role="button"
                    ><i class="fab fa-google"></i
                ></a>

                <!-- Instagram -->
                <a
                    data-mdb-ripple-init
                    class="btn text-white btn-floating m-1"
                    style="background-color: #ac2bac;"
                    href="#!"
                    role="button"
                    ><i class="fab fa-instagram"></i
                ></a>

                <!-- Linkedin -->
                <a
                    data-mdb-ripple-init
                    class="btn text-white btn-floating m-1"
                    style="background-color: #0082ca;"
                    href="#!"
                    role="button"
                    ><i class="fab fa-linkedin-in"></i
                ></a>
                <!-- Github -->
                <a
                    data-mdb-ripple-init
                    class="btn text-white btn-floating m-1"
                    style="background-color: #333333;"
                    href="#!"
                    role="button"
                    ><i class="fab fa-github"></i
                ></a>
                </section>
                <!-- Section: Social media -->
            </div>
            <!-- Grid container -->

            <!-- Copyright -->
            <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.05);">
                © 2025 PAAP:
                <a class="text-body" href="#">PAAP.com</a>
            </div>
            <!-- Copyright -->
        </footer>

        <script scr="js/main.js"></script>
        <script src="resources/bootstrap/js/bootstrap.min.js"></script>

        <script scr="js/index.js"></script>
    </body>
</html>

