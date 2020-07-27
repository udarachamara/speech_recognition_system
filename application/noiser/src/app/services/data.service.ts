import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class DataService {

  apiUrl: string = "http://localhost:5002/api/";

  constructor(private httpClient: HttpClient) { }

  uploadFile(data: any): Observable<any>{
    return this.httpClient.post<any>(this.apiUrl +'getOutput', data);
  }

  getProcessAudioClip(): Observable<any>{
    return this.httpClient.get<any>(this.apiUrl + 'getProcessFreqFiles/c331bef1a8');
  }

  getProcessAudioClipFor(name: string): Observable<any>{
    return this.httpClient.get<any>(this.apiUrl + 'getProcessFreqFilesByName/'+ name);
  }

  getUniText(): Observable<any> {
    return this.httpClient.get<any>(this.apiUrl + 'convertText');
  }
}
