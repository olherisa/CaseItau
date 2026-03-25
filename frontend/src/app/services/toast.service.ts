import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface ToastMessage {
  message: string;
  type: 'success' | 'error' | 'info';
}

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  private toastsSubject = new BehaviorSubject<ToastMessage[]>([]);
  toasts$ = this.toastsSubject.asObservable();

  show(message: string, type: 'success' | 'error' | 'info' = 'info') {
    const activeToasts = this.toastsSubject.value;
    const newToast = { message, type };
    this.toastsSubject.next([...activeToasts, newToast]);

    setTimeout(() => {
      this.remove(newToast);
    }, 4000);
  }

  remove(toast: ToastMessage) {
    const currentToasts = this.toastsSubject.value;
    this.toastsSubject.next(currentToasts.filter(t => t !== toast));
  }
}
