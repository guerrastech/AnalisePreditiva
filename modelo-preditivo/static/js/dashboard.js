const ctx = document.getElementById("graficoUnico").getContext("2d");

let grafico = null;

function criarGrafico(tipo) {
  if (grafico) grafico.destroy();

  if (tipo === "classes") {
    grafico = new Chart(ctx, {
      type: "bar",
      data: {
        labels: window.percentualLabelsClasses,
        datasets: [{
          label: "Distribuição das classes",
          data: window.percentualDataClasses,
          backgroundColor: ["#36a2eb", "#ff6384"]
        }]
      }
    });

  } else if (tipo === "genero") {
    grafico = new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Homens", "Mulheres"],
        datasets: [{
          label: "% com renda > 50K",
          data: window.percentualGenero,
          backgroundColor: ["#3498db", "#e74c3c"]
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });

  } else if (tipo === "ocupacao") {
    grafico = new Chart(ctx, {
      type: "bar",
      data: {
        labels: window.labelsOcupacao,
        datasets: [{
          label: "% com renda > 50K por ocupação",
          data: window.percentuaisOcupacao,
          backgroundColor: "#2ecc71"
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });

  } else if (tipo === "faixaEtaria") {
    grafico = new Chart(ctx, {
      type: "bar",
      data: {
        labels: window.labelsFaixaEtaria,
        datasets: [{
          label: "% com renda > 50K por faixa etária",
          data: window.valoresFaixaEtaria,
          backgroundColor: "#9b59b6"
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });

  } else if (tipo === "escolaridade") {
    grafico = new Chart(ctx, {
      type: "bar",
      data: {
        labels: window.labelsEscolaridade,
        datasets: [{
          label: "% com renda > 50K por escolaridade",
          data: window.percentuaisEscolaridade,
          backgroundColor: "#f39c12"
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }
}

document.getElementById("select-grafico").addEventListener("change", (e) => {
  criarGrafico(e.target.value);
});

// Exibe o primeiro gráfico ao carregar a página
criarGrafico("classes");

// Botão mostrar/ocultar tabela
document.getElementById("btn-mostrar-tabela").addEventListener("click", () => {
  const tabela = document.getElementById("tabela-container");
  tabela.style.display = tabela.style.display === "none" ? "block" : "none";
});
