import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { LucideAngularModule } from 'lucide-angular';

interface ScriptData {
  opening_approaches: string[];
  pain_points: Array<{
    id: string;
    description: string;
    impact: string;
    discovery_questions: string[];
  }>;
  solution_positioning: Array<{
    pain_point_id: string;
    solution: string;
    benefits: string[];
    success_story: string;
  }>;
  objection_handlers: Array<{
    objection: string;
    response: string;
    follow_up: string;
  }>;
  value_based_closing: string[];
  supporting_elements: {
    statistics: string[];
    roi_calculations: string[];
  };
}

@Component({
  selector: 'app-script-generator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatExpansionModule,
    MatProgressSpinnerModule,
    LucideAngularModule 
  ],
  templateUrl: './script-generator.component.html',
  styleUrls: ['./script-generator.component.css']
})
export class ScriptGeneratorComponent {
  @Input() companyResearch = '';
  
  prospectName = '';
  prospectPosition = '';
  companyName = '';
  isLoading = false;
  scriptData: ScriptData | null = null;
  error = '';
  openAccordion: 'coldCall' | 'salesScript' | 'solutions' | 'objectives' | 'objectionHandlers' | 'closingStatements' | null = null;

  toggleAccordion(section: 'coldCall' | 'salesScript' | 'solutions' | 'objectives' | 'objectionHandlers' | 'closingStatements') {
    this.openAccordion = this.openAccordion === section ? null : section;
  }

  async handleResearch(e: Event) {
    e.preventDefault();
    this.isLoading = true;
    this.error = '';
    this.scriptData = null;

    try {
      const response = await fetch('http://127.0.0.1:8000/generate_script', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          prospect_name: this.prospectName,
          prospect_position: this.prospectPosition,
          company_name: this.companyName
        }),
      });

      console.log("111111111111111111 : ", response);
      

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate scripts');
      }

      const data = await response.json();
      console.log("2222222222 : ", data);

      console.log("444444444444444 : ", data.script);
      
      
      this.scriptData = JSON.parse(data.script);
      // this.scriptData = data.script;

      console.log("33333333333333 : ", this.scriptData);
      
      this.openAccordion = 'coldCall'; // Open first accordion by default

    } catch (err) {
      this.error = err instanceof Error ? err.message : 'Failed to generate scripts';
      console.error('Error:', err);
    } finally {
      this.isLoading = false;
    }
  }

  getPainPointDescription(painPointId: string): string {
    const painPoint = this.scriptData?.pain_points.find(p => p.id === painPointId);
    return painPoint ? painPoint.description : 'Unknown';
  }  
}
