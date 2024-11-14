document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de reservas por hora (container_satistics_1)
    const ctx = document.getElementById('reservationsByHourChart').getContext('2d');
    const hours = JSON.parse(document.getElementById('chart-hours').textContent);
    const counts = JSON.parse(document.getElementById('chart-counts').textContent);
    const reservationsByHourChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hours,
            datasets: [{
                label: 'Number of Reservations',
                data: counts,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { 
                    title: { display: true, text: 'Hour of the Day' }
                },
                y: { 
                    beginAtZero: true, 
                    title: { display: true, text: 'Number of Reservations' }
                }
            }
        }
    });

    // Gráfico de reservas por bloque (container_satistics_2)
    const ctx2 = document.getElementById('reservationsByBuildingChart').getContext('2d');
    const blocks = JSON.parse(document.getElementById('chart-blocks').textContent);
    const counts2 = JSON.parse(document.getElementById('chart2-counts').textContent);
    const reservationsByBuildingChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: blocks,
            datasets: [{
                label: 'Number of Reservations',
                data: counts2,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { 
                    title: { display: true, text: 'Building Numbers' }
                },
                y: { 
                    beginAtZero: true, 
                    title: { display: true, text: 'Number of Reservations' }
                }
            }
        }
    });

    // Función para analizar datos por hora
    window.analyzeData = function() {
        const analysisContainer = document.getElementById('collapseExample1');
        
        fetch('/analyze-data/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('card_text_1').textContent = data.message;
                new bootstrap.Collapse(analysisContainer, { toggle: true });
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('card_text_1').textContent = "An error occurred while analyzing data.";
            });
    }

    // Función para analizar datos por bloque
    window.analyzeBlockData = function() {
        const analysisContainer2 = document.getElementById('collapseExample2');
        
        fetch('/analyze-block-data/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('card_text_2').textContent = data.message;
                new bootstrap.Collapse(analysisContainer2, { toggle: true });
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('card_text_2').textContent = "An error occurred while analyzing block data.";
            });
    }
});
