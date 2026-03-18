import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private currentUserSubject: BehaviorSubject<any>;
  public currentUser: Observable<any>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<any>(null);
    this.currentUser = this.currentUserSubject.asObservable();
    this.checkSession();
  }

  private checkSession() {
      this.http.get<any>(`${this.apiUrl}/me`).subscribe({
          next: (user) => this.currentUserSubject.next(user),
          error: () => this.currentUserSubject.next(null)
      });
  }

  public get currentUserValue(): any {
    return this.currentUserSubject.value;
  }

  isLoggedIn(): boolean {
    return this.currentUserValue !== null;
  }

  login(username_or_email: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, { username_or_email, password })
      .pipe(map(response => {
        this.currentUserSubject.next({ user_id: response.user_id, username: response.username });
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
