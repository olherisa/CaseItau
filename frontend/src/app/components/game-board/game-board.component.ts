import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../../services/game.service';

@Component({
  selector: 'app-game-board',
  templateUrl: './game-board.component.html',
  styleUrls: ['./game-board.component.css']
})
export class GameBoardComponent implements OnInit {
  gameId!: number;
  isLoading = true;
  error = '';
  
  availableColors: string[] = ['R', 'G', 'B', 'Y', 'O', 'P'];
  colorMap: { [key: string]: string } = {
      'R': '#ff4757', // Red
      'G': '#2ed573', // Green
      'B': '#1e90ff', // Blue
      'Y': '#ffa502', // Yellow
      'O': '#ff6348', // Orange
      'P': '#9b59b6'  // Purple
  };

  currentGuess: (string | null)[] = [null, null, null, null];
  
  history: any[] = [];
  isGameOver = false;
  isWinner = false;
  secretCode: string[] | null = null;
  score: number | null = null;
  maxAttempts = 10;

  constructor(
      private route: ActivatedRoute,
      private router: Router,
      private gameService: GameService
  ) {}

  ngOnInit(): void {
      this.route.paramMap.subscribe(params => {
          const idParam = params.get('gameId');
          if (idParam) {
              this.gameId = +idParam;
              this.loadGameStatus();
          } else {
              this.router.navigate(['/dashboard']);
          }
      });
  }

  loadGameStatus(): void {
      this.isLoading = true;
      this.gameService.getGameStatus(this.gameId).subscribe({
          next: (res) => {
              this.updateGameState(res);
              this.isLoading = false;
          },
          error: (err) => {
              this.error = err.message || 'Erro ao carregar o jogo';
              this.isLoading = false;
          }
      });
  }

  updateGameState(state: any): void {
      this.isGameOver = state.is_game_over;
      this.isWinner = state.is_winner;
      this.history = state.attempts || [];
      this.secretCode = state.secret_code;
      this.score = state.score;
  }

  selectColor(color: string, index: number): void {
      if (this.isGameOver) return;
      this.currentGuess[index] = color;
  }
  
  getColorHex(colorCode: string | null | undefined): string {
      return colorCode ? this.colorMap[colorCode] : 'transparent';
  }

  isGuessComplete(): boolean {
      return this.currentGuess.every(c => c !== null);
  }

  submitGuess(): void {
      if (!this.isGuessComplete() || this.isGameOver) return;
      
      this.isLoading = true;
      this.error = '';

      this.gameService.makeGuess(this.gameId, this.currentGuess as string[]).subscribe({
          next: (res) => {
              // Optionally reload full state or append locally
              // We'll reload to ensure we are in sync with backend
              this.loadGameStatus();
              this.currentGuess = [null, null, null, null];
          },
          error: (err) => {
              this.error = err.message;
              this.isLoading = false;
          }
      });
  }

  goBack(): void {
      this.router.navigate(['/dashboard']);
  }
}
