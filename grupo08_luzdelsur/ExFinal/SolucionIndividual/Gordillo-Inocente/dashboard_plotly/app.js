// ==============================================
// DATOS - SuperMarket Sales Dashboard
// ==============================================

const data = {
    // Ventas por Sucursal
    ventasSucursal: {
        yangon: { enero: 106197.67, febrero: 0, marzo: 0, total: 106197.67 },
        naypyitaw: { enero: 110568.71, febrero: 0, marzo: 0, total: 110568.71 },
        mandalay: { enero: 106200.37, febrero: 0, marzo: 0, total: 106200.37 }
    },

    // Productos
    productos: [
        { nombre: 'Alimentos y bebidas', ventas: 56144.84, margen: 2673.56, rating: 6.97 },
        { nombre: 'Moda y accesorios', ventas: 54305.89, margen: 2585.78, rating: 7.03 },
        { nombre: 'Productos electrónicos', ventas: 54337.53, margen: 2587.50, rating: 6.92 },
        { nombre: 'Deportes y viajes', ventas: 55122.83, margen: 2624.90, rating: 6.92 },
        { nombre: 'Hogar y estilo de vida', ventas: 53861.91, margen: 2564.85, rating: 6.84 },
        { nombre: 'Salud y belleza', ventas: 49193.74, margen: 2342.56, rating: 7.00 }
    ],

    // Métodos de Pago
    metodosPago: [
        { metodo: 'E-wallet', ventas: 109994.10, transacciones: 345 },
        { metodo: 'Efectivo', ventas: 112206.57, transacciones: 344 },
        { metodo: 'Tarjeta de Crédito', ventas: 100767.08, transacciones: 311 }
    ],

    // Clientes
    clientes: [
        { tipo: 'Miembro - Mujer', ticket: 344.86, transacciones: 259 },
        { tipo: 'Miembro - Hombre', ticket: 317.43, transacciones: 240 },
        { tipo: 'Normal - Mujer', ticket: 308.71, transacciones: 262 },
        { tipo: 'Normal - Hombre', ticket: 319.55, transacciones: 239 }
    ]
};

// ==============================================
// NAVEGACIÓN ENTRE DASHBOARDS
// ==============================================

function showDashboard(dashboardNumber, button) {
    // Ocultar todos los dashboards
    document.querySelectorAll('.dashboard').forEach(d => {
        d.classList.remove('active');
    });

    // Remover clase active de todos los botones
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostrar dashboard seleccionado
    document.getElementById('dashboard' + dashboardNumber).classList.add('active');
    button.classList.add('active');

    // Inicializar gráficos del dashboard seleccionado con animación
    setTimeout(() => {
        if (dashboardNumber === 1) {
            initDashboard1();
        } else if (dashboardNumber === 2) {
            initDashboard2();
        } else if (dashboardNumber === 3) {
            initDashboard3();
        }
    }, 100);
}

// ==============================================
// CONFIGURACIÓN DE PLOTLY
// ==============================================

const plotlyConfig = {
    responsive: true,
    displayModeBar: false
};

const animationConfig = {
    transition: {
        duration: 1500,
        easing: 'cubic-in-out'
    },
    frame: {
        duration: 1500
    }
};

// ==============================================
// DASHBOARD 1: Ventas por Sucursal + Métodos de Pago
// ==============================================

function initDashboard1() {
    createChart1_1();
    createChart1_2();
    createChart1_3();
    createChart1_4();
    createChart1_5();
    createChart1_6();
}

// Chart 1.1: Ventas Mensuales por Sucursal (Barras Agrupadas)
function createChart1_1() {
    const trace1 = {
        x: ['Yangon', 'Naypyitaw', 'Mandalay'],
        y: [0, 0, 0],
        name: 'Enero',
        type: 'bar',
        marker: {
            color: '#00d4ff',
            line: { width: 1, color: '#0099cc' }
        }
    };

    const trace2 = {
        x: ['Yangon', 'Naypyitaw', 'Mandalay'],
        y: [0, 0, 0],
        name: 'Febrero',
        type: 'bar',
        marker: {
            color: '#ff006e',
            line: { width: 1, color: '#cc0058' }
        }
    };

    const trace3 = {
        x: ['Yangon', 'Naypyitaw', 'Mandalay'],
        y: [0, 0, 0],
        name: 'Marzo',
        type: 'bar',
        marker: {
            color: '#8338ec',
            line: { width: 1, color: '#6a2dc3' }
        }
    };

    const layout = {
        barmode: 'group',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Sucursal'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ventas ($)'
        },
        legend: {
            orientation: 'h',
            y: -0.2
        },
        margin: { l: 60, r: 30, t: 20, b: 60 }
    };

    Plotly.newPlot('chart1_1', [trace1, trace2, trace3], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart1_1', {
            data: [
                { y: [106197.67, 110568.71, 106200.37] },
                { y: [0, 0, 0] },
                { y: [0, 0, 0] }
            ]
        }, animationConfig);
    }, 300);
}

