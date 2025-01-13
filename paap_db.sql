-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-01-2025 a las 18:08:53
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `paap_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add model', 7, 'add_model'),
(26, 'Can change model', 7, 'change_model'),
(27, 'Can delete model', 7, 'delete_model'),
(28, 'Can view model', 7, 'view_model'),
(29, 'Can add user', 8, 'add_user'),
(30, 'Can change user', 8, 'change_user'),
(31, 'Can delete user', 8, 'delete_user'),
(32, 'Can view user', 8, 'view_user'),
(33, 'Can add plan', 9, 'add_plan'),
(34, 'Can change plan', 9, 'change_plan'),
(35, 'Can delete plan', 9, 'delete_plan'),
(36, 'Can view plan', 9, 'view_plan'),
(37, 'Can add dataset', 10, 'add_dataset'),
(38, 'Can change dataset', 10, 'change_dataset'),
(39, 'Can delete dataset', 10, 'delete_dataset'),
(40, 'Can view dataset', 10, 'view_dataset');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(10, 'gestion_usuarios', 'dataset'),
(7, 'gestion_usuarios', 'model'),
(9, 'gestion_usuarios', 'plan'),
(8, 'gestion_usuarios', 'user'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-11-20 04:21:46.644203'),
(2, 'auth', '0001_initial', '2024-11-20 04:22:05.528700'),
(3, 'admin', '0001_initial', '2024-11-20 04:22:08.363425'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-11-20 04:22:08.449804'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-11-20 04:22:08.516727'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-11-20 04:22:09.656888'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-11-20 04:22:12.304253'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-11-20 04:22:12.529750'),
(9, 'auth', '0004_alter_user_username_opts', '2024-11-20 04:22:12.605413'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-11-20 04:22:13.613868'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-11-20 04:22:13.678530'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-11-20 04:22:13.752245'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-11-20 04:22:13.923926'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-11-20 04:22:14.122187'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-11-20 04:22:14.349006'),
(16, 'auth', '0011_update_proxy_permissions', '2024-11-20 04:22:14.475794'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-11-20 04:22:14.831824'),
(18, 'gestion_usuarios', '0001_initial', '2024-11-20 04:22:20.194843'),
(19, 'sessions', '0001_initial', '2024-11-20 04:22:21.297287');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2ipem5ys615ps2jqt08omymdbr36elh0', '.eJyrVkrNTczMUbJSKigqTU1KdIBQesn5uUo6SqXFqUV5ibmpcGmgGDq_ILG4uDy_KAVZDGxmfFFqcn5ZahFcwgjV8LTMouKSnMTiEnQTi4H68lIwZWoBWyA8eQ:1tVghF:0iKb65m3380O6DUTLL5eo9JnhBvhknmA06UEA7OoZ3Y', '2025-01-23 00:46:49.546944'),
('oagj3te1iovgabzsvvmrhds0q5knzx8c', '.eJyrVkrNTczMUbJSUtJRKi1OLcpLzE2F8BAssJL4otTk_LLUIohQWmZRcUlOYnEJQlUxUD4vBVWsILG4uDy_KAXEqwUAOB0idg:1tVeKK:gd4yfhd76eEOqlhk8la8RAmD2o3jfqmFA2i-iGBd97U', '2025-01-22 22:15:00.382352'),
('sv8rlrz9zvzr7q7jj011woez0xshrwpm', '.eJyrVkrNTczMUbJSUtJRKi1OLcpLzE2F8BCsgsTi4vL8ohQID6whvig1Ob8stQgilJZZVFySk1hcgtBTDJTPS0EVK8hJzFOyilYKKErNzSzNVYqtBQDsLiim:1tW0wi:OQiPUo22mHrAodU5ChtLVs4N_Xdsokk7rw8fAPSi0ms', '2025-01-23 22:24:08.586993'),
('v6nxcv0bpo7etvjbqgj0m06ydjnw1xfu', '.eJyrVkrNTczMUbJSKigqTU1KdIBQesn5uUo6SqXFqUV5ibmpcOl4uIiOEooEkF-QWFxcnl-UgiwGNjy-KDU5vyy1CIclaZlFxSU5icUlKAY6AmWKgfryUjCknJRqASPQQIk:1tVYU2:HjerYHbzSDJPzcdG8NAYIroBXIrQIWhjJ7DTCZlC9dg', '2025-01-22 16:00:38.075968'),
('xwdax5selipi0kgst33ejiga1q8rny4p', '.eJyrVkrNTczMUbJSKigqTU1KdIBQesn5uUo6SqXFqUV5ibmpcOl4uIiOEooEkF-QWFxcnl-UgiwGNjy-KDU5vyy1CIclaZlFxSU5icUlKAY6AmWKgfryUjCknJRqASPQQIk:1tVYh1:hlULzObuWUzcju5OX6tGi9oQdRhnIrQhaFhWGx6HRNo', '2025-01-22 16:14:03.279303');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestion_usuarios_dataset`
--

