document.addEventListener('DOMContentLoaded', async() => 
{   
    try{
        const response = await fetch('/state');
        if (response.ok) {
            const state = await response.json();
            document.getElementById('player1-cards').textContent = state.p1_count;
            document.getElementById('player2-cards').textContent = state.p2_count;
        }
    } catch (error)
    { 
        console.log('State load error:', error);
    }
});

document.getElementById('draw').addEventListener('click', async() =>
{ 
    const drawButton = document.getElementById('draw');
    try {
            drawButton.disabled = true;
            drawButton.textContent = 'Drawing...';

            const response = await fetch('/play', { method: 'POST'});
            if (!response.ok) throw new Error('Server error');
        
            const result = await response.json();
        } catch (error)
        { 
            document.getElementById('result').innerHTML='Error: ${error.message}';
        } finally {
            drawButton.disabled = result?.game_over || false;
            drawButton.textContent = 'Draw Cards';
        }

    // Update card counts
    document.getElementById('player1-cards').textContent = result.p1_count;
    document.getElementById('player2-cards').textContent = result.p2_count;

    // Update battle cards
    const battleAreas = document.querySelectorAll('.battle-card');
    result.battle_cards.array.forEach((card, index) => {
        battleAreas[index].innerHTML =
        '<img src="/static/cards/${card}" alt="Battle Card" class="card-img">';
    });

    // Update game log
    document.getElementsByID('result').innerHTML = result.log;

    // Disable button if game over
    if(result.p1_count === 0 || result.p2_count === 0)
    { 
        document.getElementById('draw').disabled = true;
    }
});


document.getElementById('reset').addEventListener('click', async () =>
{
    try {
        const response = await fetch('/reset', {method: 'POST'});
        if (!response.ok) throw new Error('Reset failed');

        location.reload();
    } catch (error){ 
        alert('Reset failed: ${error message}');
    }
});


function updateCardDisplay(elementId, cardFilename)
{
    const container = document.getElementById(elementId);
    container.classList.add('card-entering');

    setTimeout(() => {
        container.innerHTML = cardFilename ?
            '<img src="/static/cards/${cardFilename}" class="card-img" alt="Battle card">' : '';
        container.classList.remove('card-entering');
    }, 300);
}

function updateLog(message) {
    const logElement = document.getElementById('result');
    logElement.innerHTML = message;
    logElement.scrollTop = logElement.scrollHeight;
}
