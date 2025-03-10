document.getElementById('transaccionForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar que el formulario se envíe

    // Obtener los valores del formulario
    const cuenta = document.getElementById('cuenta').value;
    const tipo = document.getElementById('tipo').value;
    const monto = parseFloat(document.getElementById('monto').value);

    // Validar el monto
    if (isNaN(monto) || monto <= 0) {
        mostrarResultado('El monto debe ser un número positivo.', 'error');
        return;
    }

    // Simular una transacción
    let saldoActual = 1000; // Saldo inicial simulado
    let mensaje = '';

    if (tipo === 'deposito') {
        saldoActual += monto;
        mensaje = `Depósito de $${monto.toFixed(2)} realizado. Nuevo saldo: $${saldoActual.toFixed(2)}`;
    } else if (tipo === 'retiro') {
        if (monto > saldoActual) {
            mostrarResultado('Fondos insuficientes para realizar el retiro.', 'error');
            return;
        }
        saldoActual -= monto;
        mensaje = `Retiro de $${monto.toFixed(2)} realizado. Nuevo saldo: $${saldoActual.toFixed(2)}`;
    }

    // Mostrar el resultado
    mostrarResultado(mensaje, 'exito');
});

function mostrarResultado(mensaje, tipo) {
    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.textContent = mensaje;
    resultadoDiv.className = tipo; // Aplicar clase para estilos (éxito o error)
}