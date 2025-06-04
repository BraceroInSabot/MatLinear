const modal = document.getElementById("myModal");
const openBtn = document.getElementById("openModal");
const closeBtn = document.getElementById("closeModal");
const addRowBtn = document.getElementById("addRow");
const inputsContainer = document.getElementById("inputsContainer");

// Abre e fecha o modal
openBtn.onclick = () => modal.style.display = "block";
closeBtn.onclick = () => modal.style.display = "none";
window.onclick = (e) => { if (e.target === modal) modal.style.display = "none"; };

// Cria elemento HTML de uma nova linha com botão de exclusão
function criarNovaLinha() {
    const div = document.createElement("div");
    div.className = "input-row";
    div.innerHTML = `
        <select>
            <option value="Preço">Preço</option>
            <option value="Quant. Min.">Quant. Min.</option>
            <option value="Quant. Max.">Quant. Max.</option>
            <option value="Quantidade">Quantidade</option>
            <option value="Quantidade Total">Quantidade Total</option>
            <option value="Preço Total">Preço Total</option>
        </select>
        <select>
            <option value="==">==</option>
            <option value="!=">!=</option>
            <option value=">">></option>
            <option value="<"><</option>
            <option value=">=">>=</option>
            <option value="<="><=</option>
        </select>
        <input type="text" placeholder="Valor 2" class="field-input">
        <button class="remove-btn">Excluir</button>
    `;

    // Evento para excluir esta linha
    div.querySelector(".remove-btn").onclick = () => div.remove();

    return div;
}

// Adiciona nova linha
addRowBtn.onclick = () => {
    const novaLinha = criarNovaLinha();
    inputsContainer.appendChild(novaLinha);
};

// Aplica o botão "Excluir" em linhas existentes
function configurarBotoesDeExcluir() {
    const botoes = inputsContainer.querySelectorAll(".remove-btn");
    botoes.forEach(btn => {
        btn.onclick = () => btn.parentElement.remove();
    });
}

// Inicializa os eventos nos elementos já existentes
window.onload = () => {
    configurarBotoesDeExcluir();
};
