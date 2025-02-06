document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".toggle-password").forEach(button => {
      button.addEventListener("click", function () {
          let input = document.getElementById(this.dataset.target);
          if (input.type === "password") {
              input.type = "text";
              this.textContent = "👁‍🗨";  // Ícone de olho aberto
          } else {
              input.type = "password";
              this.textContent = "👁";  // Ícone de olho fechado
          }
      });
  });
});
