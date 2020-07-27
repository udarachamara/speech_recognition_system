import { Component, OnInit } from '@angular/core';
import { DataService } from 'src/app/services/data.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-frequency-process',
  templateUrl: './frequency-process.component.html',
  styleUrls: ['./frequency-process.component.css']
})
export class FrequencyProcessComponent implements OnInit {

  isProcessComplete: boolean = false;
  ProcessFreqFileList: Array<any> = [];
  FileData: any = [];

  constructor(
    private dataService: DataService,
    public _DomSanitizer: DomSanitizer,) { }

  ngOnInit() {

    this.waitProcessFinish();
  }

  async waitProcessFinish() {
    await this.delay(3000)
    this.dataService.getProcessAudioClip().subscribe(res => {
      
      if (res.data) {
        res.data.forEach(element => {
          // this.ProcessFreqFileList.push({ name: element.name })
          this.dataService.getProcessAudioClipFor(element.name).subscribe(resf=>{
            this.ProcessFreqFileList.push({
              name: element.name,
              data: resf.base64
            });
          })
        });
      }
    }, error => {

    });

    this.isProcessComplete = true;

  }

  getAudioFor(file: string){
    // console.log(file);
    
  }

  private delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  generate(){
    location.href = 'uni-text'
  }

}
