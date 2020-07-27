import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { AppRoutingModule } from './app-routing.module';
import { DataService } from './services/data.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFileUploadModule } from 'angular-material-fileupload';
import { FrequencyProcessComponent } from './components/frequency-process/frequency-process.component';
import { SafeHtmlPipe } from './safe-html.pipe';
import { UnitextViewComponent } from './components/unitext-view/unitext-view.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    FrequencyProcessComponent,
    SafeHtmlPipe,
    UnitextViewComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatFileUploadModule
  ],
  providers: [
    DataService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
