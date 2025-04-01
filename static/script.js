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
            console.log("Game state updated:", state); 
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
                    throw new Error('HTTP error! status: ${response.status} - ${errorText}');
                }
            const result = await response.json();
            console.log("Result data:", result);


            // if (result.battle_cards && result.battle_cards.length >= 2){ 
            //     // console.log("Cards to display:", result.battle_cards);
            //     // document.getElementById('player1-battle-card').innerHTML = `
            //     // <img src="/static/cards/${result.battle_cards[0]}" 
            //     //     onerror="console.error('Failed to load: ${result.battle_cards[0]}')">`;
            //     // document.getElementById('player2-battle-card').innerHTML = `
            //     // <img src="/static/cards/${result.battle_cards[1]}" 
            //     //     onerror="console.error('Failed to load: ${result.battle_cards[1]}')">`;   
            //     updateCardDisplay(
            //         'player1-battle-card', 
            //         `<img src="/static/cards/${result.battle_cards[0]}" 
            //          onerror="console.error('Failed to load: ${result.battle_cards[0]}')">`
            //     );
                
            //     updateCardDisplay(
            //         'player2-battle-card', 
            //         `<img src="/static/cards/${result.battle_cards[1]}" 
            //          onerror="console.error('Failed to load: ${result.battle_cards[1]}')">`
            //     );
            // }

            if (result.battle_cards && result.battle_cards.length >= 2) {
                // Clear previous cards
                const p1Container = document.getElementById('player1-battle-card');
                const p2Container = document.getElementById('player2-battle-card');
                p1Container.innerHTML = '';
                p2Container.innerHTML = '';
                
                // Create image elements
                const p1Img = new Image();
                const p2Img = new Image();
                
                // Set image sources
                p1Img.src = `/static/cards/${result.battle_cards[0]}`;
                p2Img.src = `/static/cards/${result.battle_cards[1]}`;
                
                // Add classes
                p1Img.className = 'card-img';
                p2Img.className = 'card-img';
                
                // Error handling
                p1Img.onerror = () => {
                    console.error(`Failed to load: ${p1Img.src}`);
                    p1Img.src = '/static/cards/back.png';
                };
                p2Img.onerror = () => {
                    console.error(`Failed to load: ${p2Img.src}`);
                    p2Img.src = '/static/cards/back.png';
                };
                
                // Add to DOM
                p1Container.appendChild(p1Img);
                p2Container.appendChild(p2Img);
                
                // Debug output
                console.log('Player 1 container:', p1Container);
                console.log('Player 2 container:', p2Container);
                console.log('Player 1 image:', p1Img);
                console.log('Player 2 image:', p2Img);
            }
            


            document.getElementById('player1-cards').textContent = result.p1_count;
            document.getElementById('player2-cards').textContent = result.p2_count;

            console.log("Draw completed successfully");

            // const logElement = document.getElementById('result');
            // logElement.innerHTML = result.log;

            updateLog(result.log);

            await updateGameState();

        } catch (error)
        { 
            console.error('Draw error:', error);
            updateLog(`Error: ${error.message}`);
            //showError(error.message);
        } finally {
            drawButton.disabled = false;
            drawButton.textContent = "Draw";
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


function updateLog(message) {
    const logElement = document.getElementById('result');
    logElement.innerHTML = message;
    logElement.scrollTop = logElement.scrollHeight;
}
