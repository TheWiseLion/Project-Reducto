import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AlertModule, AccordionModule } from 'ng2-bootstrap/ng2-bootstrap';
import { AppComponent } from './app.component';
import {ReductoService} from "./reducto-service.service";
import { CollectionModalComponent } from './collection-modal/collection-modal.component';
import { ModalModule } from 'angular2-modal';
import { BootstrapModalModule } from 'angular2-modal/plugins/bootstrap';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {CopyDirective} from "./ng-copy/ng-copy";

@NgModule({
  declarations: [
    AppComponent,
    CollectionModalComponent,
    CopyDirective
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AccordionModule,
    ModalModule.forRoot(),
    BootstrapModalModule,
    NgbModule.forRoot(),
  ],
  // directives: [CopyDirective],
  providers: [ReductoService],
  bootstrap: [AppComponent],
  // IMPORTANT:
  // Since 'AdditionCalculateWindow' is never explicitly used (in a template)
  // we must tell angular about it.
  entryComponents: [ CollectionModalComponent ]
})
export class AppModule { }
