import { Component, Output, EventEmitter, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MarkdownToHtmlModule } from '../../markdown-to-html.module';
import { MatAccordion } from '@angular/material/expansion';
import {MatCardModule} from '@angular/material/card';

interface ScriptData {
  research_report: string ;
}

@Component({
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  selector: 'app-client-research',
  standalone: true,
  imports: [CommonModule, FormsModule, MatFormFieldModule, MatInputModule, MatButtonModule, MarkdownToHtmlModule,MatCardModule],
  templateUrl: './client-research.component.html',
  styleUrls: ['./client-research.component.css']
})
export class ClientResearchComponent {
  @Output() researchComplete = new EventEmitter<string>();

  prospectName = '';
  prospectPosition = '';
  companyName = '';
  isLoading = false;
  scriptData: any;
  error = '';

  constructor() {}

  async handleResearch(e: Event) {
    e.preventDefault();
    this.isLoading = true;
    this.error = '';
    this.scriptData = undefined;

    try {
      const response = await fetch('http://127.0.0.1:8000/client_research', {
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

      if (!response.ok) {
        const errorData = await response.json();
        this.error = errorData.detail || 'Failed to fetch client research';
        throw new Error(this.error);
      }

      const data = await response.json();
      console.log("Research Data: ", data);
      this.scriptData = { research_report: data.research_report };  
      this.researchComplete.emit(this.scriptData.research_report);

    } catch (err) {
      this.error = err instanceof Error ? err.message : 'Failed to fetch client research';
      console.error('Error:', err);
    } finally {
      this.isLoading = false;
    }
  }
}
