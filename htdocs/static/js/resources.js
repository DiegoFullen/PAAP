const $d = document;

const $monitor = $d.getElementById("videoMonitor");
const $videoSetup1 = $d.getElementById("optionVideoDefault");
const $videoSetup2 = $d.getElementById("optionVideo2");
const $videoSetup3 = $d.getElementById("optionVideo3");

$videoSetup1.addEventListener('click', () => {
    $monitor.src = "https://www.youtube.com/embed/u31qwQUeGuM?si=KvOhrHtuXCvr-Pz4";
  });

$videoSetup2.addEventListener('click', () => {
    $monitor.src = "https://www.youtube.com/embed/4bHUsy74Fss?si=QdUx9Frwp52JGX7z";
  });

$videoSetup3.addEventListener('click', () => {
    $monitor.src = "https://www.youtube.com/embed/NSAOrGb9orM?si=QI7OertcpN7lK0Hw";
  });
