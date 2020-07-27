import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { FrequencyProcessComponent } from './components/frequency-process/frequency-process.component';
import { UnitextViewComponent } from './components/unitext-view/unitext-view.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'process-step1',
    component: FrequencyProcessComponent
  },
  {
    path: 'uni-text',
    component: UnitextViewComponent
  }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
