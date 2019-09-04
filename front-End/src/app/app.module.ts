import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { LoginComponent } from './view/login/login.component';
import { AlertComponent } from './_directives/alert/alert.component';
import { RegisterComponent } from './view/register/register.component';
import { AlunoCreateComponent } from './view/aluno-create/aluno-create.component';
import { IdealLearnObjCreateComponent } from './view/ideal-learn-obj-create/ideal-learn-obj-create.component';
import { CrloComponent } from './view/crlo/crlo.component';
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AlertComponent,
    RegisterComponent,
    AlunoCreateComponent,
    IdealLearnObjCreateComponent,
    CrloComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
