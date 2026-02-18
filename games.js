// Game Variables
let currentGame = null;
let gameLoop = null;

// Game Cards Click Handlers
const gameCards = document.querySelectorAll('.game-card');
const categoryBtns = document.querySelectorAll('.category-btn');
const searchInput = document.getElementById('searchInput');
const gameModal = document.getElementById('gameModal');
const gameCanvas = document.getElementById('gameCanvas');
const ctx = gameCanvas.getContext('2d');

// Click on game card to open game
gameCards.forEach(card => {
    card.addEventListener('click', function() {
        const gameId = this.getAttribute('data-game');
        const gameTitle = this.querySelector('.game-title').textContent;
        openGame(gameId, gameTitle);
    });
});

// Category filter
categoryBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        categoryBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const category = this.getAttribute('data-category');
        
        gameCards.forEach(card => {
            if (category === 'all') {
                card.style.display = 'block';
            } else {
                if (card.getAttribute('data-category') === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            }
        });
    });
});

// Search functionality
searchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    
    gameCards.forEach(card => {
        const title = card.querySelector('.game-title').textContent.toLowerCase();
        const description = card.querySelector('.game-description').textContent.toLowerCase();
        const category = card.querySelector('.game-category').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || description.includes(searchTerm) || category.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

// Open Game Modal
function openGame(gameId, gameTitle) {
    document.getElementById('modalGameTitle').textContent = gameTitle;
    gameModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Stop any running game
    if (gameLoop) {
        cancelAnimationFrame(gameLoop);
    }
    
    // Start the selected game
    switch(gameId) {
        case 'racing1':
            startRacing1();
            break;
        case 'racing2':
            startRacing2();
            break;
        case 'math1':
            startMath1();
            break;
        case 'math2':
            startMath2();
            break;
        case 'action1':
            startAction1();
            break;
        case 'puzzle1':
            startPuzzle1();
            break;
    }
}

// Close Game Modal
function closeGame() {
    gameModal.classList.remove('active');
    document.body.style.overflow = 'auto';
    
    if (gameLoop) {
        cancelAnimationFrame(gameLoop);
        gameLoop = null;
    }
    
    // Clear canvas
    ctx.clearRect(0, 0, gameCanvas.width, gameCanvas.height);
}

// ESC key to close
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && gameModal.classList.contains('active')) {
        closeGame();
    }
});

// ==================== RACING GAME 1 ====================
function startRacing1() {
    const car = {
        x: gameCanvas.width / 2 - 20,
        y: gameCanvas.height - 100,
        width: 40,
        height: 60,
        speed: 5
    };
    
    const obstacles = [];
    let score = 0;
    let gameOver = false;
    
    const keys = {
        left: false,
        right: false
    };
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') keys.left = true;
        if (e.key === 'ArrowRight') keys.right = true;
    });
    
    document.addEventListener('keyup', (e) => {
        if (e.key === 'ArrowLeft') keys.left = false;
        if (e.key === 'ArrowRight') keys.right = false;
    });
    
    function createObstacle() {
        const width = 40;
        const x = Math.random() * (gameCanvas.width - width);
        obstacles.push({
            x: x,
            y: -60,
            width: width,
            height: 60,
            speed: 3
        });
    }
    
    function update() {
        if (gameOver) return;
        
        // Move car
        if (keys.left && car.x > 0) {
            car.x -= car.speed;
        }
        if (keys.right && car.x < gameCanvas.width - car.width) {
            car.x += car.speed;
        }
        
        // Create obstacles
        if (Math.random() < 0.02) {
            createObstacle();
        }
        
        // Move and check obstacles
        for (let i = obstacles.length - 1; i >= 0; i--) {
            obstacles[i].y += obstacles[i].speed;
            
            // Check collision
            if (car.x < obstacles[i].x + obstacles[i].width &&
                car.x + car.width > obstacles[i].x &&
                car.y < obstacles[i].y + obstacles[i].height &&
                car.y + car.height > obstacles[i].y) {
                gameOver = true;
            }
            
            // Remove off-screen obstacles and add score
            if (obstacles[i].y > gameCanvas.height) {
                obstacles.splice(i, 1);
                score++;
            }
        }
    }
    
    function draw() {
        // Clear canvas
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        // Draw road
        ctx.strokeStyle = '#FEC62E';
        ctx.lineWidth = 5;
        ctx.setLineDash([20, 10]);
        ctx.beginPath();
        ctx.moveTo(gameCanvas.width / 2, 0);
        ctx.lineTo(gameCanvas.width / 2, gameCanvas.height);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // Draw car
        ctx.fillStyle = '#FF6B35';
        ctx.fillRect(car.x, car.y, car.width, car.height);
        ctx.fillStyle = '#FEC62E';
        ctx.fillRect(car.x + 5, car.y + 10, 10, 10);
        ctx.fillRect(car.x + 25, car.y + 10, 10, 10);
        
        // Draw obstacles
        ctx.fillStyle = '#666';
        obstacles.forEach(obs => {
            ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
        });
        
        // Draw score
        ctx.fillStyle = '#FEC62E';
        ctx.font = 'bold 24px Fredoka';
        ctx.fillText('Skóre: ' + score, 20, 40);
        
        // Game over
        if (gameOver) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
            ctx.fillStyle = '#FF6B35';
            ctx.font = 'bold 48px Fredoka';
            ctx.textAlign = 'center';
            ctx.fillText('GAME OVER', gameCanvas.width / 2, gameCanvas.height / 2 - 20);
            ctx.fillStyle = '#FEC62E';
            ctx.font = 'bold 32px Fredoka';
            ctx.fillText('Skóre: ' + score, gameCanvas.width / 2, gameCanvas.height / 2 + 30);
            ctx.font = '20px Fredoka';
            ctx.fillStyle = '#fff';
            ctx.fillText('Stiskni ESC pro návrat', gameCanvas.width / 2, gameCanvas.height / 2 + 80);
            ctx.textAlign = 'left';
            return;
        }
    }
    
    function gameLoopFunc() {
        update();
        draw();
        gameLoop = requestAnimationFrame(gameLoopFunc);
    }
    
    gameLoopFunc();
}