CREATE TABLE `gestion_usuarios_dataset` (
  `id_dataset` int(11) NOT NULL,
  `upload_date` varchar(15) NOT NULL,
  `name_dataset` varchar(50) NOT NULL,
  `size` decimal(20,6) NOT NULL,
  `email_id` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestion_usuarios_model`
--

CREATE TABLE `gestion_usuarios_model` (
  `id_model` int(11) NOT NULL,
  `id_dataset` int(11) NOT NULL,
  `start_date` varchar(15) NOT NULL,
  `finish_date` varchar(15) NOT NULL,
  `name` varchar(50) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestion_usuarios_plan`
--

CREATE TABLE `gestion_usuarios_plan` (
  `id` int(20) NOT NULL,
  `hours` decimal(5,2) NOT NULL,
  `type_plan` varchar(20) NOT NULL,
  `email_id` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestion_usuarios_user`
--

CREATE TABLE `gestion_usuarios_user` (
  `email` varchar(254) NOT NULL,
  `id_user` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email_recover` varchar(254) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `firstlastname` varchar(50) DEFAULT NULL,
  `secondlastname` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestion_usuarios_user`
--

INSERT INTO `gestion_usuarios_user` (`email`, `id_user`, `username`, `name`, `password`, `email_recover`, `status`, `firstlastname`, `secondlastname`) VALUES
('prueba@prueba.com', 1, 'HOLAWA', 'prueba', 'prueba', '', 1, 'prueba', 'prueba');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestion_usuarios_user_temporal`
--

CREATE TABLE `gestion_usuarios_user_temporal` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(150) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email_recover` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT 1,
  `firstlastname` varchar(100) NOT NULL,
  `secondlastname` varchar(100) DEFAULT NULL,
  `token` varchar(64) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestion_usuarios_user_temporal`
--

INSERT INTO `gestion_usuarios_user_temporal` (`id`, `email`, `username`, `name`, `password`, `email_recover`, `status`, `firstlastname`, `secondlastname`, `token`, `created_at`) VALUES
(25, 'a21310382@ceti.mx', 'AngeloHazielOso', 'Angel', '111', 'angelohaziel2002l@gmail.com', 1, 'Hernandez', 'Nachez', 'A2L0VDj7Z98AefgTGsRrUG2DGl3PSfQy', '2025-01-06 21:39:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hiperparametros`
--

CREATE TABLE `hiperparametros` (
  `id_dataset` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `algoritmo` varchar(20) NOT NULL,
  `tipo` tinyint(1) NOT NULL,
  `criterio` tinyint(1) NOT NULL,
  `nodosValue` int(11) NOT NULL,
  `max_hojasValue` int(11) NOT NULL,
  `divisorValue` int(11) NOT NULL,
  `hojasValue` int(11) NOT NULL,
  `reduccionValue` double NOT NULL,
  `semilla` tinyint(1) NOT NULL,
  `poda` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `gestion_usuarios_dataset`
--
ALTER TABLE `gestion_usuarios_dataset`
  ADD PRIMARY KEY (`id_dataset`),
  ADD KEY `gestion_usuarios_dat_email_id_54a2e1cb_fk_gestion_u` (`email_id`);

--
-- Indices de la tabla `gestion_usuarios_model`
--
ALTER TABLE `gestion_usuarios_model`
  ADD PRIMARY KEY (`id_model`);

--
-- Indices de la tabla `gestion_usuarios_plan`
--
ALTER TABLE `gestion_usuarios_plan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gestion_usuarios_pla_email_id_e96fd098_fk_gestion_u` (`email_id`);

--
-- Indices de la tabla `gestion_usuarios_user`
--
ALTER TABLE `gestion_usuarios_user`
  ADD PRIMARY KEY (`email`);

--
-- Indices de la tabla `gestion_usuarios_user_temporal`
--
ALTER TABLE `gestion_usuarios_user_temporal`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `gestion_usuarios_user_temporal`
--
ALTER TABLE `gestion_usuarios_user_temporal`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `gestion_usuarios_dataset`
--
ALTER TABLE `gestion_usuarios_dataset`
  ADD CONSTRAINT `gestion_usuarios_dat_email_id_54a2e1cb_fk_gestion_u` FOREIGN KEY (`email_id`) REFERENCES `gestion_usuarios_user` (`email`);

--
-- Filtros para la tabla `gestion_usuarios_plan`
--
ALTER TABLE `gestion_usuarios_plan`
  ADD CONSTRAINT `gestion_usuarios_pla_email_id_e96fd098_fk_gestion_u` FOREIGN KEY (`email_id`) REFERENCES `gestion_usuarios_user` (`email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
