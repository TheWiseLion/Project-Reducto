import { Component, ViewContainerRef } from '@angular/core';
import {ReductoService} from "./reducto-service.service";
import {Modal, Overlay} from "angular2-modal";
import {Context, CollectionModalComponent} from "./collection-modal/collection-modal.component";


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  // directives: [CopyDirective]
})
export class AppComponent {
  constructor(public reducto:ReductoService, vcRef: ViewContainerRef, public modal: Modal){}
  articles: Array<any> = [{}];//First element because ngb is a pile of dog shit.
  html: string ="";
  url: string = "";

  //Modified After Load Button
  validUrl: boolean = false;

  //!= null if validUrl
  error: boolean = false;
  errorMessage: string = "Error - Can't Load URL";
  loading: boolean = false;

  /***
   * On Error Of Article Summary
   * @param error
   */
  onError(error:any){
    console.log("Error");
    console.log(error);
    //TODO: set error message
    this.error = true;
    this.validUrl = false;
    this.loading = false;
  }

  /***
   * On Success Of Article Summary
   * @param payload
   */
  onArticleResults(payload: any, url:string){
    console.log("Loaded");
    console.log(payload);
    this.error = false;
    this.validUrl = true;
    this.articles.push( {
      images: payload.images,
      summary: payload.summary,
      title: payload.title,
      website: payload.website,
      fullUrl: url,
      selected: 0,
      showImage: true,
      left: function () {
        this.selected -= 1;
        if(this.selected<0){
          this.selected = this.images.length -1;
        }
      },
      right: function () {
        this.selected += 1;
        if(this.selected==this.images.length){
          this.selected = 0;
        }
      }
    });
    this.loading = false;
  }

  /***
   * On Click Of Add Article Button
   */
  newArticle(){
    let regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
    let valid = regexp.test(this.url);
    if(this.loading) return; //Bounce when still processing the first one.

    if(valid) {
      this.loading = true;
      var tmpUrl = this.url + ""; //Copy of string?
      this.reducto.getUrlSummary(this.url).subscribe(
        data => this.onArticleResults(data,tmpUrl),
        err => this.onError(err),
        () => this.loading = false
      );
    }else{
      this.error = true;
      this.loading = false;
      this.errorMessage = "Invalid URL Format"
    }
  }

  generateSummaries(){

    CollectionModalComponent.email_html = CollectionModalComponent.getArticlesAsEmail(this.articles.slice(1,));
    let context = new Context(this.articles.slice(1,), CollectionModalComponent.email_html);
    let myModal = this.modal.open(CollectionModalComponent,context);
  }

  deleteArticle(index: number){
    console.log(index);
    // if (index > -1) {
    //   this.articles.splice(index, 1);
    // }
    // this.articles2.push(index);
    // this.articles2.splice(0,1);
    this.articles.splice(0,1);
    // this.articles.push(this.articles[0]);
  }
}
