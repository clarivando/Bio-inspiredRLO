import { ProfissionalDetailsComponent } from './../profissional-details/profissional-details.component';
import { Observable } from "rxjs";
import { ProfissionalService } from "../../service/profissional.service";
import { Profissional } from "../../model/profissional";
import { Component, OnInit } from "@angular/core";
import { Router } from '@angular/router';

@Component({
  selector: "app-profissional-list",
  templateUrl: "./profissional-list.component.html",
  styleUrls: ["./profissional-list.component.css"]
})
export class ProfissionalListComponent implements OnInit {
  profissionais: Observable<Profissional[]>;

  constructor(private profissionalService: ProfissionalService,
    private router: Router) {}

  ngOnInit() {
    this.reloadData();
  }

  reloadData() {
    this.profissionais = this.profissionalService.getProfissionaisList();
  }

  deleteProfissional(id: number) {
    this.profissionalService.deleteProfissional(id)
      .subscribe(
        data => {
          console.log('sucesso');
          this.reloadData();
        },
        error => console.log(error));
  }

}
