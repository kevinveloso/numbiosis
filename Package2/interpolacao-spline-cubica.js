/* global math */

function processPoints(points) {
	// ordenar matriz por valores x
	points.sort(function(a, b) {
		if (a.x < b.x) return -1;
		if (a.x === b.x) return 0;
		return 1;
	});

	for (var i = 0; i < points.length; i++) {
		if (i < points.length - 1 && points[i].x === points[i + 1].x) {
			// dois pontos têm o mesmo valor x

			// verifique se o valor y é o mesmo
			if (points[i].y === points[i + 1].y) {
				// remova o último
				points.splice(i, 1);
				i--;
			}
			else {
				throw Error('SameXDifferentY');
			}
		}
	}

	if (points.length < 2) {
		throw Error('NotEnoughPoints');
	}	

	for (var i = points.length - 1; i >= 0; i--) {
		points[i].x = parseFloat(points[i].x);
		points[i].y = parseFloat(points[i].y);
	}

	return points;
}

function getMinMax(points) {
	// determine os valores max e min x e y
	minX = points[0].x;
	maxX = points[0].x;
	minY = points[0].y;
	maxY = points[0].y;

	for (var i = 1; i < points.length; i++) {
		minX = Math.min(minX, points[i].x);
		maxX = Math.max(maxX, points[i].x);
		minY = Math.min(minY, points[i].y);
		maxY = Math.max(maxY, points[i].y);
	}

	return {
		minX: minX, 
		maxX: maxX, 
		minY: minY, 
		maxY: maxY 
	};
}

