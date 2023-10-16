document.addEventListener("DOMContentLoaded", function () {
  const navbarMenu = document.getElementById("menu");
  const burgerMenu = document.getElementById("burger");
  const bgOverlay = document.querySelector(".overlay");
  const dropdownBtn = document.querySelectorAll(".dropdown-btn");
  const dropdown = document.querySelectorAll(".dropdown");
  const hamburgerBtn = document.getElementById("hamburger");
  const navMenu = document.querySelector(".menu");
  const links = document.querySelectorAll(".dropdown a");
  const searchBlock = document.querySelector(".search-block");
  const searchToggle = document.querySelector(".search-toggle");
  const searchCancel = document.querySelector(".search-cancel");

  // Function to set aria-expanded attribute to false for all dropdown buttons
  function setAriaExpandedFalse() {
    dropdownBtn.forEach((btn) => btn.setAttribute("aria-expanded", "false"));
  }

  function closeDropdownMenu() {
    dropdown.forEach((drop) => {
      drop.classList.remove("active");
      drop.addEventListener("click", (e) => e.stopPropagation());
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

  // Event listener for hamburger button
  hamburgerBtn.addEventListener("click", toggleHamburger);

  // Event listener for profile dropdown
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

  // Event listener for burger menu
  if (burgerMenu && bgOverlay) {
    burgerMenu.addEventListener("click", () => {
      navbarMenu.classList.add("is-active");
      bgOverlay.classList.toggle("is-active");
    });
  }

  // Open and Close Search Bar Toggle
  if (searchToggle && searchCancel) {
    searchToggle.addEventListener("click", () => {
      searchBlock.classList.add("is-active");
    });

    searchCancel.addEventListener("click", () => {
      searchBlock.classList.remove("is-active");
    });
  }

  // Test function, debugging
  // function addNumbers(a, b) {
  //   return a + b;
  // }

  // // Call the function and display the result on the page
  // const num1 = 5;
  // const num2 = 7;
  // const sum = addNumbers(num1, num2);

  // // Display the result in the "result" span element
  // document.getElementById("result").textContent = sum;
});
