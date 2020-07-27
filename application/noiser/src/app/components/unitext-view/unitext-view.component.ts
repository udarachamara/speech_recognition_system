import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { DataService } from 'src/app/services/data.service';

@Component({
  selector: 'app-unitext-view',
  templateUrl: './unitext-view.component.html',
  styleUrls: ['./unitext-view.component.css']
})
export class UnitextViewComponent implements OnInit {

  uniTextFormGroup: FormGroup
  isProcessComplete: boolean = false;
  Success: boolean = false;

  constructor(private fb: FormBuilder, private dataService: DataService) { }

  ngOnInit() {
    this.uniTextFormGroup = this.fb.group({
      textCtrl: ['']
    })

    this.dataService.getUniText().subscribe(res=>{
      console.log(res);
      this.uniTextFormGroup.controls.textCtrl.setValue(res.uni_text)
      this.isProcessComplete = true
      this.Success = true
    }, err=>{
      this.isProcessComplete = true
      this.Success = false
    })
  }

}
