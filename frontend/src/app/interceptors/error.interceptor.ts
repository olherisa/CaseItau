import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { ToastService } from '../services/toast.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService, private router: Router, private toastService: ToastService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError((err: HttpErrorResponse) => {
      let errorMsg = '';
      
      if (err.status === 401) {
          // auto logout if 401 response returned from api
          this.authService.logout();
          this.router.navigate(['/login']);
          errorMsg = 'Sua sessão expirou ou token inválido. Por favor, faça login novamente.';
      } else if (err.error && err.error.detail) {
          // standard backend business exception structure
          errorMsg = err.error.detail;
      } else {
          errorMsg = "Ocorreu um erro inesperado na comunicação com o servidor.";
      }

      this.toastService.show(errorMsg, 'error');
      console.error('API Error:', err);
      return throwError(() => new Error(errorMsg));
    }));
  }
}
