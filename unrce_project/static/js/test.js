document.addEventListener("DOMContentLoaded", function () {
    console.log("loaded")
    // Open and Close Navbar Menu
    const navbarMenu = document.getElementById("menu");
    const burgerMenu = document.getElementById("burger");
    const bgOverlay = document.querySelector(".overlay");
  
    if (burgerMenu && bgOverlay) {
      burgerMenu.addEventListener("click", () => {
        console.log("burger loaded")
          navbarMenu.classList.add("is-active");
          bgOverlay.classList.toggle("is-active");
      });
    // Selecting elements
    const dropdownBtn = document.querySelectorAll(".dropdown-btn");
    const dropdown = document.querySelectorAll(".dropdown");
    const hamburgerBtn = document.getElementById("hamburger");
    const navMenu = document.querySelector(".menu");
    const links = document.querySelectorAll(".dropdown a");
  
    // Function to set aria-expanded attribute to false for all dropdown buttons
    function setAriaExpandedFalse() {
      dropdownBtn.forEach((btn) => btn.setAttribute("aria-expanded", "false"));
    }
  
    // Function to close all dropdown menus
    function closeDropdownMenu() {
      dropdown.forEach((drop) => {
        drop.classList.remove("active");
        drop.addEventListener("click", (e) => e.stopPropagation());
        console.log("loaded")
      });
    }
  
    // Function to toggle the hamburger menu
    function toggleHamburger() {
      navMenu.classList.toggle("show");
    }
  
    // Event listeners for dropdown buttons
    dropdownBtn.forEach((btn) => {
      btn.addEventListener("click", function (e) {
        const dropdownIndex = e.currentTarget.dataset.dropdown;
        const dropdownElement = document.getElementById(dropdownIndex);
        console.log("loaded")
        dropdownElement.classList.toggle("active");
        dropdown.forEach((drop) => {
          if (drop.id !== btn.dataset["dropdown"]) {
            drop.classList.remove("active");
          }
        });
        e.stopPropagation();
        btn.setAttribute(
          "aria-expanded",
          btn.getAttribute("aria-expanded") === "false" ? "true" : "false"
        );
      });
    });
  
    // Event listeners for dropdown links
    links.forEach((link) =>
      link.addEventListener("click", () => {
        closeDropdownMenu();
        setAriaExpandedFalse();
        toggleHamburger();
      })
    );
  
    // Event listener to close dropdowns when clicking on the document body
    document.documentElement.addEventListener("click", () => {
      closeDropdownMenu();
      setAriaExpandedFalse();
    });
  
    // Event listener to close dropdowns when the Escape key is pressed
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeDropdownMenu();
        setAriaExpandedFalse();
      }
    });
  
    // Event listener for toggling the hamburger menu
    hamburgerBtn.addEventListener("click", toggleHamburger);
  
    // Event listener for profile dropdown
    document.addEventListener('DOMContentLoaded', function () {
      const profileDropdownToggle = document.querySelector('.profile-dropdown-toggle');
      const profileDropdown = document.querySelector('.profile-dropdown');
  
      profileDropdownToggle.addEventListener('click', function (e) {
        e.stopPropagation(); // Prevent the click event from propagating to the body
        profileDropdown.classList.toggle('active');
      });
  
      // Close the dropdown when clicking outside of it
      document.body.addEventListener('click', function () {
        profileDropdown.classList.remove('active');
      });
  
      // Prevent the dropdown from closing when clicking inside it
      profileDropdown.addEventListener('click', function (e) {
        e.stopPropagation();
      });
    });
    
  }
  
      bgOverlay.addEventListener("click", () => {
          navbarMenu.classList.remove("is-active");
          bgOverlay.classList.toggle("is-active");
      });
    
  
    // Close Navbar Menu on Links Click
    document.querySelectorAll(".menu-link").forEach((link) => {
      link.addEventListener("click", () => {
          navbarMenu.classList.remove("is-active");
          bgOverlay.classList.remove("is-active");
      });
    });
  
    // Open and Close Search Bar Toggle
    const searchBlock = document.querySelector(".search-block");
    const searchToggle = document.querySelector(".search-toggle");
    const searchCancel = document.querySelector(".search-cancel");
  
    if (searchToggle && searchCancel) {
      searchToggle.addEventListener("click", () => {
          searchBlock.classList.add("is-active");
      });
  
      searchCancel.addEventListener("click", () => {
          searchBlock.classList.remove("is-active");
      });
    }
  });
  
  
  
  