<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <title>IA</title>

    <link rel="stylesheet" href="css/dashboard.css">
    <link rel="stylesheet" href="css/ia.css">
    <!-- Custom fonts for this template-->
    <link href="js/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">

    <!-- Custom styles for this template-->
    <link href="css/sb-admin-2.min.css" rel="stylesheet">

</head>

<body id="page-top">

    <!-- Page Wrapper -->
    <div id="wrapper">

        <!-- Sidebar -->
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion custom-nav" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <a class="sidebar-brand d-flex align-items-center justify-content-center" href="#">
                <img src="resources/img/logotipoColor.png" class="img-fluid" id="logoDash" alt="Responsive logo">
                <div class="sidebar-brand-text mx-3"  style="font-family: 'Post No Bills Jaffna SemiBold', sans-serif; font-size: 1.8rem; color: #2E3EA5;">
                    PAAP
                </div>
                <div class="text-center d-none d-md-inline mt-3">
                    <button class="border-0" id="sidebarToggle"></button>
                </div>
            </a>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Heading -->
            <div class="sidebar-heading mt-4 opacity-50">
                MENU
            </div>

            <!-- Nav Item - Charts -->
            <li class="nav-item ml-2">
                <a class="nav-link" href="dashboard.php">
                    <i class="fas fa-fw fa-chart-area"></i>
                    <span>Dashboard</span></a>
            </li>

            <!-- Nav Item - Entrenamiento -->
            <li class="nav-item ml-2">
                <a class="nav-link" href="#">
                    <i class="fas fa-fw fa-table"></i>
                    <span>Entrenamiento</span></a>
            </li>

             <!-- Nav Item - Tables -->
            <li class="nav-item ml-2">
                <a class="nav-link" href="resources.php">
                    <i class="fas fa-book"></i>
                    <span>Recursos</span></a>
            </li>

            <!-- Heading -->
            <div class="sidebar-heading mt-5">
                OTHER
            </div>

            <!-- Nav Item - Ajustes -->
            <li class="nav-item">       
                <a class="nav-link ml-2">
                    <i class="fas fa-fw fa-cog"></i>
                    <span>Ajustes</span>
                </a>
            </li>
            
            <!-- Nav Item - Pagos -->
            <li class="nav-item">
                <a class="nav-link pl-5 pl-1 especial" href="payment.php">
                    <i class="fas fa-solid fa-wallet"></i>
                    <span>Pagos</span></a>
            </li>

             <!-- Nav Item - Cuenta -->
            <li class="nav-item">
                <a class="nav-link pl-5 pl-1 especial" href="account.php">
                    <i class="fas fa-solid fa-user"></i>
                    <span>Cuenta</span></a>
            </li>
             
            <!-- Nav Item - Manual -->
            <li class="nav-item ml-2">
                <a class="nav-link" href="manual.php">
                    <i class="fas fa-solid fa-info"></i>
                    <span>Manual</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider d-none d-md-block mt-5">
            <hr class="sidebar-divider d-none d-md-block mt-5">
            <hr class="sidebar-divider d-none d-md-block mt-5">
            <hr class="sidebar-divider d-md-block mt-5" style="border-top: 3px solid #bbb;">

            <!-- Nav Item - Salir -->
            <li class="nav-item ml-2">
                <btn class="nav-link" id="btnSalir">
                    <span>Cerrar Sesión</span></btn>
            </li>

            <!-- Sidebar Toggler (Sidebar) -->

        </ul>
        <!-- End of Sidebar -->

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">

            <!-- Main Content -->
            <div id="content">

                <!-- Begin Page Content -->
                <div class="container-fluid">

                    <!-- Page Heading -->
                     <!--<h1 class="h3 mb-4 text-gray-800 mt-3">placeholder algo algo sjdiasd</h1> -->
                    <div class="container mt-5"  id="infoSet">
                        <div class="row justify-content-md-end">  

                            <div class="col-md-auto pl-5">
                                <span style="color: #082431; font-weight: 500; font-size: 1.2rem; ">Modelo</span> 
                            </div>
                            <div class="col-md-auto">
                                <input type="text" name="modelName" id="modelName" placeholder="placeholderName">
                            </div>
                            <div class="col">
                            </div>
                        </div>   
                    </div>

                    <!-- Alert para cerrar sesión -->
                    <dialog id="dialog">
                        <p>¿Está seguro de querer cerrar sesión?</p>
                        <button type="button" class="btn btn-outline-dark btn-sm" id="optAccept">Aceptar</button>
                        <button type="button" class="btn btn-outline-dark btn-sm" id="optCancel">Cancelar</button>
                    </dialog>

                    <div class="container mt-5">
                        <div class="row">
                            <div class="col text-center main">

                                <div class="card">
                                    <h5 class="header pt-3 pb-1">Subir Archivo de Entrenamiento</h5>
                                    <div class="card-body-file pt-3 dropZone">
                                        <i class='fas fa-cloud-upload-alt pb-5' style="font-size: 3.5rem; color:#483EA8"></i>
                                        <h5 class="card-title">Arrastra, suelta archivos o <a href="" id="linknav">Navega</a></h5>
                                        <p class="card-text">Extensión de Formato Aceptada: CSV</p>
                                    </div>


                                    <main>

                                    </main>

                                    <div class="alert alert-light pt-4" role="alert">
                                        <input type="file" name="file" id="file" accept=".csv"/>
                                        <span id="fileInfo">No se ha seleccionado ningun archivo</span>
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <form action="" id="selectionAlgorithm">
                                    <div class="form-group">
                                        <label for="selectAlgorithm" class="montserrat">ALGORITMO</label>
                                        <select class="form-control" id="selectAlgorithm" onchange="showHyper()" required>
                                            <option value="">Forma de Entrenamiento</option>
                                            <option value="arbolDesicion">Arboles de Decisión</option>
                                            <option value="kNeighbors">K-Nearest Neighbors</option>
                                            <option value="randomForest">Random Forest</option>
                                        </select>
                                        
                                        <div class="ml-5 mt-3">
                                            <input class="form-check-input" type="radio" name="algoritmoType" id="typeRegresion" required>
                                            <label class="form-check-label mr-5" for="flexCheckDefault">
                                                Regresión
                                            </label>
                                            
                                            <input class="form-check-input" type="radio" name="algoritmoType" id="typeClasificación">
                                            <label class="form-check-label" for="flexCheckDefault">
                                                Clasificación
                                            </label>
                                        </div>
                                    </div> 
                                </form>
                                <button type="submit" form="selectionAlgorithm" class="btn btn-outline-primary" style="width: 100%;"> <span>Guardar Configuración</span> </button>
                            </div>
                        </div>
                    </div>

                    <div class="container hiper hidden mt-4" id="arbolDesicion">
                        <form action="">
                        <div class="row">
                            <div class="col">
                                <div class="card pr-3">
                                    <h5 class="header" style="font-size: 1rem;">Criterio</h5>
                                    <div class="card-body pt-1">

                                    <input class="form-check-input" type="radio" name="criterioRadio" id="entropyRadio">
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Entropia
                                    </label>
                                    <br>
                                    <input class="form-check-input" type="radio" name="criterioRadio" id="giniRadio" checked>
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Indice Gini (Default)
                                    </label>

                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Profundida Máxima (<span id="nodosValue">Nodos</span>)</h5>
                                    <div class="card-body pt-3">
                                        <span>1</span>
                                        <input type="range" class="form-range" id="nodosRange" min="1" max="100">
                                        <span>100</span>
                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Máximo de nodos hoja <span id="max-hojasValue"></span></h5>
                                    <div class="card-body">
                                        <span>2</span>
                                        <input type="range" class="form-range" id="max-hojasRange" min="2" max="500">
                                        <span>500</span>
                                    </div>
                                </div>
                            
                            </div>

                            <div class="col">
                                <div class="card pr-4">
                                    <h5 class="header" style="font-size: 1rem;">Mínimo de Muestras para dividir un Nodo <span id="divisorValue"></span></h5>
                                    <div class="card-body">
                                        <span>2</span>
                                        <input type="range" class="form-range" id="divisorRange" min="2" max="50">
                                        <span>50</span>
                                    </div>
                                </div>

                                <div class="card pr-4 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Mínimo de Muestras en un Nodo Hoja <span id="hojasValue"></span></h5>
                                    <div class="card-body">
                                        <span>1</span>
                                        <input type="range" class="form-range" id="hojasRange" min="1" max="50">
                                        <span>50</span>
                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Reducción mínima de impureza para dividir <span id="reduccionValue"></span></h5>
                                    <div class="card-body">
                                        <span>0</span>
                                        <input type="range" class="form-range" id="reduccionRange" min="0" max="0.1" value="0.05" step="0.001">
                                        <span>0.1</span>
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <div class="card">
                                    <h5 class="header" style="font-size: 1rem;">Semilla para reproducibilidad</h5>
                                    <div class="card-body pt-1">

                                    <input class="form-check-input" type="radio" value="" name="semillaRadio" id="semillaRadio">
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Mejor
                                    </label>
                                    <br>
                                    <input class="form-check-input" type="radio" value="" name="semillaRadio" id="aleatorioRadio" checked>
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Aleatorio
                                    </label>

                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Parámetro de poda <br>costo-complejidad <span id="ccpValue"></span></h5>
                                    <div class="card-body">
                                        <span>0</span>
                                        <input type="range" class="form-range" id="ccpRange" min="0" max="0.1" value="0.05" step="0.001">
                                        <span>0.1</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </form>
                    </div>

                    <div class="container hiper hidden mt-4" id="kNeighbors">
                        <form action="">
                        <div class="row">
                            <div class="col">
                                <div class="card pr-3">
                                    <h5 class="header" style="font-size: 1rem;">Criterio</h5>
                                    <div class="card-body pt-1">

                                    <input class="form-check-input" type="radio" name="criterioRadio" id="entropyRadio-KNN">
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Entropia
                                    </label>
                                    <br>
                                    <input class="form-check-input" type="radio" name="criterioRadio" id="giniRadio-KNN" checked>
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Indice Gini (Default)
                                    </label>

                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Profundida Máxima (<span id="nodosValue-KNN">Nodos</span>)</h5>
                                    <div class="card-body pt-3">
                                        <span>1</span>
                                        <input type="range" class="form-range" id="nodosRange-KNN" min="1" max="100">
                                        <span>100</span>
                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Máximo de nodos hoja <span id="max-hojasValue-KNN"></span></h5>
                                    <div class="card-body">
                                        <span>2</span>
                                        <input type="range" class="form-range" id="max-hojasRange-KNN" min="2" max="500" step="1">
                                        <span>500</span>
                                    </div>
                                </div>
                            
                            </div>

                            <div class="col">
                                <div class="card pr-4">
                                    <h5 class="header" style="font-size: 1rem;">Mínimo de Muestras para dividir un Nodo <span id="divisorValue-KNN"></span></h5>
                                    <div class="card-body">
                                        <span>2</span>
                                        <input type="range" class="form-range" id="divisorRange-KNN" min="2" max="50">
                                        <span>50</span>
                                    </div>
                                </div>

                                <div class="card pr-4 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Mínimo de Muestras en un Nodo Hoja <span id="hojasValue-KNN"></span></h5>
                                    <div class="card-body">
                                        <span>1</span>
                                        <input type="range" class="form-range" id="hojasRange-KNN" min="1" max="50">
                                        <span>50</span>
                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Reducción mínima de impureza para dividir <span id="reduccionValue-KNN"></span></h5>
                                    <div class="card-body">
                                        <span>0</span>
                                        <input type="range" class="form-range" id="reduccionRange-KNN" min="0" max="0.1" value="0.05" step="0.001">
                                        <span>0.1</span>
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <div class="card">
                                    <h5 class="header" style="font-size: 1rem;">Semilla para reproducibilidad</h5>
                                    <div class="card-body pt-1">

                                    <input class="form-check-input" type="radio" value="" name="semillaRadio" id="semillaRadio-KNN">
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Mejor
                                    </label>
                                    <br>
                                    <input class="form-check-input" type="radio" value="" name="semillaRadio" id="aleatorioRadio-KNN" checked>
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Aleatorio
                                    </label>

                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Parámetro de poda <br>costo-complejidad <span id="ccpValue-KNN"></span></h5>
                                    <div class="card-body">
                                        <span>0</span>
                                        <input type="range" class="form-range" id="ccpRange-KNN" min="0" max="0.1" value="0.05" step="0.001">
                                        <span>0.1</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </form>
                    </div>

                    <div class="container hiper hidden mt-4" id="randomForest">
                        <form action="">
                        <div class="row">
                            <div class="col">
                                <div class="card pr-3">
                                    <h5 class="header" style="font-size: 1rem;">Criterio</h5>
                                    <div class="card-body pt-1">

                                    <input class="form-check-input" type="radio" name="criterioRadio" value="" id="entropyRadio-RF">
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Entropia
                                    </label>
                                    <br>
                                    <input class="form-check-input" type="radio" name="criterioRadio" value="" id="giniRadio-RF" checked>
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Indice Gini (Default)
                                    </label>

                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Profundida Máxima (<span id="nodosValue-RF">Nodos</span>)</h5>
                                    <div class="card-body pt-3">
                                        <span>1</span>
                                        <input type="range" class="form-range" id="nodosRange-RF" min="1" max="100">
                                        <span>100</span>
                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Máximo de nodos hoja <span id="max-hojasValue-RF"></span></h5>
                                    <div class="card-body">
                                        <span>2</span>
                                        <input type="range" class="form-range" id="max-hojasRange-RF" min="2" max="500">
                                        <span>500</span>
                                    </div>
                                </div>
                            
                            </div>

                            <div class="col">
                                <div class="card pr-4">
                                    <h5 class="header" style="font-size: 1rem;">Mínimo de Muestras para dividir un Nodo <span id="divisorValue-RF"></span></h5>
                                    <div class="card-body">
                                        <span>2</span>
                                        <input type="range" class="form-range" id="divisorRange-RF" min="2" max="50">
                                        <span>50</span>
                                    </div>
                                </div>

                                <div class="card pr-4 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Mínimo de Muestras en un Nodo Hoja <span id="hojasValue-RF"></span></h5>
                                    <div class="card-body">
                                        <span>1</span>
                                        <input type="range" class="form-range" id="hojasRange-RF" min="1" max="50">
                                        <span>50</span>
                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Reducción mínima de impureza para dividir <span id="reduccionValue-RF"></span></h5>
                                    <div class="card-body">
                                        <span>0</span>
                                        <input type="range" class="form-range" id="reduccionRange-RF" min="0" max="0.1" value="0.05" step="0.001">
                                        <span>0.1</span>
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <div class="card">
                                    <h5 class="header" style="font-size: 1rem;">Semilla para reproducibilidad</h5>
                                    <div class="card-body pt-1">

                                    <input class="form-check-input" type="radio" value="" name="semillaRadio" id="semillaRadio-RF">
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Mejor
                                    </label>
                                    <br>
                                    <input class="form-check-input"type="radio" value="" name="semillaRadio" id="aleatorioRadio-RF" checked>
                                    <label class="form-check-label" for="flexCheckDefault">
                                        Aleatorio
                                    </label>

                                    </div>
                                </div>

                                <div class="card pr-3 mt-4">
                                    <h5 class="header" style="font-size: 1rem;">Parámetro de poda <br>costo-complejidad <span id="ccpValue-RF"></span></h5>
                                    <div class="card-body">
                                        <span>0</span>
                                        <input type="range" class="form-range" id="ccpRange-RF" min="0" max="0.1" value="0.05" step="0.001">
                                        <span>0.1</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </form>
                    </div>


                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->


    <!-- Bootstrap core JavaScript-->
    <script src="js/vendor/jquery/jquery.min.js"></script>
    <script src="js/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="js/vendor/jquery-easing/jquery.easing.min.js"></script>

    <script src="js/dashboard.min.js"></script>
    <script src="js/ia.js"></script>


</body>

</html>