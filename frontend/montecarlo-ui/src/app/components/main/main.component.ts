import { Component, OnInit } from '@angular/core';
import {DataService} from "../../services/data/data.service";
// import Plotly from 'plotly.js'

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  data: {
    timestamp: Date,
    symbol: string,
    price: number
  }[];
  metrics: {
    symbol: string,
    rank: string
  }[]

  constructor(private dataSvc: DataService) { }

  ngOnInit(): void {
    this.dataSvc.getMetrics().subscribe(result => this.metrics = result);
  }

  loadData(event){
    this.dataSvc.getData(event.target.value).subscribe(result => {
      this.data = result
      const xData = this.data.map(row => new Date(row.timestamp))
      const yData = this.data.map(row => row.price)
      var data = [{
        x: xData,
        y: yData,
        mode:"markers"
      }];

      var layout = {
        title: "Symbol Price over time"
      };

        (window as any).Plotly.newPlot("plot", data, layout);
    });

  }

}
