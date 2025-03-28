// const elements = {
//     drawBtn: document.getElementById('draw-btn'),
//     resetBtn: document.getElementById('reset-btn'),
//     player1Card: document.getElementById('player1-btn'),
//     player2Card: document.getElementById('player2-btn'),
//     player1Count: document.getElementById('player1-count'),
//     player2Count: document.getElementById('player2-count'),
//     gameLog: document.getElementById('game-log'),
// }

document.addEventListener('DOMContentLoaded', async() => 
{   
    await updateGameState();
});

async function updateGameState(){ 
    try {
        const response = await fetch('/state');
        if (response.ok)
        { 
            const state = await response.json();
            document.getElementById('player1-cards').textContent = state.p1_count;
            document.getElementById('player2-cards').textContent = state.p2_count;
        }
    } catch (error){ 
        console.error('State update error:', error);
    }
}

document.getElementById('draw').addEventListener('click', async() =>
{ 
    const drawButton = document.getElementById('draw');
    try {
            drawButton.disabled = true;
            drawButton.textContent = 'Drawing...';

            const response = await fetch('/play', { method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            console.log("Response received: ", response);


            if (!response.ok)
                { 
                    const errorText = await response.text();
                    throw new Error('HTTP error! status: ${response.stats}');
                }
            const result = await response.json();
            console.log("Result data:", result);


            if (result.battle_cards && result.battle_cards.length >= 2){ 
                console.log("Cards to display:", result.battle_cards);
                document.getElementById('player1-battle-card').innerHTML = `
                <img src="/static/cards/${result.battle_cards[1]}" 
                    onerror="console.error('Failed to load: ${result.battle_cards[0]}')">`;
                document.getElementById('player2-battle-card').innerHTML = `
                <img src="/static/cards/${result.battle_cards[1]}" 
                    onerror="console.error('Failed to load: ${result.battle_cards[1]}')">`;   
            }


            document.getElementById('player1-cards').textContent = result.p1_count;
            document.getElementById('player2-cards').textContent = result.p2_count;

            console.log("Draw completed successfully");

            const logElement = document.getElementById('result');
            logElement.innerHTML = result.log;

            await updateGameState();

        } catch (error)
        { 
            console.error('Draw error:', error);
            showError(error.message);
        } finally {
            drawButton.disable = false;
        }
});


document.getElementById('reset').addEventListener('click', async () =>
{
    try {
        const response = await fetch('/reset', {method: 'POST'});
        if (!response.ok) throw new Error('Reset failed');
        location.reload();
    } catch (error){ 
        console.error('Reset error', error);
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
