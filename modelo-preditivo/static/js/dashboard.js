document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('graficoUnico');
    if (!canvas) return;
  
    const ctx = canvas.getContext('2d');
  
    const grafico = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [{
          label: '',
          data: [],
          backgroundColor: [],
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: true, text: '' }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: value => value + '%'
            }
          }
        }
      }
    });
  
    function mostrarGraficoClasses() {
      grafico.data.labels = window.percentualLabelsClasses;
      grafico.data.datasets[0].data = window.percentualDataClasses;
      grafico.data.datasets[0].backgroundColor = ['#36A2EB', '#FF6384'];
      grafico.options.plugins.title.text = 'Distribuição das Classes Preditas';
      grafico.update();
    }
  
    function mostrarGraficoGenero() {
      grafico.data.labels = ['Homens', 'Mulheres'];
      grafico.data.datasets[0].data = window.percentualGenero;
      grafico.data.datasets[0].backgroundColor = ['#4B9CD3', '#F675A8'];
      grafico.options.plugins.title.text = 'Percentual com Renda > 50K por Gênero';
      grafico.update();
    }
  
    function mostrarGraficoOcupacao() {
      grafico.data.labels = window.labelsOcupacao;
      grafico.data.datasets[0].data = window.percentuaisOcupacao;
      grafico.data.datasets[0].backgroundColor = '#36A2EB';
      grafico.options.plugins.title.text = 'Percentual com Renda > 50K por Ocupação';
      grafico.update();
    }
  
    const tituloClasses = document.getElementById('titulo-classes');
    const tituloGenero = document.getElementById('titulo-genero');
    const tituloOcupacao = document.getElementById('titulo-ocupacao');
  
    if (tituloClasses) tituloClasses.addEventListener('mouseover', mostrarGraficoClasses);
    if (tituloGenero) tituloGenero.addEventListener('mouseover', mostrarGraficoGenero);
    if (tituloOcupacao) tituloOcupacao.addEventListener('mouseover', mostrarGraficoOcupacao);
  
    mostrarGraficoClasses();
  });
  