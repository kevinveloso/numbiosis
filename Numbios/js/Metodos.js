//So funcionava se fosse com node.js
// load math.js
//const math = require('js/node_modules/mathjs');
//var linSystem = require("linear-solve");

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

    return Array(x, y);
}

var sistema = ['x+y-3', '(x*x)+(y*y)-9'];
var x0 = [1, 5];

newton(sistema, x0, 0.0001, 0.0001);