import {Directive, Input, HostListener, OnInit} from '@angular/core';
import { TemplateRef, ViewContainerRef } from '@angular/core';
//http://stackoverflow.com/questions/38483267/angular2-directive-to-modify-click-handling


@Directive({
  selector: '[ngCopy]'
})
export class CopyDirective implements OnInit{

  // targetIsFunction: null;
  targetType: null;
  target: null;


  constructor() { }

  ngOnInit(): void {
    document.addEventListener('copy',this.onCopy);
  }

  @Input('ngCopy') copyTarget: any;
  @Input('ngCopyType') copyType: string = "text/plain";

  @HostListener('click', ['$event'])

  //Static Containers Set On Copy
  static copyContent: any = null;
  static copyType: any = "";
  static copyReady: boolean = false;

  @HostListener('click', ['$event'])
  onClick($event) {
    // Set all our static properties:
    CopyDirective.copyReady = true;
    CopyDirective.copyType = this.copyType;
    CopyDirective.copyContent = this.copyTarget;

    // Now Call Copy:
    document.execCommand('copy'); //Goes to on copy
  }

  onCopy(event){
    console.log("Copy Event");
    if(CopyDirective.copyReady){

      console.log(CopyDirective.copyType +" + "+ CopyDirective.copyContent);
      let result = event.clipboardData.setData(CopyDirective.copyType, CopyDirective.copyContent);
      event.preventDefault();
      CopyDirective.copyReady = false;
    }

  }

}