// Chart 1.2: Distribución Total por Ciudad (Donut)
function createChart1_2() {
    const trace = {
        labels: ['Yangon', 'Naypyitaw', 'Mandalay'],
        values: [0, 0, 0],
        type: 'pie',
        hole: 0.5,
        marker: {
            colors: ['#00d4ff', '#ff006e', '#8338ec'],
            line: { color: '#0a1929', width: 2 }
        },
        textinfo: 'label+percent',
        textfont: { size: 14, color: '#fff' }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff' },
        showlegend: true,
        legend: {
            orientation: 'h',
            y: -0.1
        },
        margin: { l: 20, r: 20, t: 20, b: 60 },
        annotations: [{
            text: '$322,967',
            x: 0.5,
            y: 0.5,
            font: { size: 24, color: '#00d4ff', weight: 'bold' },
            showarrow: false
        }]
    };

    Plotly.newPlot('chart1_2', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart1_2', {
            data: [{ values: [106197.67, 110568.71, 106200.37] }]
        }, animationConfig);
    }, 500);
}

// Chart 1.3: Métodos de Pago - Ventas (Barras Horizontales)
function createChart1_3() {
    const trace = {
        x: [0, 0, 0],
        y: ['E-wallet', 'Efectivo', 'Tarjeta de Crédito'],
        type: 'bar',
        orientation: 'h',
        marker: {
            color: ['#00d4ff', '#ff006e', '#8338ec'],
            line: { width: 1, color: '#0a1929' }
        },
        text: ['$0', '$0', '$0'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 12 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ventas ($)'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0)',
        },
        margin: { l: 150, r: 80, t: 20, b: 50 }
    };

    Plotly.newPlot('chart1_3', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart1_3', {
            data: [{
                x: [109994.10, 112206.57, 100767.08],
                text: ['$109,994', '$112,207', '$100,767']
            }]
        }, animationConfig);
    }, 700);
}

// Chart 1.4: Transacciones por Método de Pago (Barras)
function createChart1_4() {
    const trace = {
        x: ['E-wallet', 'Efectivo', 'Tarjeta de Crédito'],
        y: [0, 0, 0],
        type: 'bar',
        marker: {
            color: '#00d4ff',
            line: { width: 1, color: '#0099cc' }
        },
        text: [0, 0, 0],
        textposition: 'outside',
        textfont: { color: '#fff', size: 12 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Transacciones'
        },
        margin: { l: 60, r: 30, t: 20, b: 80 }
    };

    Plotly.newPlot('chart1_4', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart1_4', {
            data: [{
                y: [345, 344, 311],
                text: [345, 344, 311]
            }]
        }, animationConfig);
    }, 900);
}

// Chart 1.5: Ticket Promedio por Método de Pago
function createChart1_5() {
    const ticketEwallet = 109994.10 / 345;
    const ticketEfectivo = 112206.57 / 344;
    const ticketTarjeta = 100767.08 / 311;

    const trace = {
        x: ['E-wallet', 'Efectivo', 'Tarjeta de Crédito'],
        y: [0, 0, 0],
        type: 'bar',
        marker: {
            color: ['#00d4ff', '#ff006e', '#8338ec'],
            line: { width: 1, color: '#0a1929' }
        },
        text: ['$0', '$0', '$0'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 12 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ticket Promedio ($)'
        },
        margin: { l: 60, r: 30, t: 20, b: 80 }
    };

    Plotly.newPlot('chart1_5', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart1_5', {
            data: [{
                y: [ticketEwallet, ticketEfectivo, ticketTarjeta],
                text: ['$' + ticketEwallet.toFixed(2), '$' + ticketEfectivo.toFixed(2), '$' + ticketTarjeta.toFixed(2)]
            }]
        }, animationConfig);
    }, 1100);
}

