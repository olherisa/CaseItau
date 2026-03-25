import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GameService } from '../../services/game.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  isLoading = false;
  error = '';
  username = '';

  constructor(
    private gameService: GameService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
      const user = this.authService.currentUserValue;
      if (user && user.username) {
          this.username = user.username;
      }
  }

  startNewGame(): void {
    this.isLoading = true;
    this.error = '';
    
    this.gameService.startNewGame().subscribe({
        next: (response) => {
            this.isLoading = false;
            // Navigate to the newly created game board
            this.router.navigate(['/game', response.game_id]);
        },
        error: (err) => {
            this.isLoading = false;
            this.error = err.message || 'Erro ao iniciar uma nova partida.';
        }
    });
  }

  goToRanking(): void {
      this.router.navigate(['/ranking']);
  }

  logout(): void {
      this.authService.logout();
      this.router.navigate(['/login']);
  }
}
