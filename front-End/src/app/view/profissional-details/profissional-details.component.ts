import { Profissional } from '../../model/profissional';
import { Component, OnInit, Input } from '@angular/core';
import { ProfissionalService } from '../../service/profissional.service';
import { ProfissionalListComponent } from '../profissional-list/profissional-list.component';

@Component({
  selector: 'app-profissional-details',
  templateUrl: './profissional-details.component.html',
  styleUrls: ['./profissional-details.component.css']
})
export class ProfissionalDetailsComponent implements OnInit {

  @Input() profissional: Profissional;

  constructor(private profissionalService: ProfissionalService, private listComponent: ProfissionalListComponent) { }

  ngOnInit() {
  }

}