// Chart 1.6: Participación de Mercado por Sucursal
function createChart1_6() {
    const total = 322966.75;
    const yangonPct = (106197.67 / total) * 100;
    const naypyitawPct = (110568.71 / total) * 100;
    const mandalayPct = (106200.37 / total) * 100;

    const trace = {
        x: [0, 0, 0],
        y: ['Yangon', 'Naypyitaw', 'Mandalay'],
        type: 'bar',
        orientation: 'h',
        marker: {
            color: ['#00d4ff', '#ff006e', '#8338ec'],
            line: { width: 1, color: '#0a1929' }
        },
        text: ['0%', '0%', '0%'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 12 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Participación (%)',
            range: [0, 40]
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0)',
        },
        margin: { l: 100, r: 80, t: 20, b: 50 }
    };

    Plotly.newPlot('chart1_6', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart1_6', {
            data: [{
                x: [yangonPct, naypyitawPct, mandalayPct],
                text: [yangonPct.toFixed(1) + '%', naypyitawPct.toFixed(1) + '%', mandalayPct.toFixed(1) + '%']
            }]
        }, animationConfig);
    }, 1300);
}

// ==============================================
// DASHBOARD 2: Análisis de Productos
// ==============================================

function initDashboard2() {
    createChart2_1();
    createChart2_2();
    createChart2_3();
    createChart2_4();
    createChart2_5();
    createChart2_6();
}

// Chart 2.1: Ranking de Productos por Ventas (Barras Horizontales)
function createChart2_1() {
    const productosOrdenados = [...data.productos].sort((a, b) => b.ventas - a.ventas);
    
    const trace = {
        x: [0, 0, 0, 0, 0, 0],
        y: productosOrdenados.map(p => p.nombre),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: ['#00d4ff', '#00b8e6', '#009ccc', '#0080b3', '#006499', '#004880'],
            line: { width: 1, color: '#0a1929' }
        },
        text: ['$0', '$0', '$0', '$0', '$0', '$0'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 11 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 11 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ventas ($)'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0)',
            automargin: true
        },
        margin: { l: 180, r: 80, t: 20, b: 50 }
    };

    Plotly.newPlot('chart2_1', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const ventasValues = productosOrdenados.map(p => p.ventas);
        const ventasText = productosOrdenados.map(p => '$' + p.ventas.toLocaleString('en-US', {maximumFractionDigits: 0}));
        
        Plotly.animate('chart2_1', {
            data: [{
                x: ventasValues,
                text: ventasText
            }]
        }, animationConfig);
    }, 300);
}

// Chart 2.2: Margen Bruto por Producto (Barras)
function createChart2_2() {
    const trace = {
        x: data.productos.map(p => p.nombre),
        y: [0, 0, 0, 0, 0, 0],
        type: 'bar',
        marker: {
            color: '#ff006e',
            line: { width: 1, color: '#cc0058' }
        },
        text: ['$0', '$0', '$0', '$0', '$0', '$0'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 11 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 10 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            tickangle: -45
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Margen ($)'
        },
        margin: { l: 60, r: 30, t: 20, b: 120 }
    };

    Plotly.newPlot('chart2_2', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const margenValues = data.productos.map(p => p.margen);
        const margenText = data.productos.map(p => '$' + p.margen.toLocaleString('en-US', {maximumFractionDigits: 0}));
        
        Plotly.animate('chart2_2', {
            data: [{
                y: margenValues,
                text: margenText
            }]
        }, animationConfig);
    }, 500);
}

