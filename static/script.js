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
                console.log("Raw card data from server:", result.battle_cards);
                
                // Player 1's card
                const p1Img = document.createElement('img');
                p1Img.src = `/static/cards/${result.battle_cards[0]}`;
                p1Img.alt = "Player 1's card";
                p1Img.classList.add('card-img');
                p1Img.onerror = function() {
                    console.error(`Failed to load: ${this.src}`);
                    //this.src = '/static/cards/back.png';
                };
                
                // Player 2's card
                const p2Img = document.createElement('img');
                p2Img.src = `/static/cards/${result.battle_cards[1]}`;
                p2Img.alt = "Player 2's card";
                p2Img.classList.add('card-img');
                p2Img.onerror = function() {
                    console.error(`Failed to load: ${this.src}`);
                    //this.src = '/static/cards/back.png';
                };
                
                // Update displays with animation
                updateCardDisplay('player1-battle-card', p1Img.outerHTML);
                updateCardDisplay('player2-battle-card', p2Img.outerHTML);
                
                // Debug: Check if elements exist
                console.log("Player 1 battle card element:", document.getElementById('player1-battle-card'));
                console.log("Player 2 battle card element:", document.getElementById('player2-battle-card'));
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


function updateCardDisplay(elementId, cardHTML)
{
    // const container = document.getElementById(elementId);
    // container.classList.add('card-entering');

    // // setTimeout(() => {
    // //     container.innerHTML = cardFilename ?
    // //         `<img src="/static/cards/${cardFilename}" class="card-img" alt="Battle card">` : '';
    // //     container.classList.remove('card-entering');
    // // }, 300);
    // setTimeout(() => {
    //     container.innerHTML = cardHTML || '';
    //     container.classList.remove('card-entering');
    // }, 300);
    // Replace your current updateCardDisplay calls with this:
if (result.battle_cards && result.battle_cards.length >= 2) {
    console.log("Card data received:", result.battle_cards);
    
    // Immediate DOM update (no animation delay)
    document.getElementById('player1-battle-card').innerHTML = `
        <img src="/static/cards/${result.battle_cards[0]}" 
             class="card-img"
             onerror="this.onerror=null;this.src='/static/cards/back.png'">`;
    
    document.getElementById('player2-battle-card').innerHTML = `
        <img src="/static/cards/${result.battle_cards[1]}" 
             class="card-img"
             onerror="this.onerror=null;this.src='/static/cards/back.png'">`;
    
    // Debug verification
    const p1Img = document.querySelector('#player1-battle-card img');
    const p2Img = document.querySelector('#player2-battle-card img');
    console.log("Player 1 img element:", p1Img);
    console.log("Player 2 img element:", p2Img);
    
    if (p1Img) {
        p1Img.onload = () => console.log("P1 image loaded");
        p1Img.onerror = () => console.log("P1 image failed");
    }
    if (p2Img) {
        p2Img.onload = () => console.log("P2 image loaded");
        p2Img.onerror = () => console.log("P2 image failed");
    }
}

}

function updateLog(message) {
    const logElement = document.getElementById('result');
    logElement.innerHTML = message;
    logElement.scrollTop = logElement.scrollHeight;
}