// ==================== RACING GAME 2 ====================
function startRacing2() {
    let position = gameCanvas.width / 2;
    let score = 0;
    let speed = 3;
    const coins = [];
    
    const keys = { left: false, right: false };
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') keys.left = true;
        if (e.key === 'ArrowRight') keys.right = true;
    });
    
    document.addEventListener('keyup', (e) => {
        if (e.key === 'ArrowLeft') keys.left = false;
        if (e.key === 'ArrowRight') keys.right = false;
    });
    
    function createCoin() {
        coins.push({
            x: Math.random() * (gameCanvas.width - 30),
            y: -30,
            size: 30,
            collected: false
        });
    }
    
    function update() {
        if (keys.left && position > 30) position -= 5;
        if (keys.right && position < gameCanvas.width - 30) position += 5;
        
        if (Math.random() < 0.03) createCoin();
        
        coins.forEach(coin => {
            if (!coin.collected) {
                coin.y += speed;
                
                const dist = Math.sqrt((coin.x - position) ** 2 + (coin.y - (gameCanvas.height - 80)) ** 2);
                if (dist < 40) {
                    coin.collected = true;
                    score += 10;
                    speed += 0.1;
                }
            }
        });
        
        // Remove off-screen coins
        for (let i = coins.length - 1; i >= 0; i--) {
            if (coins[i].y > gameCanvas.height) {
                coins.splice(i, 1);
            }
        }
    }
    
    function draw() {
        ctx.fillStyle = '#0a0a1a';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        // Draw car
        ctx.fillStyle = '#f093fb';
        ctx.beginPath();
        ctx.arc(position, gameCanvas.height - 80, 30, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw coins
        coins.forEach(coin => {
            if (!coin.collected) {
                ctx.fillStyle = '#FEC62E';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.size / 2, 0, Math.PI * 2);
                ctx.fill();
            }
        });
        
        // Score
        ctx.fillStyle = '#FEC62E';
        ctx.font = 'bold 28px Fredoka';
        ctx.fillText('Skóre: ' + score, 20, 40);
        ctx.font = '16px Fredoka';
        ctx.fillText('Rychlost: ' + speed.toFixed(1), 20, 70);
    }
    
    function gameLoopFunc() {
        update();
        draw();
        gameLoop = requestAnimationFrame(gameLoopFunc);
    }
    
    gameLoopFunc();
}