// Interpolação de spline cúbica
// A função usa a biblioteca math.js para garantir resultados de alta precisão.
// @param p Os pontos. Uma matriz de objetos com coordenadas x e y.
// @param type A condição de contorno de interpolação ("quadrático", "notaknot", "periódico", "natural"). "natural" é o valor padrão.
function cubicSplineInterpolation(p, boundary) {
	var row = 0;
	var solutionIndex = (p.length - 1) * 4;

	// inicializar matriz
	var m = []; // linhas
	for (var i = 0; i < (p.length - 1) * 4; i++) {
		// colunas (linhas + 1)
		m.push([]);
		for (var j = 0; j <= (p.length - 1) * 4; j++) {
			m[i].push(math.bignumber(0)); // preencher com zeros
		}
	}

	// splines através de equações p
	for (var functionNr = 0; functionNr < p.length-1; functionNr++, row++) {
		var p0 = p[functionNr], p1 = p[functionNr+1];
		m[row][functionNr*4+0] = math.pow(math.bignumber(p0.x), 3);
		m[row][functionNr*4+1] = math.pow(math.bignumber(p0.x), 2); 
		m[row][functionNr*4+2] = math.bignumber(p0.x);
		m[row][functionNr*4+3] = math.bignumber(1); 
		m[row][solutionIndex] = math.bignumber(p0.y);

		m[++row][functionNr*4+0] = math.pow(math.bignumber(p1.x), 3);
		m[row][functionNr*4+1] = math.pow(math.bignumber(p1.x), 2); 
		m[row][functionNr*4+2] = math.bignumber(p1.x);
		m[row][functionNr*4+3] = math.bignumber(1); 
		m[row][solutionIndex] = math.bignumber(p1.y);
	}

	// primeira derivada
	for (var functionNr = 0; functionNr < p.length - 2; functionNr++, row++) {
		var p1 = p[functionNr+1];
		m[row][functionNr*4+0] = math.multiply(3, math.pow(math.bignumber(p1.x), 2));
		m[row][functionNr*4+1] = math.multiply(2, math.bignumber(p1.x));
		m[row][functionNr*4+2] = math.bignumber(1);
		m[row][functionNr*4+4] = math.multiply(-3, math.pow(math.bignumber(p1.x), 2));
		m[row][functionNr*4+5] = math.multiply(-2, math.bignumber(p1.x));
		m[row][functionNr*4+6] = math.bignumber(-1);
	}

	// segunda derivada
	for (var functionNr = 0; functionNr < p.length - 2; functionNr++, row++) {
		var p1 = p[functionNr+1];
		m[row][functionNr*4+0] = math.multiply(6, math.bignumber(p1.x));
		m[row][functionNr*4+1] = math.bignumber(2);
		m[row][functionNr*4+4] = math.multiply(-6, math.bignumber(p1.x));
		m[row][functionNr*4+5] = math.bignumber(-2);
	}


	// condições de contorno
	switch (boundary) {
		/*case "quadratic": // primeira e última spline quadrática
			m[row++][0] = math.bignumber(1);
			m[row++][solutionIndex-4+0] = math.bignumber(1);
			break;

		case "notaknot": // Não-nó-spline
			m[row][0+0] = math.bignumber(1);
			m[row++][0+4] = math.bignumber(-1);
			m[row][solutionIndex-8+0] = math.bignumber(1);
			m[row][solutionIndex-4+0] = math.bignumber(-1);
			break;

		case "periodic": // função periódica
			// primeira derivada do primeiro e último ponto igual
			m[row][0] = math.multiply(3, math.pow(math.bignumber(p[0].x), 2));
			m[row][1] = math.multiply(2, math.bignumber(p[0].x));
			m[row][2] = math.bignumber(1);
			m[row][solutionIndex-4+0] = math.multiply(-3, math.pow(math.bignumber(p[p.length-1].x), 2));
			m[row][solutionIndex-4+1] = math.multiply(-2, math.bignumber(p[p.length-1].x));
			m[row++][solutionIndex-4+2] = math.bignumber(-1);

			// segunda derivada do primeiro e último ponto igual
			m[row][0] = math.multiply(6, math.bignumber(p[0].x));
			m[row][1] = math.bignumber(2);
			m[row][solutionIndex-4+0] = math.multiply(-6, math.bignumber(p[p.length-1].x));
			m[row][solutionIndex-4+1] = math.bignumber(-2);
			break;*/

			default: // spline natural
			m[row][0+0] = math.multiply(6, p[0].x);
			m[row++][0+1] = math.bignumber(2);
			m[row][solutionIndex-4+0] = math.multiply(6, math.bignumber(p[p.length-1].x));
			m[row][solutionIndex-4+1] = math.bignumber(2);
			break;
	}


	var reducedRowEchelonForm = rref(m);
	var coefficients = [];
	for (var i = 0; i < reducedRowEchelonForm.length; i++) {
		coefficients.push(reducedRowEchelonForm[i][reducedRowEchelonForm[i].length - 1]);
	}

	var functions = [];
	for (var i = 0; i < coefficients.length; i += 4) {
		functions.push({
			a: parseFloat(coefficients[i]),
			b: parseFloat(coefficients[i+1]),
			c: parseFloat(coefficients[i+2]),
			d: parseFloat(coefficients[i+3]),
			range: { xmin: parseFloat(p[i/4].x), xmax: parseFloat(p[i/4+1].x) }
		});
	}
	return functions;
}

// Formulário de escalão de fileira reduzido
// Extraído de https://rosettacode.org/wiki/Reduced_row_echelon_form
// Modificado para funcionar com math.js (alta precisão de flutuação).
function rref(mat) {
    var lead = 0;
    for (var r = 0; r < mat.length; r++) {
        if (mat[0].length <= lead) {
            return;
        }
        var i = r;
        while (mat[i][lead] === 0) {
            i++;
            if (mat.length === i) {
                i = r;
                lead++;
                if (mat[0].length === lead) {
                    return;
                }
            }
        }

        var tmp = mat[i];
        mat[i] = mat[r];
        mat[r] = tmp;
 
        var val = mat[r][lead];
        for (var j = 0; j < mat[0].length; j++) {
            mat[r][j] = math.divide(mat[r][j], val);
        }
 
        for (var i = 0; i < mat.length; i++) {
            if (i === r) continue;
            val = math.bignumber(mat[i][lead]);
            for (var j = 0; j < mat[0].length; j++) {
                mat[i][j] = math.subtract(math.bignumber(mat[i][j]), math.multiply((val), math.bignumber(mat[r][j])));
            }
        }
        lead++;
    }
    return mat;
}