// Chart 2.3: Calificación por Línea de Producto (Scatter)
function createChart2_3() {
    const trace = {
        x: data.productos.map(p => p.nombre),
        y: [0, 0, 0, 0, 0, 0],
        mode: 'markers+text',
        type: 'scatter',
        marker: {
            size: [0, 0, 0, 0, 0, 0],
            color: '#8338ec',
            line: { width: 2, color: '#6a2dc3' }
        },
        text: ['0.0', '0.0', '0.0', '0.0', '0.0', '0.0'],
        textposition: 'top center',
        textfont: { color: '#fff', size: 12 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 10 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            tickangle: -45
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Rating',
            range: [0, 10]
        },
        margin: { l: 60, r: 30, t: 20, b: 120 }
    };

    Plotly.newPlot('chart2_3', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const ratingValues = data.productos.map(p => p.rating);
        const ratingSize = data.productos.map(p => p.rating * 5);
        const ratingText = data.productos.map(p => p.rating.toFixed(2));
        
        Plotly.animate('chart2_3', {
            data: [{
                y: ratingValues,
                marker: { size: ratingSize },
                text: ratingText
            }]
        }, animationConfig);
    }, 700);
}

// Chart 2.4: Comparativa Ventas vs Margen (Barras Agrupadas)
function createChart2_4() {
    const trace1 = {
        x: data.productos.map(p => p.nombre),
        y: [0, 0, 0, 0, 0, 0],
        name: 'Ventas',
        type: 'bar',
        marker: {
            color: '#00d4ff',
            line: { width: 1, color: '#0099cc' }
        }
    };

    const trace2 = {
        x: data.productos.map(p => p.nombre),
        y: [0, 0, 0, 0, 0, 0],
        name: 'Margen',
        type: 'bar',
        marker: {
            color: '#ff006e',
            line: { width: 1, color: '#cc0058' }
        }
    };

    const layout = {
        barmode: 'group',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 10 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            tickangle: -45
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Monto ($)'
        },
        legend: {
            orientation: 'h',
            y: -0.3
        },
        margin: { l: 60, r: 30, t: 20, b: 140 }
    };

    Plotly.newPlot('chart2_4', [trace1, trace2], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const ventasValues = data.productos.map(p => p.ventas);
        const margenValues = data.productos.map(p => p.margen);
        
        Plotly.animate('chart2_4', {
            data: [
                { y: ventasValues },
                { y: margenValues }
            ]
        }, animationConfig);
    }, 900);
}

// Chart 2.5: Análisis de Rentabilidad por Producto (Scatter Plot)
function createChart2_5() {
    const trace = {
        x: data.productos.map(p => 0),
        y: data.productos.map(p => 0),
        mode: 'markers+text',
        type: 'scatter',
        marker: {
            size: 20,
            color: ['#00d4ff', '#00b8e6', '#009ccc', '#0080b3', '#006499', '#004880'],
            line: { width: 2, color: '#fff' }
        },
        text: data.productos.map(p => p.nombre.split(' ')[0]),
        textposition: 'top center',
        textfont: { color: '#fff', size: 10 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ventas ($)',
            range: [48000, 57000]
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Margen ($)',
            range: [2200, 2700]
        },
        margin: { l: 60, r: 30, t: 20, b: 60 }
    };

    Plotly.newPlot('chart2_5', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const ventasValues = data.productos.map(p => p.ventas);
        const margenValues = data.productos.map(p => p.margen);
        
        Plotly.animate('chart2_5', {
            data: [{
                x: ventasValues,
                y: margenValues
            }]
        }, animationConfig);
    }, 1100);
}

// Chart 2.6: Distribución de Productos por Rating (Donut)
function createChart2_6() {
    const ratingRanges = [
        { label: 'Excelente (7.0+)', count: 0, color: '#00ff88' },
        { label: 'Bueno (6.9-7.0)', count: 0, color: '#00d4ff' },
        { label: 'Regular (<6.9)', count: 0, color: '#ff006e' }
    ];

    data.productos.forEach(p => {
        if (p.rating >= 7.0) ratingRanges[0].count++;
        else if (p.rating >= 6.9) ratingRanges[1].count++;
        else ratingRanges[2].count++;
    });

    const trace = {
        labels: ratingRanges.map(r => r.label),
        values: [0, 0, 0],
        type: 'pie',
        hole: 0.5,
        marker: {
            colors: ratingRanges.map(r => r.color),
            line: { color: '#0a1929', width: 2 }
        },
        textinfo: 'label+value',
        textfont: { size: 12, color: '#fff' }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff' },
        showlegend: true,
        legend: {
            orientation: 'h',
            y: -0.1
        },
        margin: { l: 20, r: 20, t: 20, b: 60 },
        annotations: [{
            text: '6 Líneas',
            x: 0.5,
            y: 0.5,
            font: { size: 20, color: '#00d4ff', weight: 'bold' },
            showarrow: false
        }]
    };

    Plotly.newPlot('chart2_6', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart2_6', {
            data: [{ values: ratingRanges.map(r => r.count) }]
        }, animationConfig);
    }, 1300);
}