// ==================== MATH GAME 1 ====================
function startMath1() {
    let score = 0;
    let timeLeft = 30;
    let currentQuestion = null;
    let userAnswer = '';
    
    function generateQuestion() {
        const num1 = Math.floor(Math.random() * 20) + 1;
        const num2 = Math.floor(Math.random() * 20) + 1;
        const operations = ['+', '-', '*'];
        const op = operations[Math.floor(Math.random() * operations.length)];
        
        let answer;
        switch(op) {
            case '+': answer = num1 + num2; break;
            case '-': answer = num1 - num2; break;
            case '*': answer = num1 * num2; break;
        }
        
        currentQuestion = { num1, num2, op, answer };
    }
    
    generateQuestion();
    
    const timerInterval = setInterval(() => {
        timeLeft--;
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
        }
    }, 1000);
    
    document.addEventListener('keydown', handleKeyPress);
    
    function handleKeyPress(e) {
        if (timeLeft <= 0) return;
        
        if (e.key >= '0' && e.key <= '9') {
            userAnswer += e.key;
        } else if (e.key === 'Backspace') {
            userAnswer = userAnswer.slice(0, -1);
        } else if (e.key === 'Enter' && userAnswer !== '') {
            checkAnswer();
        } else if (e.key === '-' && userAnswer === '') {
            userAnswer = '-';
        }
    }
    
    function checkAnswer() {
        if (parseInt(userAnswer) === currentQuestion.answer) {
            score += 10;
            timeLeft += 2;
        } else {
            score = Math.max(0, score - 5);
        }
        userAnswer = '';
        generateQuestion();
    }
    
    function draw() {
        ctx.fillStyle = '#0a1a2e';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        if (timeLeft > 0) {
            // Draw question
            ctx.fillStyle = '#4facfe';
            ctx.font = 'bold 64px Fredoka';
            ctx.textAlign = 'center';
            ctx.fillText(
                `${currentQuestion.num1} ${currentQuestion.op} ${currentQuestion.num2} = ?`,
                gameCanvas.width / 2,
                gameCanvas.height / 2 - 50
            );
            
            // Draw user answer
            ctx.fillStyle = '#FEC62E';
            ctx.font = 'bold 48px Fredoka';
            ctx.fillText(userAnswer || '_', gameCanvas.width / 2, gameCanvas.height / 2 + 50);
            
            // Draw score and time
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 24px Fredoka';
            ctx.textAlign = 'left';
            ctx.fillText('Skóre: ' + score, 20, 40);
            ctx.fillText('Čas: ' + timeLeft + 's', 20, 75);
            
            ctx.font = '18px Fredoka';
            ctx.textAlign = 'center';
            ctx.fillText('Napiš odpověď a stiskni ENTER', gameCanvas.width / 2, gameCanvas.height - 40);
        } else {
            // Game over
            ctx.fillStyle = '#FF6B35';
            ctx.font = 'bold 48px Fredoka';
            ctx.textAlign = 'center';
            ctx.fillText('ČAS VYPRŠEL!', gameCanvas.width / 2, gameCanvas.height / 2 - 20);
            ctx.fillStyle = '#FEC62E';
            ctx.font = 'bold 36px Fredoka';
            ctx.fillText('Tvoje skóre: ' + score, gameCanvas.width / 2, gameCanvas.height / 2 + 40);
            
            document.removeEventListener('keydown', handleKeyPress);
            clearInterval(timerInterval);
        }
        
        ctx.textAlign = 'left';
    }
    
    function gameLoopFunc() {
        draw();
        gameLoop = requestAnimationFrame(gameLoopFunc);
    }
    
    gameLoopFunc();
}

