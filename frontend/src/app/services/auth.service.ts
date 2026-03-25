import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { User } from '../models/user.interface';
import { AuthResponse } from '../models/auth.interface';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<User | null>(null);
    this.currentUser = this.currentUserSubject.asObservable();
    this.checkSession();
  }

  private checkSession() {
      this.http.get<User>(`${this.apiUrl}/me`).subscribe({
          next: (user) => this.currentUserSubject.next(user),
          error: () => this.currentUserSubject.next(null)
      });
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  isLoggedIn(): boolean {
    return this.currentUserValue !== null;
  }

  login(identifier: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, { identifier, password })
      .pipe(map(response => {
        this.currentUserSubject.next({ id: response.user_id, username: response.username });
        return response;
      }));
  }

  register(username: string, email: string, password: string): Observable<any> {
      return this.http.post<any>(`${this.apiUrl}/register`, { username, email, password });
  }

  logout() {
    this.http.post(`${this.apiUrl}/logout`, {}).subscribe({
        next: () => this.currentUserSubject.next(null),
        error: () => this.currentUserSubject.next(null)
    });
  }
}
