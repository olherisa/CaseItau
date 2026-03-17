import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private apiGamesUrl = `${environment.apiUrl}/games`;
  private apiRankingUrl = `${environment.apiUrl}/ranking`;

  constructor(private http: HttpClient) { }

  startNewGame(): Observable<any> {
      return this.http.post(`${this.apiGamesUrl}/start`, {});
  }

  makeGuess(gameId: number, guess: string[]): Observable<any> {
      return this.http.post(`${this.apiGamesUrl}/${gameId}/guess`, { guess });
  }

  getGameStatus(gameId: number): Observable<any> {
      return this.http.get(`${this.apiGamesUrl}/${gameId}/status`);
  }

  getRanking(): Observable<any> {
      return this.http.get(this.apiRankingUrl);
  }
}