// ==================== MATH GAME 2 ====================
function startMath2() {
    let score = 0;
    let combo = 0;
    let numbers = [];
    let targetSum = 0;
    let selectedNumbers = [];
    
    function generatePuzzle() {
        numbers = [];
        selectedNumbers = [];
        
        // Generate random numbers
        for (let i = 0; i < 6; i++) {
            numbers.push({
                value: Math.floor(Math.random() * 20) + 1,
                x: 150 + (i % 3) * 200,
                y: 150 + Math.floor(i / 3) * 150,
                selected: false
            });
        }
        
        // Pick 2-3 numbers for target
        const count = Math.random() < 0.5 ? 2 : 3;
        const indices = [];
        while (indices.length < count) {
            const idx = Math.floor(Math.random() * numbers.length);
            if (!indices.includes(idx)) indices.push(idx);
        }
        
        targetSum = indices.reduce((sum, idx) => sum + numbers[idx].value, 0);
    }
    
    generatePuzzle();
    
    gameCanvas.addEventListener('click', handleClick);
    
    function handleClick(e) {
        const rect = gameCanvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        numbers.forEach(num => {
            const dist = Math.sqrt((x - num.x) ** 2 + (y - num.y) ** 2);
            if (dist < 40) {
                num.selected = !num.selected;
                checkAnswer();
            }
        });
    }
    
    function checkAnswer() {
        const sum = numbers.filter(n => n.selected).reduce((s, n) => s + n.value, 0);
        
        if (sum === targetSum) {
            const selectedCount = numbers.filter(n => n.selected).length;
            score += 10 * (combo + 1);
            combo++;
            setTimeout(generatePuzzle, 500);
        } else if (sum > targetSum) {
            combo = 0;
        }
    }
    
    function draw() {
        ctx.fillStyle = '#1a0a2e';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        // Draw target
        ctx.fillStyle = '#4facfe';
        ctx.font = 'bold 32px Fredoka';
        ctx.textAlign = 'center';
        ctx.fillText('Cílový součet: ' + targetSum, gameCanvas.width / 2, 50);
        
        // Draw numbers
        numbers.forEach(num => {
            ctx.fillStyle = num.selected ? '#FF6B35' : '#30cfd0';
            ctx.beginPath();
            ctx.arc(num.x, num.y, 40, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 32px Fredoka';
            ctx.fillText(num.value, num.x, num.y + 10);
        });
        
        // Draw score
        ctx.textAlign = 'left';
        ctx.fillStyle = '#FEC62E';
        ctx.font = 'bold 24px Fredoka';
        ctx.fillText('Skóre: ' + score, 20, 40);
        ctx.fillText('Combo: x' + (combo + 1), 20, 75);
        
        ctx.font = '16px Fredoka';
        ctx.textAlign = 'center';
        ctx.fillText('Klikni na čísla, která dají součet!', gameCanvas.width / 2, gameCanvas.height - 30);
    }
    
    function gameLoopFunc() {
        draw();
        gameLoop = requestAnimationFrame(gameLoopFunc);
    }
    
    gameLoopFunc();
}

// ==================== ACTION GAME ====================
function startAction1() {
    const player = {
        x: gameCanvas.width / 2,
        y: gameCanvas.height / 2,
        size: 30
    };
    
    const enemies = [];
    let score = 0;
    let gameOver = false;
    
    gameCanvas.addEventListener('click', shoot);
    
    function createEnemy() {
        const side = Math.floor(Math.random() * 4);
        let x, y;
        
        switch(side) {
            case 0: x = Math.random() * gameCanvas.width; y = -30; break;
            case 1: x = gameCanvas.width + 30; y = Math.random() * gameCanvas.height; break;
            case 2: x = Math.random() * gameCanvas.width; y = gameCanvas.height + 30; break;
            case 3: x = -30; y = Math.random() * gameCanvas.height; break;
        }
        
        enemies.push({
            x: x,
            y: y,
            size: 25,
            speed: 1 + Math.random() * 2,
            health: 2
        });
    }
    
    function shoot(e) {
        if (gameOver) return;
        
        const rect = gameCanvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;
        
        for (let i = enemies.length - 1; i >= 0; i--) {
            const dist = Math.sqrt((clickX - enemies[i].x) ** 2 + (clickY - enemies[i].y) ** 2);
            if (dist < enemies[i].size) {
                enemies[i].health--;
                if (enemies[i].health <= 0) {
                    enemies.splice(i, 1);
                    score += 10;
                }
                break;
            }
        }
    }
    
    function update() {
        if (gameOver) return;
        
        if (Math.random() < 0.02) createEnemy();
        
        enemies.forEach(enemy => {
            const dx = player.x - enemy.x;
            const dy = player.y - enemy.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            enemy.x += (dx / dist) * enemy.speed;
            enemy.y += (dy / dist) * enemy.speed;
            
            if (dist < player.size + enemy.size) {
                gameOver = true;
            }
        });
    }
    
    function draw() {
        ctx.fillStyle = '#0a0a0a';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        // Draw player
        ctx.fillStyle = '#4facfe';
        ctx.beginPath();
        ctx.arc(player.x, player.y, player.size, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw enemies
        enemies.forEach(enemy => {
            ctx.fillStyle = enemy.health === 1 ? '#f5576c' : '#FF6B35';
            ctx.beginPath();
            ctx.arc(enemy.x, enemy.y, enemy.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        // Score
        ctx.fillStyle = '#FEC62E';
        ctx.font = 'bold 24px Fredoka';
        ctx.fillText('Skóre: ' + score, 20, 40);
        ctx.font = '16px Fredoka';
        ctx.fillText('Klikej na nepřátele!', 20, 70);
        
        if (gameOver) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
            ctx.fillStyle = '#FF6B35';
            ctx.font = 'bold 48px Fredoka';
            ctx.textAlign = 'center';
            ctx.fillText('GAME OVER', gameCanvas.width / 2, gameCanvas.height / 2);
            ctx.fillStyle = '#FEC62E';
            ctx.font = 'bold 32px Fredoka';
            ctx.fillText('Skóre: ' + score, gameCanvas.width / 2, gameCanvas.height / 2 + 50);
        }
    }
    
    function gameLoopFunc() {
        update();
        draw();
        gameLoop = requestAnimationFrame(gameLoopFunc);
    }
    
    gameLoopFunc();
}

// ==================== PUZZLE GAME ====================
function startPuzzle1() {
    const cards = [];
    const icons = ['🎮', '🏆', '⭐', '🎯', '🎨', '🎪', '🎭', '🎸'];
    let flippedCards = [];
    let matchedPairs = 0;
    let moves = 0;
    
    // Create pairs
    const cardValues = [...icons, ...icons].sort(() => Math.random() - 0.5);
    
    for (let i = 0; i < 16; i++) {
        cards.push({
            x: 150 + (i % 4) * 150,
            y: 50 + Math.floor(i / 4) * 110,
            width: 120,
            height: 100,
            value: cardValues[i],
            flipped: false,
            matched: false
        });
    }
    
    gameCanvas.addEventListener('click', handleCardClick);
    
    function handleCardClick(e) {
        if (flippedCards.length >= 2) return;
        
        const rect = gameCanvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        cards.forEach(card => {
            if (!card.flipped && !card.matched &&
                x > card.x && x < card.x + card.width &&
                y > card.y && y < card.y + card.height) {
                
                card.flipped = true;
                flippedCards.push(card);
                
                if (flippedCards.length === 2) {
                    moves++;
                    setTimeout(checkMatch, 800);
                }
            }
        });
    }
    
    function checkMatch() {
        if (flippedCards[0].value === flippedCards[1].value) {
            flippedCards[0].matched = true;
            flippedCards[1].matched = true;
            matchedPairs++;
        } else {
            flippedCards[0].flipped = false;
            flippedCards[1].flipped = false;
        }
        flippedCards = [];
    }
    
    function draw() {
        ctx.fillStyle = '#16213e';
        ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
        
        // Draw cards
        cards.forEach(card => {
            if (card.matched) {
                ctx.fillStyle = '#2ecc71';
            } else if (card.flipped) {
                ctx.fillStyle = '#FEC62E';
            } else {
                ctx.fillStyle = '#30cfd0';
            }
            
            ctx.fillRect(card.x, card.y, card.width, card.height);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
            ctx.strokeRect(card.x, card.y, card.width, card.height);
            
            if (card.flipped || card.matched) {
                ctx.font = '48px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(card.value, card.x + card.width / 2, card.y + card.height / 2);
            }
        });
        
        // Stats
        ctx.fillStyle = '#FEC62E';
        ctx.font = 'bold 20px Fredoka';
        ctx.textAlign = 'left';
        ctx.fillText('Tahy: ' + moves, 20, 30);
        ctx.fillText('Páry: ' + matchedPairs + '/8', 20, 60);
        
        // Win condition
        if (matchedPairs === 8) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(0, 0, gameCanvas.width, gameCanvas.height);
            ctx.fillStyle = '#2ecc71';
            ctx.font = 'bold 48px Fredoka';
            ctx.textAlign = 'center';
            ctx.fillText('VYHRÁLS!', gameCanvas.width / 2, gameCanvas.height / 2);
            ctx.fillStyle = '#FEC62E';
            ctx.font = 'bold 32px Fredoka';
            ctx.fillText('Tahů: ' + moves, gameCanvas.width / 2, gameCanvas.height / 2 + 50);
        }
    }
    
    function gameLoopFunc() {
        draw();
        gameLoop = requestAnimationFrame(gameLoopFunc);
    }
    
    gameLoopFunc();
}