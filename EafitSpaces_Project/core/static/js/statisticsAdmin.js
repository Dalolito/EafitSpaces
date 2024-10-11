document.addEventListener('DOMContentLoaded', function() {
    // Verificar que el canvas esté disponible antes de intentar crear el gráfico
    const ctx = document.getElementById('reservationsByHourChart').getContext('2d');

    // Los datos de las horas y los conteos serán inyectados desde el HTML con JSON.parse
    const hours = JSON.parse(document.getElementById('chart-hours').textContent);
    const counts = JSON.parse(document.getElementById('chart-counts').textContent);

    // Crear la gráfica usando Chart.js
    const reservationsByHourChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hours, // Lista de horas (6-22)
            datasets: [{
                label: 'Number of Reservations',
                data: counts, // Número de reservas por cada hora
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive:true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Hour of the Day'
                    },
                    ticks: {
                        callback: function(value) {
                            // Convertir los valores de las horas a formato 12 horas con AM/PM
                            const hour = parseInt(this.getLabelForValue(value));
                            if (hour > 12) {
                                return (hour - 12) + ' PM';
                            } else if (hour === 12) {
                                return '12 PM';
                            } else if (hour === 0) {
                                return '12 AM';
                            } else {
                                return hour + ' AM';
                            }
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Reservations'
                    }
                }
            }
        }
    });


    const ctx2 = document.getElementById('reservationsByBuildingChart').getContext('2d');

    // Obtener los datos de los elementos JSON
    const blocks = JSON.parse(document.getElementById('chart-blocks').textContent);
    const counts2 = JSON.parse(document.getElementById('chart2-counts').textContent);

    // Crear la gráfica de barras usando Chart.js
    const reservationsByBuildingChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: blocks, // Números de bloques (e.g., "38", "39", ...)
            datasets: [{
                label: 'Number of Reservations',
                data: counts2, // Cantidad de reservas para cada bloque
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Reservations'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Building Numbers'
                    }
                }
            }
        }
    });
});
