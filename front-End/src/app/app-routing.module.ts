import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './view/login/login.component';
import { AlunoCreateComponent } from './view/aluno-create/aluno-create.component';
import { IdealLearnObjCreateComponent } from './view/ideal-learn-obj-create/ideal-learn-obj-create.component';
import { CrloComponent } from './view/crlo/crlo.component';

const routes: Routes = [
  { path: '', component: LoginComponent, pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: AlunoCreateComponent},
  {path: 'cadastroideal', component: IdealLearnObjCreateComponent},
  {path: 'crlo', component: CrloComponent}
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
