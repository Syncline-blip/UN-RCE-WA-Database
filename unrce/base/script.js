// script.js

document.addEventListener("DOMContentLoaded", function () {
    const hamburgerIcon = document.querySelector(".hamburger-icon");
    const sidebar = document.querySelector(".sidebar");

    // Toggle sidebar on hamburger icon click
    hamburgerIcon.addEventListener("click", function () {
        sidebar.classList.toggle("show-sidebar");
    });
});
