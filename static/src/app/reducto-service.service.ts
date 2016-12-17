import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable} from "rxjs/Observable";

@Injectable()
export class ReductoService {

  constructor(public http: Http) { }

  public getUrlSummary(url: string){
    let headers = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
    let myUrl = "http://localhost:8788/api/summarize/summarize"+encodeURI("?url="+url);
    return this.http.get(myUrl, headers).map(res => res.json())
  }

}
