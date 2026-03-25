import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading = false;
  submitted = false;
  isRegistering = false;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private authService: AuthService,
    private toastService: ToastService
  ) {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/dashboard']);
    }
  }

  ngOnInit(): void {
    this.initForm();
  }

  initForm() {
      this.loginForm = this.formBuilder.group({
          identifier: ['', Validators.required],
          password: ['', [Validators.required, Validators.minLength(6)]]
      });

      if(this.isRegistering) {
           this.loginForm = this.formBuilder.group({
              username: ['', Validators.required],
              email: ['', [Validators.required, Validators.email]],
              password: ['', [Validators.required, Validators.minLength(6)]]
          });
      }
  }

  toggleMode() {
      this.isRegistering = !this.isRegistering;
      this.submitted = false;
      this.initForm();
  }

  // convenience getter for easy access to form fields
  get f() { return this.loginForm.controls; }

  onSubmit(): void {
    this.submitted = true;

    // stop here if form is invalid
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    
    if (this.isRegistering) {
        this.authService.register(this.f['username'].value, this.f['email'].value, this.f['password'].value)
        .subscribe({
            next: () => {
                this.loading = false;
                this.toggleMode(); // switch back to login
                this.toastService.show('Conta criada com sucesso! Você já pode fazer login.', 'success');
            },
            error: () => {
                this.loading = false;
            }
        });
    } else {
        this.authService.login(this.f['identifier'].value, this.f['password'].value)
        .subscribe({
          next: () => {
            this.toastService.show('Login realizado com sucesso!', 'success');
            this.router.navigate(['/dashboard']);
          },
          error: () => {
            this.loading = false;
          }
        });
    }
  }
}
