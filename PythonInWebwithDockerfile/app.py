import time
import redis
from flask import Flask, render_template_string, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; }
        canvas { background-color: #000; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Snake Game</h1>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const box = 20;
        let snake = [{x: 9 * box, y: 10 * box}];
        let direction = 'RIGHT';
        let food = {
            x: Math.floor(Math.random() * 19 + 1) * box,
            y: Math.floor(Math.random() * 19 + 1) * box
        };

        document.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowLeft' && direction !== 'RIGHT') direction = 'LEFT';
            else if (event.key === 'ArrowUp' && direction !== 'DOWN') direction = 'UP';
            else if (event.key === 'ArrowRight' && direction !== 'LEFT') direction = 'RIGHT';
            else if (event.key === 'ArrowDown' && direction !== 'UP') direction = 'DOWN';
        });

        function drawGame() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < snake.length; i++) {
                ctx.fillStyle = (i === 0) ? 'green' : 'white';
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
                ctx.strokeStyle = 'red';
                ctx.strokeRect(snake[i].x, snake[i].y, box, box);
            }

            ctx.fillStyle = 'red';
            ctx.fillRect(food.x, food.y, box, box);

            let snakeX = snake[0].x;
            let snakeY = snake[0].y;

            if (direction === 'LEFT') snakeX -= box;
            if (direction === 'UP') snakeY -= box;
            if (direction === 'RIGHT') snakeX += box;
            if (direction === 'DOWN') snakeY += box;

            if (snakeX === food.x && snakeY === food.y) {
                food = {
                    x: Math.floor(Math.random() * 19 + 1) * box,
                    y: Math.floor(Math.random() * 19 + 1) * box
                };
            } else {
                snake.pop();
            }

            const newHead = {x: snakeX, y: snakeY};

            if (snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || collision(newHead, snake)) {
                clearInterval(game);
                alert('Game Over');
                location.reload();
            }

            snake.unshift(newHead);
        }

        function collision(head, array) {
            for (let i = 0; i < array.length; i++) {
                if (head.x === array[i].x && head.y === array[i].y) {
                    return true;
                }
            }
            return false;
        }

        const game = setInterval(drawGame, 100);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
