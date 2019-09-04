import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { AlunoService } from 'src/app/service/aluno.service';
import { Aluno } from 'src/app/model/aluno';


@Component({templateUrl: 'aluno-create.component.html'})
export class AlunoCreateComponent implements OnInit {
    registerForm: FormGroup;
    loading = false;
    submitted = false;
    aluno: Aluno = new Aluno();
    constructor(
        private formBuilder: FormBuilder,
        private router: Router,
        private alunoService: AlunoService) { }

    ngOnInit() {
        this.registerForm = this.formBuilder.group({
            nome: ['', Validators.required],
            matricula: ['', Validators.required],
            estiloInput: '',
            estiloUnderstanding: '',
            estiloPercpetion: '',
            estiloProcessing: '',
            usuario: ['', Validators.required],
            senha: ['', [Validators.required, Validators.minLength(6)]]
        });
    }

    // convenience getter for easy access to form fields
    get f() { return this.registerForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.registerForm.invalid) {
            return;
        }

        this.loading = true;
        this.alunoService.createAluno(this.registerForm.value)
            .pipe(first())
            .subscribe(
                data => {
                    this.router.navigate(['/login']);
                },
                error => {
                    this.loading = false;
                });
    }
}