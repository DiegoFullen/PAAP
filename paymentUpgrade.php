<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <title>Cuenta</title>

    <link rel="stylesheet" href="css/dashboard.css">
    <link rel="stylesheet" href="css/paymentUpgrade.css">
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
                <a class="nav-link" href="">
                    <i class="fas fa-fw fa-chart-area"></i>
                    <span>Dashboard</span></a>
            </li>

            <!-- Nav Item - Entrenamiento -->
            <li class="nav-item ml-2">
                <a class="nav-link" href="ia.php">
                    <i class="fas fa-fw fa-table"></i>
                    <span>Entrenamiento</span></a>
            </li>

             <!-- Nav Item - Tables -->
            <li class="nav-item ml-2">
                <a class="nav-link" href="#">
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
                <a class="nav-link pl-5 pl-1 especial" href="#">
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
                <a class="nav-link" href="#">
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
                    <div class="container mt-5"  id="accountSet">
                        <div class="row justify-content-md">  
                            <div class="col-md-auto">
                                <span style="color: #082431; font-weight: 500; font-size: 1.2rem;" class="ml-4">Mi Perfil </span> 
                                <a href="" class="btn btn-light ml-4 disabled" role="button" aria-disabled="true">Editar</a>
                            </div>
                        </div>   

                        <div class="row ml-3 mt-4">
                            <div class="col-2">
                                <img src="resources/img/usuario.png" alt="usuarioPerfil" class="imgPlaceholder">
                            </div>
                            <div class="col-3 ml-5" style="text-align: start;">
                                <label for="userName" class="col-form-label">Nombre Usuario</label>
                                <input type="text" readonly class="form-control-plaintext" id="userName" placeholder="Usuario1234" value="Placeholder">
                            </div>
                            <div class="col-3 ml-5" style="text-align: start;">   
                                <label for="accountType" class="col-form-label">Tipo de Cuenta</label>
                                <input type="text"  readonly class="form-control-plaintext" id="accountType" placeholder="Usuario1234" value="Premium">
                            </div>
                        </div>
                    </div>

                    <dialog id="dialog">
                        <p>¿Está seguro de querer cerrar sesión?</p>
                        <button type="button" class="btn btn-outline-dark btn-sm" id="optAccept">Aceptar</button>
                        <button type="button" class="btn btn-outline-dark btn-sm" id="optCancel">Cancelar</button>
                    </dialog>

                    <div class="row mt-5 ml-5">
                        <div class="col-3">

                            <div class="card" id="paycheck">
                                <div class="card-body">
                                <div class="col">
                                    <form>
                                        <div class="form-group mb-5">
                                            <label for="selectCategory" class="montserrat">ALGORITMO</label>
                                            <select class="form-control" id="selectCategory">
                                                <option>Tipo de Cuenta</option>
                                                <option value="arbolDesicion">Integrado</option>
                                                <option value="kNeighbors">CETI</option>
                                                <option value="randomForest">Premium</option>
                                            </select>
                                        </div> 

                                        <button type="submit" form="selectionAlgorithm" class="btn btn-outline-primary" style="width: 100%;"> <span>Actualizar</span> </button>
                                    </form>
                            </div>
                                </div>
                            </div>
                        </div>

                        <div class="col">

                        </div>
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

    <!-- Custom scripts for all pages-->
     
    <script src="js/dashboard.min.js"></script>
    <script src="js/paymentUpgrade.js"></script>
</body>

</html>