// ==============================================
// DASHBOARD 3: Segmentación de Clientes
// ==============================================

function initDashboard3() {
    createChart3_1();
    createChart3_2();
    createChart3_3();
    createChart3_4();
    createChart3_5();
    createChart3_6();
}

// Chart 3.1: Ticket Promedio por Tipo de Cliente (Barras)
function createChart3_1() {
    const trace = {
        x: data.clientes.map(c => c.tipo),
        y: [0, 0, 0, 0],
        type: 'bar',
        marker: {
            color: ['#00d4ff', '#0099cc', '#ff006e', '#cc0058'],
            line: { width: 1, color: '#0a1929' }
        },
        text: ['$0', '$0', '$0', '$0'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 12 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 11 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            tickangle: -30
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ticket Promedio ($)'
        },
        margin: { l: 60, r: 30, t: 20, b: 100 }
    };

    Plotly.newPlot('chart3_1', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const ticketValues = data.clientes.map(c => c.ticket);
        const ticketText = data.clientes.map(c => '$' + c.ticket.toFixed(2));
        
        Plotly.animate('chart3_1', {
            data: [{
                y: ticketValues,
                text: ticketText
            }]
        }, animationConfig);
    }, 300);
}

// Chart 3.2: Ventas por Género y Tipo (Barras Agrupadas)
function createChart3_2() {
    const trace1 = {
        x: ['Mujer', 'Hombre'],
        y: [0, 0],
        name: 'Miembro',
        type: 'bar',
        marker: {
            color: '#00d4ff',
            line: { width: 1, color: '#0099cc' }
        }
    };

    const trace2 = {
        x: ['Mujer', 'Hombre'],
        y: [0, 0],
        name: 'Normal',
        type: 'bar',
        marker: {
            color: '#ff006e',
            line: { width: 1, color: '#cc0058' }
        }
    };

    const layout = {
        barmode: 'group',
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Género'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ventas ($)'
        },
        legend: {
            orientation: 'h',
            y: -0.2
        },
        margin: { l: 60, r: 30, t: 20, b: 70 }
    };

    Plotly.newPlot('chart3_2', [trace1, trace2], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const miembroMujer = data.clientes[0].ticket * data.clientes[0].transacciones;
        const miembroHombre = data.clientes[1].ticket * data.clientes[1].transacciones;
        const normalMujer = data.clientes[2].ticket * data.clientes[2].transacciones;
        const normalHombre = data.clientes[3].ticket * data.clientes[3].transacciones;
        
        Plotly.animate('chart3_2', {
            data: [
                { y: [miembroMujer, miembroHombre] },
                { y: [normalMujer, normalHombre] }
            ]
        }, animationConfig);
    }, 500);
}

// Chart 3.3: Distribución de Transacciones (Donut)
function createChart3_3() {
    const trace = {
        labels: data.clientes.map(c => c.tipo),
        values: [0, 0, 0, 0],
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: ['#00d4ff', '#0099cc', '#ff006e', '#cc0058'],
            line: { color: '#0a1929', width: 2 }
        },
        textinfo: 'label+percent',
        textfont: { size: 12, color: '#fff' }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 11 },
        showlegend: true,
        legend: {
            orientation: 'v',
            x: 1.1,
            y: 0.5
        },
        margin: { l: 20, r: 150, t: 20, b: 20 },
        annotations: [{
            text: '1,000',
            x: 0.5,
            y: 0.5,
            font: { size: 24, color: '#00d4ff', weight: 'bold' },
            showarrow: false
        }]
    };

    Plotly.newPlot('chart3_3', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const transaccionesValues = data.clientes.map(c => c.transacciones);
        
        Plotly.animate('chart3_3', {
            data: [{ values: transaccionesValues }]
        }, animationConfig);
    }, 700);
}

