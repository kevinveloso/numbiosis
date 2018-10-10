//Função de Newton para Sistemas Não-Lineares
//
function newton(sistema, x0, e1, e2) {

    var F = Array(sistema.length);
    
    var Jacobiana = [];
    for(var i=0; i<sistema.length; i++) {
        Jacobiana[i] = new Array(2);
    };

    //Cálculo por linhas da Jacobiana
    var i = 0;
    sistema.forEach(linha => {
        Jacobiana[i][0] = math.derivative(linha, 'x', {simplify: false}).toString();
        Jacobiana[i][1] = math.derivative(linha, 'y', {simplify: false}).toString();
        i++;
    });

    var x = x0[0];
    var y = x0[1];

    while(true){    
        //Calcula F com valor de x0
        var j = 0;
        sistema.forEach(linha => {       
            F[j] = eval(linha);
            F[j] = F[j] * -1;
            j++;
        });

        //Criterio de parada
        var norma = 0;
        F.forEach(linha=> {
            norma = norma + (linha*linha);
        });

        if(math.sqrt(norma) < e1) {
            break;
        }

        var valorJacobiana = Jacobiana;
        j = 0;
        valorJacobiana.forEach(linha => {
            valorJacobiana[j][0] = eval(Jacobiana[j][0]);
            valorJacobiana[j][1] = eval(Jacobiana[j][1]);
            j++;
        });
        
        //mudei a chamada a função solve, pois tive que mudar a importação da biblioteca
        var xy = solve(valorJacobiana, F);
        var sx = xy[0];
        var sy = xy[1];

        var xk1 = Array(2);

        xk1[0] = x + sx;
        xk1[1] = y + sy;

        if(math.sqrt(math.pow(xk1[0] - x, 2)+math.pow(xk1[1] - y, 2)) < e2) {
            x = xk1[0];
            y = xk1[1];
            break;
        }
        

        x = xk1[0];
        y = xk1[1];
    }

    return Array(valorJacobiana, F, sx, sy, x, y);
}

//Função de Gauss Jordan
//
function gaussJordan(sistema, b) {
  // ENTRADA:.
  //var sistema = ['3x-0.1x-0.2x', '0.1x+7x-0.3x', '0.3x-0.2x+10x'];
  //var b = [7.85, -19.3, 71.4];

  //Matriz com valores:.
  var matriz = [];
  for(var i=0; i<sistema.length; i++) {
      matriz[i] = new Array(sistema.length);
  }

  var aux = new Array(sistema.length);  //auxiliar para valores;
  var valoresFinais = new Array(sistema.length);  //auxiliar para valores x1, x2, x3;
  var baux = 0;
  var somaMatriz = 0;

  //Pegando os valores x1, x2, x3;
  var i = 0;
  sistema.forEach(linha => {
      var valor = sistema[i]
      matriz[i] = valor.split("x")
      i++;
  });

  //testanto:.
  //document.getElementById("demo").innerHTML = matriz[0];
  //document.getElementById("demo1").innerHTML = matriz[1];
  //document.getElementById("demo2").innerHTML = matriz[2];

  //calculando
  for(var i = 0; i < sistema.length-1; i++){
    pivor = matriz[i][i]; //pivor

    //Abaixo do pivor;
    for(var j = i+1; j < sistema.length; j++){
        var x = matriz[j][i] / matriz[i][i];

        //mutiplicando toda a linha do pivor;
        for(var k = 0; k < sistema.length; k++){
            aux[k] = matriz[i][k] * x;
        }

        //subtraindo a linha do pivor com a linha que se deseja zera os elementos:.
        for(var k = 0; k < sistema.length; k++){
            matriz[j][k] = matriz[j][k] - aux[k];
        }

        //alterando os valores de b:.
        baux = b[i] * x;
        b[j] = b[j] - baux;
    }
  }

  //Calculando os valores e modificando as matrizes:.
  for(var i = sistema.length-1; i > -1; i--){ //lendo matriz de trás para frente;

    //Somar todos os elementos para futuramente isolar o x desejado;
    somaMatriz = 0;
    for (var j = i; j < sistema.length-1; j++) {
      somaMatriz = somaMatriz + matriz[i][j+1];
    }

    //calculando o valor de X;(isolando o X);
    baux = (b[i] - somaMatriz) / matriz[i][i];
    //guardando o valor de X na matriz:.
    b[i] = baux;

    //atualizando valores da matriz realizando as multiplicações;
    for (var j = i; j > 0; j--) {
      matriz[j-1][i] = matriz[j-1][i] * baux;
    }
  }

  return b;

  //PRINTANDO OS VALORES DE X ENCONTRADOS:.
  //document.getElementById("demo").innerHTML =  b[0];  //x1
  //document.getElementById("demo1").innerHTML = b[1];  //x2
  //document.getElementById("demo2").innerHTML = b[2];  //x3
}