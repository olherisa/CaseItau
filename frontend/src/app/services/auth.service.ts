import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private currentUserSubject: BehaviorSubject<any>;
  public currentUser: Observable<any>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<any>(this.getDecodedToken());
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): any {
    return this.currentUserSubject.value;
  }

  isLoggedIn(): boolean {
    const token = this.getToken();
    if (!token) return false;
    
    // Check expiration
    const decoded: any = jwtDecode(token);
    const isExpired = decoded.exp < (Date.now() / 1000);
    if (isExpired) {
        this.logout();
        return false;
    }
    return true;
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getDecodedToken(): any {
      const token = this.getToken();
      if(token) {
          try {
             return jwtDecode(token);
          } catch(e) {
              return null;
          }
      }
      return null;
  }

  login(username_or_email: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, { username_or_email, password })
      .pipe(map(response => {
        // store jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem('access_token', response.access_token);
        this.currentUserSubject.next(jwtDecode(response.access_token));
        return response;
      }));
  }

  register(username: string, email: string, password: string): Observable<any> {
      return this.http.post<any>(`${this.apiUrl}/register`, { username, email, password });
  }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('access_token');
    this.currentUserSubject.next(null);
  }
}
