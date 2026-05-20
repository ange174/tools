import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 遊戲設置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("貪食蛇 - Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        """重置遊戲"""
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    
    def spawn_food(self):
        """隨機生成食物"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_events(self):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        """更新遊戲狀態"""
        if self.game_over:
            return
        
        self.direction = self.next_direction
        
        # 計算新頭部位置
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, new_head_y := head_y + dy)
        
        # 檢查碰撞牆壁
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
        
        # 檢查碰撞自己
        if new_head in self.snake:
            self.game_over = True
            return
        
        # 移動蛇
        self.snake.insert(0, new_head)
        
        # 檢查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def draw(self):
        """繪製遊戲"""
        self.screen.fill(BLACK)
        
        # 繪製網格
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # 繪製蛇
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * GRID_SIZE + 1, y * GRID_SIZE + 1,
                              GRID_SIZE - 2, GRID_SIZE - 2)
            if i == 0:
                # 頭部
                pygame.draw.rect(self.screen, GREEN, rect)
            else:
                # 身體
                pygame.draw.rect(self.screen, YELLOW, rect)
        
        # 繪製食物
        food_x, food_y = self.food
        food_rect = pygame.Rect(food_x * GRID_SIZE + 1, food_y * GRID_SIZE + 1,
                               GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # 繪製分數
        score_text = self.font.render(f"分數: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 繪製遊戲結束信息
        if self.game_over:
            game_over_text = self.font.render("遊戲結束！", True, RED)
            restart_text = self.small_font.render("按 SPACE 重新開始", True, WHITE)
            
            # 計算居中位置
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """運行遊戲"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
