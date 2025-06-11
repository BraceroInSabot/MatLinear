var produto = []

function atualizarTabela() {
    // Limpa o conteúdo atual da tabela e adiciona os novos produtos
    const tbody = document.querySelector(".tabela tbody");
    tbody.innerHTML = "";

    produto.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item['Produto']}</td>
            <td>${item['Preço']}</td>
            <td>${item['Quant. Min.']}</td>
            <td>${item['Quant. Max.']}</td>
        `;
        tbody.appendChild(tr);
    });

    console.log(produto);
}

const adicionarProduto = () => {
    // Obtém os valores dos campos de entrada e adiciona ao array produto
    const nomeProduto = document.getElementById("produto").value;
    const precoProduto = document.getElementById("preco").value;
    const qtdMinimo = document.getElementById("minimo").value;
    const qtdMaximo = document.getElementById("maximo").value;

    produto.push({'Produto': nomeProduto, 'Preço': precoProduto, 'Quant. Min.': qtdMinimo, 'Quant. Max.': qtdMaximo}); 

    atualizarTabela(); 
}

document.getElementById("inputImportarDados").addEventListener("change", function(event) {
    // Envia um arquivo selecionado para o servidor, processa a resposta e atualiza a tabela
    const file = event.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append("arquivo", file);
    temp_produtos = []

    try{
        
        const val_produtos = fetch("http://localhost:8000/api/v1/arquivo/importar/", { 
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert("Arquivo enviado com sucesso!");
            // Faça algo com a resposta, se necessário
            produto = []
            produto.push(data)
            produto = produto[0]
            atualizarTabela();
        })
    } catch (error) {
        alert("Erro ao processar o arquivo.");
    }

    console.log(produto);
});

const limparTabela = () => {
    // Limpa o array produto e a tabela
    document.getElementById("modalConfirmacao").style.display = "flex";
    document.getElementById("btnSim").onclick = function() {
        // Limpa a tabela e o array
        produto = [];
        atualizarTabela();
        document.getElementById("modalConfirmacao").style.display = "none";
    };

    document.getElementById("btnNao").onclick = function() {
        // Apenas fecha o modal
        document.getElementById("modalConfirmacao").style.display = "none";
    };
};

const exportarTabela = () => {
    // Converte o array produto em um formato CSV
    if (produto.length == 0) {
        alert("Tabela vazia!");
        return;
    }

    try {
    fetch("http://localhost:8000/api/v1/arquivo/exportar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(produto) // ou os dados que você quer exportar
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "exportado.xlsx";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    });
    } catch (error) {
        alert("Erro ao exportar a tabela.");
    }
};

function coletarDadosInputs() {
    const linhas = document.querySelectorAll("#inputsContainer .input-row");
    const dados = [];

    linhas.forEach(linha => {
        const selects = linha.querySelectorAll("select");
        const input = linha.querySelector("input");

        const campo = selects[0].value;
        const operador = selects[1].value;
        const valor = input.value;

        dados.push({ campo, operador, valor });
    });

    return dados;
}

// Adiciona as restrições
// document.getElementById("salvarTabela").onclick = () => {
//     const dados = coletarDadosInputs();

//     fetch("https://sua-api.com/filtro", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify(dados)
//     })
//     .then(response => response.json())
//     .then(result => {
//         console.log("Resposta da API:", result);
//     })
//     .catch(error => {
//         console.error("Erro ao enviar:", error);
//     });
// };

const salvarTabela = (modo) => {
    if (produto.length == 0) {
        alert("Tabela vazia!");
        return;
    }

    const dados = {
        "tabela": produto,
        "restricao": coletarDadosInputs(),
        "modo": modo
    };

    fetch("http://localhost:8000/api/v1/arquivo/inserir/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao enviar dados.");
        }
        return response.json();
    })
    .then(data => {
        console.log("Sucesso:", data);
        window.location.href = "http://127.0.0.1:5501/template/relatorios.html";
    })
    .catch(error => {
        console.error("Erro:", error);
    });

    window.location.href = "http://127.0.0.1:5501/template/relatorios.html";
};

const btnExportar  = document.getElementById("btnExportar");
btnExportar.addEventListener("click", exportarTabela);

const limparTabelaBotao = document.getElementById("limparTabela");
limparTabelaBotao.addEventListener("click", limparTabela);

const adicionarProdutoBotao = document.getElementById("adicionarProduto");
adicionarProdutoBotao.addEventListener("click", adicionarProduto);

document.querySelectorAll("#salvarTabela").forEach(btn => {
    btn.addEventListener("click", function() {
        const modo = this.getAttribute("data-modo") === "true";
        salvarTabela(modo);
    });
});

document.getElementById("btnImportarDados").addEventListener("click", function() {
    document.getElementById("inputImportarDados").click();
});
