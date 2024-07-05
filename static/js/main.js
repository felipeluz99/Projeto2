function atualizarDados() {
  fetch('/dados-atualizados')
    .then(response => response.json())
    .then(data => {
      //console.log(data.estado[1]["temperatura"])
      try {
        if (data.previsao) {
          if (document.getElementById('cidade')) {
            document.getElementById('cidade').textContent = data.previsao.cidade;
          }
          if (document.getElementById('data')) {
            document.getElementById('data').textContent = data.previsao.data;
          }
          if (document.getElementById('temp-atual')) {
            document.getElementById('temp-atual').textContent = `${data.previsao.temp_atual} °C`;
          }
          if (document.getElementById('temp-max')) {
            document.getElementById('temp-max').textContent = `Máx ${data.previsao.temp_max} °C`;
          }
          if (document.getElementById('temp-min')) {
            document.getElementById('temp-min').textContent = `Mín ${data.previsao.temp_min} °C`;
          }

          if (document.getElementById('temp_interna')) {
            document.getElementById('temp_interna').textContent = ` ${data.estado[1]["temperatura"]} °C`;
          }
          if (document.getElementById('umidade')) {
            document.getElementById('umidade').textContent = `${data.estado[2]["umidade"]}%`;
          }
          if (document.getElementById('tipo-tempo-img')) {
            let imgSrc = '/static/pics/tempo_aberto.png';
            if (data.previsao.tipo_tempo === 'Cloudy') {
              imgSrc = '/static/pics/tempo_nublado.png';
            } else if (data.previsao.tipo_tempo === 'Rain') {
              imgSrc = '/static/pics/tempo_chuvoso.png';
            }
            document.getElementById('tipo-tempo-img').src = imgSrc;
          }
        }

        if (data.estado) {
         // const luzes = data.estado[0].luzes[0];
         // for (const luz in luzes) {
           // if (document.getElementById(luz)) {
          //    document.getElementById(luz).textContent = luzes[luz];
        //    }
        //  }

          const modo = data.estado[3].modo;
          if (document.getElementById('modo')) {
            document.getElementById('modo').textContent = modo;
          }

          const temperatura = data.estado[0]["ar"][0]["temperatura"];
          if (document.getElementById('temperatura')) {
            document.getElementById('temperatura').textContent = `${temperatura} °C`;
          }
          var modo_ar = data.estado[0]["ar"][0]["modo"];
          if(document.getElementById(modo_ar)){
             document.getElementById(modo_ar).click() = true;
          }
          const janela = data.estado[2].janela;
          if (document.getElementById('janela')) {
            document.getElementById('janela').textContent = janela;
          }
        }
      } catch (error) {
        console.error('Erro ao atualizar dados:', error);
      }
    })
    .catch(error => {
      console.error('Erro ao buscar dados:', error);
    });
}

setInterval(atualizarDados, 5000);


window.onload = atualizarDados;
