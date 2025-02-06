document.addEventListener('DOMContentLoaded', function() {
    // Selecionando todos os botões de "olho"
    const toggleButtons = document.querySelectorAll('.id_senha');
    console.log("Carregou ");
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Pegando o campo de senha correspondente
            const inputField = document.getElementById(button.dataset.target);
            
            if (inputField.type === "password") {
                inputField.type = "text"; // Torna a senha visível
                button.textContent = "👁‍🗨"; // Altera para olho aberto
            } else {
                inputField.type = "password"; // Torna a senha invisível
                button.textContent = "👁"; // Altera para olho fechado
            }
        });
    });
});
