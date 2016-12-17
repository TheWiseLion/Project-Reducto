import {Injectable, Inject} from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable} from "rxjs/Observable";
import {DOCUMENT} from '@angular/platform-browser';

@Injectable()
export class ReductoService {

  constructor(public http: Http,@Inject(DOCUMENT) private document) { }

  public getUrlSummary(url: string){
    let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
    let myUrl = document.location.protocol +'//'+ document.location.hostname+"/api/summarize/summarize"+encodeURI("?url="+url);
    return this.http.get(myUrl, headers).map(res => res.json())
  }

}