// Chart 3.4: Comparativa Miembro vs Normal (Barras Horizontales)
function createChart3_4() {
    const totalMiembro = data.clientes[0].ticket * data.clientes[0].transacciones + 
                         data.clientes[1].ticket * data.clientes[1].transacciones;
    const totalNormal = data.clientes[2].ticket * data.clientes[2].transacciones + 
                        data.clientes[3].ticket * data.clientes[3].transacciones;

    const trace = {
        x: [0, 0],
        y: ['Cliente Miembro', 'Cliente Normal'],
        type: 'bar',
        orientation: 'h',
        marker: {
            color: ['#00d4ff', '#ff006e'],
            line: { width: 1, color: '#0a1929' }
        },
        text: ['$0', '$0'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 14 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 12 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Ventas Totales ($)'
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0)',
        },
        margin: { l: 150, r: 100, t: 20, b: 50 }
    };

    Plotly.newPlot('chart3_4', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart3_4', {
            data: [{
                x: [totalMiembro, totalNormal],
                text: ['$' + totalMiembro.toLocaleString('en-US', {maximumFractionDigits: 0}), 
                       '$' + totalNormal.toLocaleString('en-US', {maximumFractionDigits: 0})]
            }]
        }, animationConfig);
    }, 900);
}

// Chart 3.5: Valor Promedio del Cliente (LTV - Lifetime Value Simulado)
function createChart3_5() {
    // Simulamos LTV como ticket * transacciones promedio por segmento
    const ltv = data.clientes.map(c => ({
        tipo: c.tipo,
        valor: c.ticket * (c.transacciones / 100) // Factor simulado
    }));

    const trace = {
        x: ltv.map(l => l.tipo),
        y: [0, 0, 0, 0],
        type: 'bar',
        marker: {
            color: ['#00d4ff', '#0099cc', '#ff006e', '#cc0058'],
            line: { width: 1, color: '#0a1929' }
        },
        text: ['$0', '$0', '$0', '$0'],
        textposition: 'outside',
        textfont: { color: '#fff', size: 11 }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', size: 10 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            tickangle: -30
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.1)',
            title: 'Valor del Cliente ($)'
        },
        margin: { l: 60, r: 30, t: 20, b: 100 }
    };

    Plotly.newPlot('chart3_5', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        const ltvValues = ltv.map(l => l.valor);
        const ltvText = ltv.map(l => '$' + l.valor.toFixed(0));
        
        Plotly.animate('chart3_5', {
            data: [{
                y: ltvValues,
                text: ltvText
            }]
        }, animationConfig);
    }, 1100);
}

// Chart 3.6: Distribución de Clientes por Género (Donut)
function createChart3_6() {
    const totalMujer = data.clientes[0].transacciones + data.clientes[2].transacciones;
    const totalHombre = data.clientes[1].transacciones + data.clientes[3].transacciones;

    const trace = {
        labels: ['Mujer', 'Hombre'],
        values: [0, 0],
        type: 'pie',
        hole: 0.5,
        marker: {
            colors: ['#ff006e', '#00d4ff'],
            line: { color: '#0a1929', width: 2 }
        },
        textinfo: 'label+percent',
        textfont: { size: 14, color: '#fff' }
    };

    const layout = {
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff' },
        showlegend: true,
        legend: {
            orientation: 'h',
            y: -0.1
        },
        margin: { l: 20, r: 20, t: 20, b: 60 },
        annotations: [{
            text: '1,000',
            x: 0.5,
            y: 0.5,
            font: { size: 24, color: '#00d4ff', weight: 'bold' },
            showarrow: false
        }]
    };

    Plotly.newPlot('chart3_6', [trace], layout, plotlyConfig);

    // Animación
    setTimeout(() => {
        Plotly.animate('chart3_6', {
            data: [{ values: [totalMujer, totalHombre] }]
        }, animationConfig);
    }, 1300);
}

// ==============================================
// INICIALIZACIÓN
// ==============================================

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar el primer dashboard por defecto
    initDashboard1();

    // Resize handler
    window.addEventListener('resize', function() {
        const activeDashboard = document.querySelector('.dashboard.active');
        if (activeDashboard) {
            const dashboardId = activeDashboard.id;
            const charts = activeDashboard.querySelectorAll('.chart');
            charts.forEach(chart => {
                Plotly.Plots.resize(chart);
            });
        }
    });

    console.log('Dashboard cargado exitosamente con 3 pantallas y animaciones');
});
