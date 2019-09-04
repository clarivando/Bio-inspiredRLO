import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators, FormBuilder, FormArray } from '@angular/forms';
import { first } from 'rxjs/operators';
import { IdealLearnObjService } from 'src/app/service/ideal-learn-obj.service';
import { Router } from '@angular/router';
import { IdealLearnObj } from 'src/app/model/ideal-learn-obj';

@Component({
  selector: 'app-ideal-learn-obj-create',
  templateUrl: './ideal-learn-obj-create.component.html',
  styleUrls: ['./ideal-learn-obj-create.component.css']
})
export class IdealLearnObjCreateComponent implements OnInit {


  idealLOForm: FormGroup
  loading = false;
  submitted = false;
  concepts: FormArray
  orderForm: FormGroup
  idealLearnObj: IdealLearnObj = new IdealLearnObj

  constructor(private formBuilder: FormBuilder,
    private idealLearnObjService: IdealLearnObjService,
    private router: Router) { }

  ngOnInit() {
    this.idealLOForm = this.formBuilder.group({
      title: ['', Validators.required],
      concepts: this.formBuilder.array([this.createConcept()]),
      semantic_density: '',
      difficulty: '',
      interactivity_type: '',
      interactivity_level: ''
    });
  }
  
  createConcept(): FormGroup {
    return this.formBuilder.group({
      concept: ''
    });
  }

  addConcept(): void {
    this.concepts = this.idealLOForm.get('concepts') as FormArray;
    this.concepts.push(this.createConcept());
  }
  getIdealLearnObj(){
    var conceito='';
    var item = '';
    var arrayControl = this.idealLOForm.get('concepts') as FormArray;
    for (let index = 0; index < arrayControl.length; index++) {
      item = arrayControl.at(index).get('concept').value;
      conceito = conceito + item + ';';
    } 


    this.idealLearnObj.title=this.idealLOForm.get('title').value;
    this.idealLearnObj.concept=conceito;
    this.idealLearnObj.semantic_density=this.idealLOForm.get('semantic_density').value;
    this.idealLearnObj.difficulty=this.idealLOForm.get('difficulty').value;
    this.idealLearnObj.interactivity_type=this.idealLOForm.get('interactivity_type').value;
    this.idealLearnObj.interactivity_level=this.idealLOForm.get('interactivity_level').value;
  }

  onSubmit() {
    this.getIdealLearnObj();
    this.submitted = true;

        // stop here if form is invalid
        if (this.idealLOForm.invalid) {
            return;
        }

        this.loading = true;
        this.idealLearnObjService.createIdealLearnObj(this.idealLearnObj)
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



