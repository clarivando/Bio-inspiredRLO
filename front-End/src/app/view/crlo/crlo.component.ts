import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { IdealLearnObj } from 'src/app/model/ideal-learn-obj';
import { CrloService } from 'src/app/service/crlo.service';
import { first } from 'rxjs/operators';
import { FormGroup, FormBuilder } from '@angular/forms';
import { AlunoService } from 'src/app/service/aluno.service';
import { IdealLearnObjService } from 'src/app/service/ideal-learn-obj.service';
import { Aluno } from 'src/app/model/aluno';
import { Crlo } from 'src/app/model/crlo';
import { LearnObj } from 'src/app/model/learn-obj';


@Component({
  selector: 'app-crlo',
  templateUrl: './crlo.component.html',
  styleUrls: ['./crlo.component.css']
})
export class CrloComponent implements OnInit {
  loading = false;
  crlo: Crlo = new Crlo();
  crloForm: FormGroup;
  idealLearnObjs: Observable<IdealLearnObj[]>;
  alunos: Observable<Aluno[]>;
  learnObjs:Observable<LearnObj[]>;
  teste='';
<<<<<<< HEAD
  index_aluno=0;
  index_oa_ideal=0;
=======
>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe

  constructor(private formBuilder: FormBuilder,
    private router: Router,
    private crloService : CrloService,
    private alunoService: AlunoService, 
    private idealLearnObjService: IdealLearnObjService) { }

  ngOnInit() {this.crloForm=this.formBuilder.group({
    idealLO:'',
    aluno:'',
    learnObj:''
<<<<<<< HEAD
  })

  this.idealLearnObjService.getIdealLearnObj().subscribe(
    data => {
      this.idealLearnObjs=JSON.parse(data);
      console.log(this.idealLearnObjs);
    },
    error => {
      this.loading = false;
    });

    this.alunoService.getAlunosList().subscribe(
      data => {
          this.alunos=JSON.parse(data);
          console.log(this.alunos);
        },
        error => {
            this.loading = false;
      });
  }

  onSubmit() {
      this.crlo.aluno =this.crloForm.get('aluno').value;
      this.crlo.idealLO = this.crloForm.get('idealLO').value;
     
=======

  })
    this.idealLearnObjs=this.idealLearnObjService.getIdealLearnObj();
    this.alunos=this.alunoService.getAlunosList();

    
  }

  onSubmit() {
      this.crlo.aluno=this.crloForm.get('aluno').value;
      this.teste='12345';
      this.crlo.idealLO=this.crloForm.get('idealLO').value;
>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe
      this.crloService.retrieve(this.crlo)
      .subscribe(
          data => {
            this.learnObjs=JSON.parse(data);
            console.log(this.learnObjs);
          },
          error => {
<<<<<<< HEAD
            this.loading = false;
          });
  }
=======
              this.loading = false;
          });
  }

>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe
}    
  

