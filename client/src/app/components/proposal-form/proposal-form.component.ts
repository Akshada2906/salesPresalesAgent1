import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MarkdownModule } from 'ngx-markdown';
import { MarkdownToHtmlModule } from "../../markdown-to-html.module";

interface ProposalData {
  customer: string;
  title: string;
  requirements: string;
  completion: string;
  amount: number;
}

interface ProposalSection {
  title: string;
  content: string;
  layout_rank: number;
}

interface GeneratedProposal {
  proposal: {
    [key: string]: ProposalSection;
  };
}

@Component({
  selector: 'app-proposal-form',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule, HttpClientModule, MatIconModule, MarkdownModule, MarkdownToHtmlModule],
  templateUrl: './proposal-form.component.html',
  styleUrls: ['./proposal-form.component.css'],
  providers: [HttpClient]
})
export class ProposalFormComponent {
  proposalForm: FormGroup;
  isLoading = false;
  proposal: any;

  private http = inject(HttpClient);
  private fb = inject(FormBuilder);

  constructor() {
    this.proposalForm = this.fb.group({
      customer: ['', Validators.required],
      title: ['', Validators.required],
      requirements: ['', Validators.required],
      completion: ['', Validators.required],
      amount: [0, [Validators.required, Validators.min(0)]],
    });
  }

  generateProposal(data: ProposalData): Observable<GeneratedProposal> {
    return this.http.post<GeneratedProposal>('http://localhost:8000/generate_proposal', data);
  }

  handleSubmit(): void {
    if (this.proposalForm.invalid) {
      return;
    }

    this.isLoading = true;

    this.generateProposal(this.proposalForm.value)
    .subscribe(
      (result) => {
        const proposalSections = Object.values(result.proposal);
        proposalSections.sort((a, b) => a.layout_rank - b.layout_rank);
        let proposalData = { proposal: proposalSections };
        this.proposal = proposalData.proposal;
        console.log("111111111 : ", this.proposal);
        this.isLoading = false;
      },
      (error: HttpErrorResponse) => {
        console.error('Error generating proposal:', error);
        this.isLoading = false;
      }
    );  
  }

  get f() {
    return this.proposalForm.controls;
  }
}
