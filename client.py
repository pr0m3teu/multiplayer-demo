import pygame
import sys
import socket
import json
from common import *

pygame.init()

class Player(PlayerCommon):
    def __init__(self, x, y, conn) -> None:
        super().__init__(x, y, conn)
        self.rect = pygame.Rect(self.x, self.y, 60, 60)

    def draw_self(self, screen : pygame.Surface):
        pygame.draw.rect(screen, RED, self.rect)


def connect_to_server() -> Player:
    conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_socket.connect((HOST, PORT))
    try:
        msg : dict = json.loads(conn_socket.recv(1024))
        if msg["type"] != "hello":
            raise Exception("ERROR: Could not properly comunicate with server! ")
            
        conn_socket.sendall(json.dumps(msg).encode("utf-8"))

        msg = json.loads(conn_socket.recv(1024))

        if msg["type"] != "pos":
            raise Exception("ERROR: Could not receive intial player data from server!")
        
        player = Player(msg["x"], msg["y"], conn_socket)

    except Exception as e:
        print(e)
        conn_socket.close()
        sys.exit(1)

    return player

def main() -> None:
    screen : pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock : pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Demo")
    
    player = connect_to_server()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                player.conn.close()
                pygame.quit()
                print("Exit Succesfully")
                sys.exit(0)

        screen.fill(BLACK)
        player.draw_self(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

