import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, Pipe } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { DataService } from 'src/app/services/data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {

  // @ViewChild('figAudio', {static: false}) figAudioComp: ElementRef;

  figAudio: any = null;
  audioSrc: any = null;

  public isLoadAudioFile: boolean = false;

  constructor(private router: Router, private dataService: DataService) { }

  ngOnInit() {
  }

  ngAfterViewInit() {
    // this.figAudio = this.figAudioComp;

  }

  onChangeFileInput(fileInput: any) {

    if (fileInput.target.files && fileInput.target.files[0]) {
      this.isLoadAudioFile = true;
      const file = fileInput.target.files[0];
      console.log(file);
      // return
      // const reader = new FileReader();
      // reader.readAsDataURL(file);
      // let data = null;
      // reader.onload = () => {
      //   data = reader.result;
      //   this.audioSrc = data.toString();

      // };
      let data = new FormData()
      data.append('file', file)
      this.dataService.uploadFile(data).subscribe(res => {
        console.log(res);
        this.router.navigateByUrl('process-step1')
      }, error => {
        console.log(error);

      })

    } else {
      this.audioSrc = null;
      this.isLoadAudioFile = false;
    }

  }


}

