import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GameService } from '../../services/game.service';

@Component({
  selector: 'app-ranking',
  templateUrl: './ranking.component.html',
  styleUrls: ['./ranking.component.css']
})
export class RankingComponent implements OnInit {
  ranking: any[] = [];
  isLoading = true;
  error = '';

  constructor(
      private gameService: GameService,
      private router: Router
  ) {}

  ngOnInit(): void {
      this.loadRanking();
  }

  loadRanking(): void {
      this.isLoading = true;
      this.gameService.getRanking().subscribe({
          next: (data) => {
              this.ranking = data;
              this.isLoading = false;
          },
          error: (err) => {
              this.error = 'Erro ao carregar o ranking global.';
              this.isLoading = false;
          }
      });
  }

  goBack(): void {
      this.router.navigate(['/dashboard']);
  }
}
